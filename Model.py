# The code that creates the initial network and saves it
import tensorflow as tf
from tensorflow import keras

if __name__ == "__main__":
    #Create neural network
    model = keras.layers.Sequential([
        keras.layers.Flatten(input_shape=(100,1)),
        keras.layers.Dense(64,activation=tf.nm.relu),
        keras.layers.Dense(100,activation=tf.nm.softmax)])

    #save both of the models to the computer so they can be accessed by train.py and inference.py later
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver.save(sess, 'my_test_model')