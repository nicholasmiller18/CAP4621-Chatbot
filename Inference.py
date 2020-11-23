import sqlite3
import os
import tensorflow as tf
from tensorflow import keras
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lookups import Lookups
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

checkpoint_path = "training_checkpoints/cp.ckpt"
connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()

def CreateModel():
    #Define the neural network
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=100, return_sequences=True),input_shape=100)) #input layer
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=64))) #middle layers
    model.add(keras.layers.Dense(units=100,name='Output'))

    #Compile the model
    model.compile(optimizer='Adam',loss='CosineSimilarity')

    model.summary()

    return model

def convertToNums(s):
    ret = []
    tokens = word_tokenize(s)
    i = 0
    for token in tokens:
        if i >= 100:
            break
        sql = "SELECT index FROM dict WHERE word = {};".format(token)
        c.execute(sql)
        num = c.fetchone()
        ret.append(num)
        i+=1
    while len(ret) < 100:
        ret.append(0)
    return ret

def convertToSentence(output_data):
    ret = []
    for token in output_data:
        if token != 0:
            sql = "SELECT word FROM dict WHERE index = {};".format(token)
            c.execute(sql)
            word = c.fetchone()
            ret.append(word)
        else:
            break
    sentence = ""
    for word in ret:
        sentence = sentence + word + " "
    return sentence

if __name__ == "__main__":
    #create a blank model, the same one used in train
    print("Creating model.")
    model = CreateModel()

    #load previously calculated/trained weights to the blank model
    print("Loading trained model.")
    model.load_weights(checkpoint_path)

    while True:
        #ask for a sentence to input
        s = Input("Enter a sentence: ")

        #covert the sentence to numbers
        input_data = convertToNums(s)

        #input the sentence to the model
        output_data = model.predict(input_data)

        #turn the model output into words using the dictionary
        sentence = convertToSentence(output_data)
        print(sentence)