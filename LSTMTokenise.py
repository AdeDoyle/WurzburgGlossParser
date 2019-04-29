import time
import pickle
from PrepareHandContent import remove_non_glosses
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

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
pre_characters = 3
print("Set training parameters...")


# Import test and train sets
train_in = open("toktrain.pkl", "rb")
train_set = pickle.load(train_in)
test_in = open("toktest.pkl", "rb")
test_set = pickle.load(test_in)
x_train = remove_non_glosses(train_set)
x_test, y_test = test_set[0], test_set[1]
print("Loaded training and test data...")


# Combine all test and train sets into one list for later operations
all_testtrain = x_train + x_test + y_test


# Maps all characters in both sets
chars = sorted(list(set("".join(all_testtrain))))
chardict = dict((c, i + 1) for i, c in enumerate(chars))
rchardict = dict((i + 1, c) for i, c in enumerate(chars))
print("Mapped Characters...")


def encode(string_list):
    """Encodes a list of glosses using mapping"""
    temp_list = list()
    for plain_string in string_list:
        encoded_string = [chardict[char] for char in plain_string]
        temp_list.append(encoded_string)
    return temp_list


# Encode all glosses using mapping
x_train = encode(x_train)
x_test = encode(x_test)
y_test = encode(y_test)
print("Encoded training and test data...")


def pad(string_list):
    """Pads a list of glosses so that they all come to same length"""
    max_len = max([len(x) for x in all_testtrain]) + pre_characters
    padded_array = np.array(pad_sequences(string_list, maxlen=max_len, padding="pre"))
    return padded_array


# Pad all glosses to same length
x_train = pad(x_train)
x_test = pad(x_test)
y_test = pad(y_test)
print("Padded training and test data...")


# One hot encode all glosses
x_train = to_categorical(x_train)
x_test = to_categorical(x_test)
y_test = to_categorical(y_test)
print("One Hot encoded training and test data...")


def decode(string_list):
    """Decodes a list of strings with characters rendered as One Hot vectors"""
    temp_list = list()
    for encoded_string in string_list:
        string_list = []
        for char_vect in encoded_string:
            from_categorical = np.argmax(char_vect)
            if from_categorical != 0:
                string_list.append(from_categorical)
        temp_list.append(string_list)
    temp_list2 = list()
    for num_string in temp_list:
        string_list = []
        for num_char in num_string:
            decoded_char = rchardict[num_char]
            string_list.append(decoded_char)
        temp_list2.append("".join(string_list))
    return temp_list2


end_time = time.time()
seconds_elapsed = end_time - start_time
print("Time elapsed: " + time_elapsed(seconds_elapsed))

