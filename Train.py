# The code that trains the neural network

import sqlite3
import os
import tensorflow as tf
from tensorflow import keras

#Note: change the directory below to wherever the 2015-01.db database is stored on your computer.
connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()

def CreateModel():
    #Define the neural network
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Dense(100,activation=tf.nn.relu,input_shape=(100,))) #input layer
    model.add(keras.layers.Dense(1024,activation=tf.nn.relu)) #middle layers
    model.add(keras.layers.Dense(1024,activation=tf.nn.relu)) #middle layers
    model.add(keras.layers.Dense(100)) #output layer

    #Compile the model
    model.build()

    model.summary()

    return model


#Starting point for the code
if __name__ == "__main__":
    #create the neural network
    model = CreateModel()

    #get the total number of paired comments in the database
    sql = "SELECT COUNT(*) FROM parent_reply;"
    c.execute(sql)
    result = c.fetchone()
    totalPairs = result[0]

    for rowCounter in range(0,totalPairs):
        #fetch the post (what is inputted to the neural network)
        sql = "SELECT parent FROM parent_reply LIMIT 1 OFFSET '{}';".format(rowCounter)
        c.execute(sql)
        result = c.fetchone()
        parent = result[0] #parent is the string to be tokenized and inputted into the neural network.

        #bucket the string into an array
        # DYLAN ADD CODE HERE





    #define the directory to save checkpoints during training so it can be accessed by other files or in the future
    checkpoint_path = "training_checkpoints/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_patt)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,verbose=1)

    #train the model
    model.fit(input_data,output_data,epochs=3,callbacks = [cp_callback])
