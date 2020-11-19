# The code that trains the neural network

import sqlite3



#Note: change the directory below to wherever the 2015-01.db database is stored on your computer.
connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()

if __name__ == "__main__":
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
        parent = result[0]
        #parent is the string to be tokenized and inputted into the neural network.

        #bucket the string into an array
        # DYLAN ADD CODE HERE


        #load the neural network


        #send the bucketed words into the network
        model.fit(bucketedinputs,bucketedoutputs,epochs=1)
