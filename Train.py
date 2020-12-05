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
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=100, return_sequences=True),input_shape=(100,1))) #input layer
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=64))) #middle layers
    model.add(keras.layers.Dense(units=100,name='Output'))

    #Compile the model
    model.compile(optimizer='Adam',loss='mean_squared_error')

    model.summary()

    return model


#Starting point for the code
if __name__ == "__main__":
    #size check on training data
    sql = "SELECT COUNT(0) FROM parent_nums;"
    c.execute(sql)
    result = c.fetchone()
    totalPairs = result[0]
    print(totalPairs)

    #create the neural network
    print("Creating model.")
    model = CreateModel()

    #try to load previously saved weights to the network
    try:
        model.load_weights(checkpoint_path)
    except:
        print("No previous model has been trained.")

    #define the directory to save checkpoints during training so it can be accessed by other files or in the future
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,save_weights_only=True,verbose=1,save_freq=100)

    #get the input train data
    sql = "SELECT * FROM parent_nums;"
    c.execute(sql)
    i_data = c.fetchall()
    input_data = np.array(i_data).reshape(totalPairs,100,1)

    #get the output train data
    sql = "SELECT * FROM comment_nums;"
    c.execute(sql)
    o_data = c.fetchall()
    output_data = np.array(o_data).reshape(totalPairs,100,1)

    #train the model
    model.fit(input_data,output_data,epochs=3,callbacks = [cp_callback])
