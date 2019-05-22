import time
from os import listdir
import os.path as op
from OpenDocx import get_text
import pickle
from PrepareHandContent import remove_non_glosses
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from tensorflow.python.keras.callbacks import TensorBoard
from keras.models import load_model


start_time = time.time()


def time_elapsed(sec):
    """Calculates time to train model"""
    if sec < 60:
        return str(sec) + " sec"
    elif sec < (60 * 60):
        return str(sec / 60) + " min"
    else:
        return str(sec / (60 * 60)) + " hr"


# Set how many characters the model should look at before predicting an upcoming character
pre_characters = 7
print("Set training parameters...")


# Import the training set of glosses for use as the single training text
one_text_in = open("toktrain.pkl", "rb")
one_text = " ".join(pickle.load(one_text_in))
text_name = "Wb. Training Glosses"

# # Import and clean CELT texts for use as the single training text
# clean_text_list = []
# all_clean_files = [f for f in listdir("CELT_Texts_Clean") if op.isfile(op.join("CELT_Texts_Clean", f))]
# for cf in all_clean_files:
#     cf = "".join(cf.split(".docx"))
#     if cf != ".DS_Store":
#         cf = op.join("CELT_Texts_Clean", cf)
#         clean_text_list.append(get_text(cf))
# one_text = " ".join(clean_text_list)
# one_text = " ".join(one_text.split("\n"))
# while "  " in one_text:
#     one_text = " ".join(one_text.split("  "))
# text_name = "CELT Collection"

# Import test and train sets for character mapping
train_in = open("toktrain.pkl", "rb")
train_set = pickle.load(train_in)
test_in = open("toktest.pkl", "rb")
test_set = pickle.load(test_in)
x_train = remove_non_glosses(train_set)
temp = []  # Reverse x_train for reverse models
for x_trainer in x_train[::-1]:  # Reverse x_train for reverse models
    new_trainer = x_trainer[::-1]  # Reverse x_train for reverse models
    temp.append(new_trainer)  # Reverse x_train for reverse models
x_train = temp  # Reverse x_train for reverse models
x_test, y_test = test_set[0], test_set[1]
print("Loaded {}, training, and test data...".format(text_name))


# Combine all test and train sets into one list for later operations
all_testtrain = [one_text] + x_train + x_test + y_test


# Maps all characters in both sets
chars = sorted(list(set("".join(all_testtrain))))
chardict = dict((c, i + 1) for i, c in enumerate(chars))
chardict["$"] = 0
vocab_size = len(chardict)
print('    No. of characters: %d' % vocab_size)
rchardict = dict((i + 1, c) for i, c in enumerate(chars))
rchardict[0] = "$"
print("Mapped Characters...")


def encode(string_list):
    """Encodes a list of glosses using mapping"""
    num_list = list()
    for plain_string in string_list:
        encoded_string = [chardict[char] for char in plain_string]
        num_list.append(encoded_string)
    return num_list


def sequence(string_list):
    """Organises gloss content into sequences"""
    one_liner = " ".join(string_list)
    sequences = list()
    for i in range(pre_characters, len(one_liner)):
        # select sequence of tokens
        seq = one_liner[i - pre_characters: i + 1]
        if seq[-1] != " ":
            seq = seq[:-1] + "$"
        # store this seq
        sequences.append(seq)
    print('    Total Sequences for {0}: {1}'.format(seq_name, len(sequences)))
    return sequences


# Organize into sequences
seq_name = "training"
x_train = sequence([one_text])
print("Organised {} into sequences...".format(text_name))


# Encode all glosses using mapping (for use with padding)
x_train = encode(x_train)
print("Encoded {}...".format(text_name))


# Separate training into input and output, and one hot encode all training sequences
sequences = np.array(x_train)
x_train, y_train = sequences[:, : - 1], sequences[:, - 1]
sequences = [to_categorical(x, num_classes=vocab_size) for x in x_train]
x_train = np.array(sequences)
y_train = to_categorical(y_train, num_classes=vocab_size)
print("One Hot encoded {}...".format(text_name))


# Define model
nodes = 54
epochs = 8
model_name = "rev-n{}_{}x{}-{}-Wb-bi.h5".format(pre_characters, nodes, nodes, epochs)  # Name model
model = Sequential()
model.add(LSTM(nodes, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))  # 1 Hidden Layer
# model.add(LSTM(nodes, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))  # 2 Hidden Layers
# model.add(LSTM(nodes, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))  # 3 Hidden Layers
model.add(LSTM(nodes, input_shape=(x_train.shape[1], x_train.shape[2])))  # 4 Hidden Layers
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())
# Log the model
tb = TensorBoard(log_dir="logs/{}".format(model_name[:-3]))
# Compile and fit model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, verbose=2, callbacks=[tb])
print("Created Model...")


# Save the model
model.save(model_name)
# # Save the mapping
# pickle.dump(chardict, open('char_mappingTBF.pkl', 'wb'))  # Name mapping
print("Saved Model...")


# # Load the model
# model = load_model('n3_Tokeniser.h5')  # Model name
# # Load the mapping
# chardict = pickle.load(open('char_mappingTBF.pkl', 'rb'))  # Mapping Name


end_time = time.time()
seconds_elapsed = end_time - start_time
print("Time elapsed: " + time_elapsed(seconds_elapsed))

