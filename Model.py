# The code that creates the initial network and saves it
import tensorflow as tf
from tensorflow import keras

if __name__ == "__main__":
    #Create encoder network
    encodermodel = keras.layers.Sequential([
        keras.layers.Flatten(input_shape=(100,1)),
        keras.layers.Dense(64,activation=tf.nm.relu),
        keras.layers.Dense(100,activation=tf.nm.softmax)])

    #Create decoder network
    decodermodel = keras.layers.Sequential([
        keras.layers.Flatten(input_shape=(100,1)),
        keras.layers.Dense(64,activation=tf.nm.relu),
        keras.layers.Dense(100,activation=tf.nm.softmax)])

    #save both of the models to the computer so they can be accessed by train.py and inference.py later