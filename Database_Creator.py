import sqlite3
import json
from datetime import datetime
import time

sql_transaction = []
start_row = 0

connection = sqlite3.connect('TrainingData.db')
c = connection.cursor()

#only push chanages to database every 1000 lines to save time
def sqlpush_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            c.execute(s)
        connection.commit()
        sql_transaction = []

def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
    sqlpush_bldr(sql)

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
    sqlpush_bldr(sql)

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
    sqlpush_bldr(sql)

def acceptable(data):
    if len(data.split(' ')) > 1000 or len(data) < 1:
        return False
    elif len(data) > 32000:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else:
        return True

def find_parent(parent_id):
    sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(parent_id)
    c.execute(sql)
    result = c.fetchone()
    if result != None:
        return result[0]
    else:
        return False

def find_existing_score(parent_id):
    sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(parent_id)
    c.execute(sql)
    result = c.fetchone()
    if result != None:
        return result[0]
    else: 
        return False
    
if __name__ == '__main__':
    c.execute("CREATE TABLE IF NOT EXISTS parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")
    row_counter = 0
    paired_rows = 0

    with open('C:/Users/twinm/Documents/College Super Senior/Artificial Intelligence/Chatbot/RC_2015-01', buffering=1000) as f:
        for row in f:
            row_counter += 1
            if row_counter > start_row:
                try:
                    #load the row and assign its data to variables
                    row = json.loads(row)
                    parent_id = row['parent_id'].split('_')[1]

                    data = row['body']
                    body = data.replace('\n',' newlinechar ').replace('\r',' newlinechar ').replace('"',"'")

                    created_utc = row['created_utc']
                    score = row['score']
                    comment_id = row['id']
                    subreddit = row['subreddit']
                    parent_data = find_parent(parent_id)
                    
                    #determine if this comment is more upvoted than other comments on this reddit post
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            if acceptable(body):
                                sql_insert_replace_comment(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                
                    else:
                        if acceptable(body):
                            if parent_data:
                                if score >= 2:
                                    sql_insert_has_parent(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                    paired_rows += 1
                            #if parent has no comment assigned
                            else:
                                sql_insert_no_parent(comment_id,parent_id,body,subreddit,created_utc,score)
                except Exception as e:
                    print(str(e))
                            
            #just prints out the progess since this will take a long time
            if row_counter % 10000 == 0:
                print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))
