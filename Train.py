# The code that trains the neural network

import sqlite3
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

#Note: change the directory below to wherever the 2015-01.db database is stored on your computer.
connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()
checkpoint_path = "training_checkpoints/cp.ckpt"

def CreateModel():
    #Define the neural network
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Bidirectional(layers.LSTM(64, return_sequences=True), input_shape=(1, 100))) #input layer
    model.add(keras.layers.Bidirectional(layers.LSTM(32))) #middle layers
    model.add(keras.layers.Dense(units=100,name='Output'))

    #Compile the model
    model.compile(optimizer='Adam',loss='CosineSimilarity')

    model.summary()

    return model


#Starting point for the code
if __name__ == "__main__":
    #create the neural network
    model = CreateModel()

    #try to load previously saved weights to the network
    model.load_weights(checkpoint_path)

    #define the directory to save checkpoints during training so it can be accessed by other files or in the future
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,save_weights_only=True,verbose=1,save_freq=10000)

    #get the input train data
    sql = "SELECT * FROM parent_num;"
    c.execute(sql)
    input_data = c.fetchone()

    #get the output train data
    sql = "SELECT * FROM comment_num"
    c.execue(sql)
    output_data = c.fetchone()

    #train the model
    model.fit(input_data,output_data,epochs=3,callbacks = [cp_callback])
