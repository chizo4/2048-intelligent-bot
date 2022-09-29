'''
user_implementation/db/scores.py

2048-Project: Data handling with database and pandas dataframe.

Author: Filip J. Cierkosz (2022)
'''


import sqlite3
import pandas as pd


def init_db():
    '''
    Initializes the database to store:
        user's ID, grid size, score, time played, date.
    '''
    db = sqlite3.connect('db/scores.db')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute(
        '''CREATE TABLE scores (
            id INTEGER PRIMARY KEY,
            grid_size INTEGER,
            score INTEGER,
            time_played_sec FLOAT,
            date_played TEXT
        )'''
    )
    db.commit()
    db.close()
    print('The DB has been successfully initialized.')

def update_db(id, gs, sc, tsec, dt):
    '''
    Updates the database inserting a new row.
    '''
    # Update only if the execution of the game was full, i.e. the user did not
    # escape the game before losing.
    if tsec > 0:
        try:
            db = sqlite3.connect('db/scores.db')
            cursor = db.cursor()
            insert_with_params = '''INSERT INTO scores
                                    (id, grid_size, score, time_played_sec, date_played)
                                    VALUES (?, ?, ?, ?, ?);'''
            data = (id, gs, sc, tsec, dt)
            cursor.execute(insert_with_params, data)
            db.commit()
            db.close()
            print(
                f'''The DB has been successfully updated with new data:\n
                    id : {id}
                    grid_size : {gs}
                    score : {sc}
                    time_played_sec : {tsec}
                    date_played : {dt}\n'''
            )
        except sqlite3.Error as e:
            print(f'Failed to update the DB. An error occurred:\n', e)
    else:
        print('\nNo updates to the DB.\n')

def count_db_rows():
    '''
    Counts the rows in the database to assign ID number to a new input.

        Returns:
            counter (int) : Number of rows in the table (used to assign ID).
    '''
    try:
        db = sqlite3.connect('db/scores.db')
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM scores')
        counter = cursor.fetchone()[0]
        db.close()
        return counter
    except sqlite3.Error as e:
        print(f'Failed to count the DB rows. An error occurred:\n', e)

def get_grid_best_score(gs):
    '''
    Finds the best score recorded in the database for an input grid size.

        Parameters:
            gs (int) : Size of the currently selected grid.

        Returns:
            best (int) : Best score on the currently selected grid.
    '''
    try:
        db = sqlite3.connect('db/scores.db')
        df = pd.read_sql_query(f'SELECT * FROM scores WHERE grid_size = {gs}', db)

        # Find the best score among filtered results.
        best = df[df['score'] == df['score'].max()]

        # If dataframe is not empty, return the score. Otherwise, return 0.
        if not best.empty:
            return best.values[0][2]

        return 0
    except sqlite3.Error as e:
        print(f'Failed to retrieve the DB data. An error occurred:\n', e)

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
