'''
2048 GAME PROJECT: Data handling with database and pandas dataframe.

Date created:
    06/2022

Author:
    Filip J. Cierkosz
'''

import sqlite3
import pandas as pd

def init_db():
    '''
    Initializes the database to store: sample's ID, win/loss, time played, date.
    '''
    db = sqlite3.connect('db/scores.db')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute('''
                CREATE TABLE scores (
                    id INTEGER PRIMARY KEY,
                    win INTEGER,
                    time_played_sec FLOAT,
                    date_played TEXT)
            ''')
    db.commit()
    db.close()
    print('The DB has been successfully initialized.')

def update_db(win, tsec, dt):
    '''
    Updates the database inserting a new row.
    '''
    # Update only if the bot managed to run (i.e. no error, or external interruption).
    if (tsec>0):
        try:
            db = sqlite3.connect('db/scores.db')
            cursor = db.cursor()
            insert_with_params = '''INSERT INTO scores
                                    (win, time_played_sec, date_played)
                                    VALUES (?, ?, ?);'''
            data = (win, tsec, dt)
            cursor.execute(insert_with_params, data)
            db.commit()
            db.close()
            print(f'''The DB has been successfully updated with new data:\n
                    win : {win}
                    time_played_sec : {tsec},
                    date_played : {dt}\n''')
        except sqlite3.Error as e:
            print(f'Failed to update the DB. An error occurred:\n', e)
    else:
        print('\nNo updates to the DB.\n')

def print_records_db():
    '''
    Displays the database records using pandas dataframe.
    '''
    try:
        db = sqlite3.connect('db/scores.db')
        df = pd.read_sql_query("SELECT * FROM scores", db)
        print(df.to_string())
    except sqlite3.Error as e:
        print(f'Failed to process the DB. An error occurred:\n', e)

# Initialize the database (executed only once, or when to recreate the DB).
#initDB()

# Display all the database records (for testing purposes).
# To run file scores.py for purposes of printing DB records, change line 112:
# from: db = sqlite3.connect('db/scores.db')
# to: db = sqlite3.connect('scores.db')
#print_records_db()
