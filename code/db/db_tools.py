'''
code/db/db_tools.py

2048-intelligent-bot: DB tools and data handling with pandas.

Author: Filip J. Cierkosz 2022 (updated: 2023)
'''


import sqlite3
import pandas as pd


def init_db():
    '''
    Initializes the database to store: 
        sample's ID, score, win/loss, time played, date.
    '''
    db = sqlite3.connect('db/bot_records_2023.db')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS bot_records_2023')
    cursor.execute(
        '''CREATE TABLE bot_records_2023 (
            id INTEGER PRIMARY KEY,
            score INTEGER,
            win INTEGER,
            time_played_sec FLOAT,
            date_played TEXT
        )'''
    )
    db.commit()
    db.close()
    print('The DB has been successfully initialized.')

def update_db(win, score, t_sec, date):
    '''
    Updates the database inserting a new row.

        Parameters:
            win (int)     : 1 for win, 0 for loss
            score (int)   : game score
            t_sec (float) : game time (in seconds)
            date          : game date
    '''
    # Update only if the bot managed to run (i.e. no error/external interruption).
    if t_sec > 0:
        try:
            db = sqlite3.connect('db/bot_records_2023.db')
            cursor = db.cursor()
            insert_with_params = '''INSERT INTO bot_records_2023
                                    (score, win, time_played_sec, date_played)
                                    VALUES (?, ?, ?, ?);'''
            data = (score, win, t_sec, date)
            cursor.execute(insert_with_params, data)
            db.commit()
            db.close()
            print(
                f'''The DB has been successfully updated with new data:\n
                    - score : {score}
                    - win : {win}
                    - time_played_sec : {t_sec},
                    - date_played : {date}\n'''
            )
        except sqlite3.Error as e:
            print('Failed to update the DB. An error occurred:\n', e)
    else:
        print('\nNo updates to the DB.\n')

def print_records_db():
    '''
    Displays the database records using pandas dataframe.
    '''
    try:
        db = sqlite3.connect('db/bot_records_2023.db')
        df = pd.read_sql_query('SELECT * FROM ', db)
        print(df.to_string())
    except sqlite3.Error as e:
        print('Failed to process the DB. An error occurred:\n', e)
