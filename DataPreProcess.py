# This is a sample Python script.
import sqlite3
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lookups import Lookups
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
connection = sqlite3.connect('C:/Users/Mark/Desktop/Chatbot/2015-01.db')
c = connection.cursor()

'''def split(toSplit, irregVerbs, dicts):
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
    return ret'''
def split(toSplit, d):
    ret = []
    tokens = word_tokenize(toSplit)
    for token in tokens:
        i = 0
        if i >= 100:
            break
        t = token.lower()
        index = d.getNum(t)
        ret.append(index)
        i+=1
    while len(ret) < 100:
        ret.append(0)
    return ret

'''
def getIrregularVerbs():
    file = open("irregularverbs.txt")
    irregVerbs = []
    for line in file:
        low = line.split()
        for word in low:
            irregVerbs.append(word)
    return irregVerbs'''

class dicts():
    def __init__(self):
        self.maxID = 1
        self.wordDict = {'': 0}
        self.iDDict = {0 : ''}
    def getMax(self):
        return self.maxID
    def add(self, word):
        if not word in self.wordDict:
            self.wordDict[word] = self.maxID
            self.iDDict[self.maxID] = word
            self.maxID += 1
    def getNum(self, word):
        if not word in self.wordDict:
            self.add(word)
        return self.wordDict[word]

    def getWord(self, id):
        return self.iDDict[id]

    '''def convertToNums(self, splitList):
        vec = []
        for token in splitList:
            vec.append(self.getNum(token))
        return vec'''

if __name__ == "__main__":
    #Delete previous entries in tables
    c.execute("DELETE FROM parent_nums;")
    #convert parent posts to numbers

    #create the sql table if it does not already exist
    c.execute("CREATE TABLE IF NOT EXISTS parent_nums('0' INT, '1' INT, '2' INT, '3' INT, '4' INT, '5' INT, '6' INT, '7' INT, '8' INT, '9' INT, '10' INT, '11' INT, '12' INT, '13' INT, '14' INT, '15' INT, '16' INT, '17' INT, '18' INT, '19' INT, '20' INT, '21' INT, '22' INT, '23' INT, '24' INT, '25' INT, '26' INT, '27' INT, '28' INT, '29' INT, '30' INT, '31' INT, '32' INT, '33' INT, '34' INT, '35' INT, '36' INT, '37' INT, '38' INT, '39' INT, '40' INT, '41' INT, '42' INT, '43' INT, '44' INT, '45' INT, '46' INT, '47' INT, '48' INT, '49' INT, '50' INT, '51' INT, '52' INT, '53' INT, '54' INT, '55' INT, '56' INT, '57' INT, '58' INT, '59' INT, '60' INT, '61' INT, '62' INT, '63' INT, '64' INT, '65' INT, '66' INT, '67' INT, '68' INT, '69' INT, '70' INT, '71' INT, '72' INT, '73' INT, '74' INT, '75' INT, '76' INT, '77' INT, '78' INT, '79' INT, '80' INT, '81' INT, '82' INT, '83' INT, '84' INT, '85' INT, '86' INT, '87' INT, '88' INT, '89' INT, '90' INT, '91' INT, '92' INT, '93' INT, '94' INT, '95' INT, '96' INT, '97' INT, '98' INT, '99' INT)")

    #get total number of pairs in parent_reply table
    sql = "SELECT COUNT(parent) FROM parent_reply;"
    c.execute(sql)
    result = c.fetchone()
    totalPairs = result[0]
    print(totalPairs)

    d = dicts()
    print("Converting strings to number arrays for the posts")
    for x in range(totalPairs):
        c.execute("SELECT parent FROM parent_reply LIMIT 1 OFFSET {};".format(x))
        result = c.fetchone()
        s = result[0]

        #convert the sentence into numbers
        vec = split(s, d)

        #place the vector of numbers into a row in an sql table
        sql = "INSERT INTO parent_nums('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99') VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(vec[0],vec[1],vec[2],vec[3],vec[4],vec[5],vec[6],vec[7],vec[8],vec[9],vec[10],vec[11],vec[12],vec[13],vec[14],vec[15],vec[16],vec[17],vec[18],vec[19],vec[20],vec[21],vec[22],vec[23],vec[24],vec[25],vec[26],vec[27],vec[28],vec[29],vec[30],vec[31],vec[32],vec[33],vec[34],vec[35],vec[36],vec[37],vec[38],vec[39],vec[40],vec[41],vec[42],vec[43],vec[44],vec[45],vec[46],vec[47],vec[48],vec[49],vec[50],vec[51],vec[52],vec[53],vec[54],vec[55],vec[56],vec[57],vec[58],vec[59],vec[60],vec[61],vec[62],vec[63],vec[64],vec[65],vec[66],vec[67],vec[68],vec[69],vec[70],vec[71],vec[72],vec[73],vec[74],vec[75],vec[76],vec[77],vec[78],vec[79],vec[80],vec[81],vec[82],vec[83],vec[84],vec[85],vec[86],vec[87],vec[88],vec[89],vec[90],vec[91],vec[92],vec[93],vec[94],vec[95],vec[96],vec[97],vec[98],vec[99])
        c.execute(sql)

        #print out every 100,000 pairs for sanity check
        if x % 10000 == 0:
            print("Inserted {} parent posts into parent_nums".format(x))
            print("Sinity Check:")
            print(s)
            print("Converted To:")
            print(vec)



    #convert comment posts to numbers
    #create the sql table if it does not already exist
    c.execute("CREATE TABLE IF NOT EXISTS comment_nums('0' INT, '1' INT, '2' INT, '3' INT, '4' INT, '5' INT, '6' INT, '7' INT, '8' INT, '9' INT, '10' INT, '11' INT, '12' INT, '13' INT, '14' INT, '15' INT, '16' INT, '17' INT, '18' INT, '19' INT, '20' INT, '21' INT, '22' INT, '23' INT, '24' INT, '25' INT, '26' INT, '27' INT, '28' INT, '29' INT, '30' INT, '31' INT, '32' INT, '33' INT, '34' INT, '35' INT, '36' INT, '37' INT, '38' INT, '39' INT, '40' INT, '41' INT, '42' INT, '43' INT, '44' INT, '45' INT, '46' INT, '47' INT, '48' INT, '49' INT, '50' INT, '51' INT, '52' INT, '53' INT, '54' INT, '55' INT, '56' INT, '57' INT, '58' INT, '59' INT, '60' INT, '61' INT, '62' INT, '63' INT, '64' INT, '65' INT, '66' INT, '67' INT, '68' INT, '69' INT, '70' INT, '71' INT, '72' INT, '73' INT, '74' INT, '75' INT, '76' INT, '77' INT, '78' INT, '79' INT, '80' INT, '81' INT, '82' INT, '83' INT, '84' INT, '85' INT, '86' INT, '87' INT, '88' INT, '89' INT, '90' INT, '91' INT, '92' INT, '93' INT, '94' INT, '95' INT, '96' INT, '97' INT, '98' INT, '99' INT)")

    #get total number of pairs in parent_reply table
    c.execute("SELECT COUNT(comment) FROM parent_reply;")
    result = c.fetchone()
    totalPairs = result[0]
    print(totalPairs)

    print("Converting strings to number arrays for the comments")
    for x in range(totalPairs):
        c.execute("SELECT comment FROM parent_reply LIMIT 1 OFFSET {};".format(x))
        result = c.fetchone()
        s = result[0]

        #convert the sentence into numbers
        vec = split(s, d)

        #place the vector of numbers into a row in an sql table
        sql = "INSERT INTO comment_nums('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99') VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(vec[0],vec[1],vec[2],vec[3],vec[4],vec[5],vec[6],vec[7],vec[8],vec[9],vec[10],vec[11],vec[12],vec[13],vec[14],vec[15],vec[16],vec[17],vec[18],vec[19],vec[20],vec[21],vec[22],vec[23],vec[24],vec[25],vec[26],vec[27],vec[28],vec[29],vec[30],vec[31],vec[32],vec[33],vec[34],vec[35],vec[36],vec[37],vec[38],vec[39],vec[40],vec[41],vec[42],vec[43],vec[44],vec[45],vec[46],vec[47],vec[48],vec[49],vec[50],vec[51],vec[52],vec[53],vec[54],vec[55],vec[56],vec[57],vec[58],vec[59],vec[60],vec[61],vec[62],vec[63],vec[64],vec[65],vec[66],vec[67],vec[68],vec[69],vec[70],vec[71],vec[72],vec[73],vec[74],vec[75],vec[76],vec[77],vec[78],vec[79],vec[80],vec[81],vec[82],vec[83],vec[84],vec[85],vec[86],vec[87],vec[88],vec[89],vec[90],vec[91],vec[92],vec[93],vec[94],vec[95],vec[96],vec[97],vec[98],vec[99])
        c.execute(sql)

        #print out every 100,000 pairs for sanity check
        if x % 10000 == 0:
            print("Inserted {} comment posts into comment_nums".format(x))
            print("Sinity Check:")
            print(s)
            print("Converted To:")
            print(vec)

    #create the sql table if it does not already exist
    print("Saving dictionary.")
    c.execute("CREATE TABLE IF NOT EXISTS dict(index INT, word TEXT)")

    for x in range(d.maxID):
        c.execute("INSERT INTO dict(index,word) VALUES ({}, {})".format(x,d.getWord(x)))
