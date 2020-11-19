# The code that trains the neural network

import sqlite3
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np

#Note: change the directory below to wherever the 2015-01.db database is stored on your computer.
connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()

def CreateModel():
    #Define the neural network
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Dense(units=3,activation=tf.nn.relu,input_shape=(3,1),name='Input')) #input layer
    model.add(keras.layers.Dense(units=1024,activation=tf.nn.relu,name='Hidden_1')) #middle layers
    model.add(keras.layers.Dense(units=1024,activation=tf.nn.relu,name='Hidden_2')) #middle layers
    model.add(keras.layers.Dense(units=3,name='Output')) #output layer

    #Compile the model
    #model.build()
    model.compile(optimizer='Adam',loss='CosineSimilarity')

    model.summary()

    return model


#Starting point for the code
if __name__ == "__main__":
    #create the neural network
    model = CreateModel()

    #define the directory to save checkpoints during training so it can be accessed by other files or in the future
    checkpoint_path = "training_checkpoints/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,verbose=1)

    input_data = np.array([1,2,3],dtype ='float')
    output_data = np.array([3,2,1],dtype='float')
    #replace input_data and output_data with our reddit training data


    #train the model
    model.fit(input_data,output_data,epochs=3,callbacks = [cp_callback])
