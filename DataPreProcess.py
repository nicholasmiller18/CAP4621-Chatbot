# This is a sample Python script.
import sqlite3
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lookups import Lookups
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

connection = sqlite3.connect('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/2015-01.db')
c = connection.cursor()

def split(toSplit, irregVerbs, dicts):
    ret = []
    model = spacy.load("en_core_web_sm")
    #lookups = Lookups()
    text = model(toSplit)
    stemmer = SnowballStemmer("english")
    wordsTotal = 0
    for word in text:
        if wordsTotal > 100:
            break
        stem = stemmer.stem(word.text)
        if word.pos_ == "PRON":
            if word.text == 'I':
                ret.append(word.text)
                dicts.add(word.text, False)
            else:
                ret.append(word.text.lower())
                dicts.add(word.text.lower(), False)
        elif word.ent_iob_ != 'O':
            ret.append(word.text)
            dicts.add(word.text, False)
        elif word.pos_ == "PROPN":
            ret.append(word.text)
            dicts.add(word.text, False)
        elif word.text.lower() in irregVerbs:
            ret.append(word.text.lower())
            dicts.add(word.text.lower(), False)
        elif word.text.lower() == "'m":
            ret.append('am')
            dicts.add('am', False)
        elif word.text.lower() != word.lemma_:
            ret.append(word.lemma_)
            dicts.add(word.lemma_, False)
            ending = word.text.replace(stem, '', 1)
            if len(ending) == 4 and ending.endswith("ing"):
                ret.append(ending[1:].lower())
                dicts.add(ending[1:].lower(), True)
                wordsTotal+=1
            elif ending != '':
                ret.append(ending.lower())
                dicts.add(ending.lower(), True)
                wordsTotal+=1
        else:
            ret.append(word.text.lower())
            dicts.add(word.text.lower(), False)
        wordsTotal+=1
    while len(ret) < 100:
        ret.append('')
    return ret

def getIrregularVerbs():
    file = open("irregularverbs.txt")
    irregVerbs = []
    for line in file:
        low = line.split()
        for word in low:
            irregVerbs.append(word)
    return irregVerbs

class dicts():
    def __init__(self):
        self.minID = -1
        self.maxID = 1
        self.wordDict = {'': 0}
        self.iDDict = {0 : ''}
    def getMin(self):
        return self.minID
    def add(self, word, suffix):
        if not word in self.wordDict:
            if suffix == True:
                self.wordDict[word] = self.minID
                self.iDDict[self.minID] = word
                self.minID -= 1
            else:
                self.wordDict[word] = self.maxID
                self.iDDict[self.maxID] = word
                self.maxID += 1
    def getNum(self, word):
        if not word in self.wordDict:
            add(word, True)
        return self.wordDict[word]

    def getWord(self, id):
        return self.iDDict[id]

    def convertToNums(self, splitList):
        vec = []
        for token in splitList:
            vec.append(self.getNum(token))
        return vec

if __name__ == "__main__":
    #Delete previous entries in tables
    c.execute("DELETE FROM parent_nums;")
    c.execute("DELETE FROM comment_nums;")
    #convert parent posts to numbers

    #create the sql table if it does not already exist
    c.execute("CREATE TABLE IF NOT EXISTS parent_nums('0' INT, '1' INT, '2' INT, '3' INT, '4' INT, '5' INT, '6' INT, '7' INT, '8' INT, '9' INT, '10' INT, '11' INT, '12' INT, '13' INT, '14' INT, '15' INT, '16' INT, '17' INT, '18' INT, '19' INT, '20' INT, '21' INT, '22' INT, '23' INT, '24' INT, '25' INT, '26' INT, '27' INT, '28' INT, '29' INT, '30' INT, '31' INT, '32' INT, '33' INT, '34' INT, '35' INT, '36' INT, '37' INT, '38' INT, '39' INT, '40' INT, '41' INT, '42' INT, '43' INT, '44' INT, '45' INT, '46' INT, '47' INT, '48' INT, '49' INT, '50' INT, '51' INT, '52' INT, '53' INT, '54' INT, '55' INT, '56' INT, '57' INT, '58' INT, '59' INT, '60' INT, '61' INT, '62' INT, '63' INT, '64' INT, '65' INT, '66' INT, '67' INT, '68' INT, '69' INT, '70' INT, '71' INT, '72' INT, '73' INT, '74' INT, '75' INT, '76' INT, '77' INT, '78' INT, '79' INT, '80' INT, '81' INT, '82' INT, '83' INT, '84' INT, '85' INT, '86' INT, '87' INT, '88' INT, '89' INT, '90' INT, '91' INT, '92' INT, '93' INT, '94' INT, '95' INT, '96' INT, '97' INT, '98' INT, '99' INT)")

    #get total number of pairs in parent_reply table
    sql = "SELECT COUNT(parent) FROM parent_reply"
    c.execute(sql)
    result = c.fetchone()
    totalPairs = result[0]
    print(totalPairs)

    d = dicts()
    irv = getIrregularVerbs()
    print("Converting strings to number arrays for the posts")
    for x in range(totalPairs):
        sql = "SELECT parent FROM parent_reply LIMIT 1 OFFSET {}".format(x)
        c.execute(sql)
        result = c.fetchone()
        s = result[0]

        #convert the sentence into numbers
        vec = d.convertToNums(split(s, irv, d))

        #place the vector of numbers into a row in an sql table
        sqlbldr = []
        for ind in range(100):
            sql = "INSERT INTO parent_nums('{}') VALUES ({})".format(ind,vec[ind])
            sqlbldr.append(sql)
        for sq in sqlbldr:
            c.execute(sq)

        #print out every 100,000 pairs for sanity check
        if x % 100000 == 0:
            print("Inserted {} parent posts into parent_nums".format(x))
            print("Sinity Check:")
            print(s)
            print("Converted To:")
            print(vec)



    #convert comment posts to numbers
    #create the sql table if it does not already exist
    c.execute("CREATE TABLE IF NOT EXISTS comment_nums('0' INT, '1' INT, '2' INT, '3' INT, '4' INT, '5' INT, '6' INT, '7' INT, '8' INT, '9' INT, '10' INT, '11' INT, '12' INT, '13' INT, '14' INT, '15' INT, '16' INT, '17' INT, '18' INT, '19' INT, '20' INT, '21' INT, '22' INT, '23' INT, '24' INT, '25' INT, '26' INT, '27' INT, '28' INT, '29' INT, '30' INT, '31' INT, '32' INT, '33' INT, '34' INT, '35' INT, '36' INT, '37' INT, '38' INT, '39' INT, '40' INT, '41' INT, '42' INT, '43' INT, '44' INT, '45' INT, '46' INT, '47' INT, '48' INT, '49' INT, '50' INT, '51' INT, '52' INT, '53' INT, '54' INT, '55' INT, '56' INT, '57' INT, '58' INT, '59' INT, '60' INT, '61' INT, '62' INT, '63' INT, '64' INT, '65' INT, '66' INT, '67' INT, '68' INT, '69' INT, '70' INT, '71' INT, '72' INT, '73' INT, '74' INT, '75' INT, '76' INT, '77' INT, '78' INT, '79' INT, '80' INT, '81' INT, '82' INT, '83' INT, '84' INT, '85' INT, '86' INT, '87' INT, '88' INT, '89' INT, '90' INT, '91' INT, '92' INT, '93' INT, '94' INT, '95' INT, '96' INT, '97' INT, '98' INT, '99' INT)")

    #get total number of pairs in parent_reply table
    sql = "SELECT COUNT(comment) FROM parent_reply"
    c.execute(sql)
    result = c.fetchone()
    totalPairs = result[0]
    print(totalPairs)

    print("Converting strings to number arrays for the comments")
    for x in range(totalPairs):
        sql = "SELECT comment FROM parent_reply LIMIT 1 OFFSET {}".format(x)
        c.execute(sql)
        result = c.fetchone()
        s = result[0]

        #convert the sentence into numbers
        vec = d.convertToNums(split(s, irv, d))

        #place the vector of numbers into a row in an sql table
        sqlbldr = []
        for ind in range(100):
            sql = "INSERT INTO comment_nums('{}') VALUES ({})".format(ind,vec[ind])
            sqlbldr.append(sql)
        for sq in sqlbldr:
            c.execute(sq)

        #print out every 100,000 pairs for sanity check
        if x % 100000 == 0:
            print("Inserted {} comment posts into comment_nums".format(x))
            print("Sinity Check:")
            print(s)
            print("Converted To:")
            print(vec)

    #create the sql table if it does not already exist
    print("Saving dictionary.")
    c.execute("CREATE TABLE IF NOT EXISTS dict(index INT, word TEXT)")

    for x in range(d.maxID):
        c.execute("INSERT INTO dict({},{})".format(x,d.getWord(x)))

