import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import random
import collections
import time
from PrepareHandContent import combinelists, compile_tokenised_glosslist


start_time = time.time()


# Calculates time to train model
def time_elapsed(sec):
    if sec < 60:
        return str(sec) + " sec"
    elif sec < (60 * 60):
        return str(sec / 60) + " min"
    else:
        return str(sec / (60 * 60)) + " hr"


# Targets Log Path (where graph will be stored)
logs_path = "/tmp/tensorflow/rnn_chars"
writer = tf.summary.FileWriter(logs_path)


# Training File
training_file = "Wb. All Glosses"


# Read the training file
def read_data(fname):
    # Split glosses, then tokenise each gloss
    allglosstoks = compile_tokenised_glosslist(training_file)
    # Remove Latin markers, then join all back into one string, add white space to start and end of string.
    combinedglosstoks = combinelists(allglosstoks)
    combinedglosstoks = [i for i in combinedglosstoks if i != "*Latin*"]
    combogltokslatrem = []
    for i in combinedglosstoks:
        if "*Latin*" not in i:
            combogltokslatrem.append(i)
        else:
            jlist = i.split("*Latin*")
            for j in jlist:
                if j != "":
                    combogltokslatrem.append(j)
    content = " " + " ".join(combogltokslatrem) + " "
    content = [content[i] for i in range(len(content))]
    content = np.array(content)
    content = np.reshape(content, [-1, ])
    return content


training_data = read_data(training_file)
print("Loaded training data...")


def build_dataset(chars):
    count = collections.Counter(chars).most_common()
    dictionary = dict()
    for char, _ in count:
        dictionary[char] = len(dictionary)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, reverse_dictionary


dictionary, reverse_dictionary = build_dataset(training_data)
vocab_size = len(dictionary)


# Parameters
learning_rate = 0.001  # Steps in which variables are updated
training_iterations = 50000  # Epochs
display_step = 1000  # Batch size: output will be shown after every X epochs
n_input = 3


# Units in RNN cell
n_hidden = 512


# Graph input for tensorflow
x = tf.placeholder("float", [n_input, 1])  # input values
y = tf.placeholder("float", vocab_size)  # labels


# RNN output node weights and biases
weights = {
    "out": tf.Variable(tf.random_normal([n_hidden, vocab_size]))
}
biases = {
    "out": tf.Variable(tf.random_normal([vocab_size]))
}


# Define RNN model
def RNN(x, weights, biases):
    # Reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])
    # Generate an n_input-element sequence of inputs
    # e.g. [.], [i], [.] -> [5], [2], [5]
    x = tf.split(x, n_input, 1)
    # Two layer LSTM, each layer having n_hidden units
    rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden), rnn.BasicLSTMCell(n_hidden)])
    # # One layer LSTM with n_hidden units
    # rnn_cell = rnn.BasicLSTMCell(n_hidden)
    # Generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)
    # There are n_input outputs, but only the last output is wanted
    return tf.matmul(outputs[-1], weights["out"] + biases["out"])


# Prediction
pred = RNN(x, weights, biases)


# Loss and Optimiser
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimiser = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)


# Model evaluation
correct_pred = tf.equal(tf.arg_max(pred, 1), tf.arg_max(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


# Initialise the variables
init = tf.global_variables_initializer()


# Launch the graph
with tf.Session() as session:
    session.run(init)
    step = 0
    offset = random.randint(0, n_input + 1)
    end_offset = n_input + 1
    act_total = 0
    loss_total = 0

    writer.add_graph(session.graph)

    while step < training_iterations:
        # Generate a small batch, add some randomness on selection process
        if offset > (len(training_data) - end_offset):
            offset = random.randint(0, n_input + 1)


