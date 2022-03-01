'''
2048 GAME PROJECT: Data handling with DB.

Date created:
    03/2022

Author:
    Filip J. Cierkosz
'''

import sqlite3
import pandas as pd

def initDB():
    '''
    Initializes the database to store: user's ID, grid size, score, time played, date.
    '''
    # Connect with the DB. Create the cursor.
    db = sqlite3.connect('scores.db')
    cursor = db.cursor()

    # Create the table with appropriate schema.
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute('''
                CREATE TABLE scores (
                    id INTEGER PRIMARY KEY,
                    grid_size INTEGER,
                    score INTEGER,
                    time_played_sec FLOAT,
                    date_played TEXT
                )
            ''')

    # Commit the operations and close the DB.
    db.commit()
    db.close()
    print('The DB has been successfully initialized.')

def updateDB(id, gs, sc, tsec, dt):
    '''
    Updates the database inserting a new row.
    '''
    if (tsec>0):
        try:
            # Connect with the DB and create the cursor.
            db = sqlite3.connect('scores.db')
            cursor = db.cursor()

            # Prepare the data to be inserted.
            insertWithParams = '''INSERT INTO scores
                                (id, grid_size, score, time_played_sec, date_played)
                                VALUES (?, ?, ?, ?, ?);'''
            dataInsert = (id, gs, sc, tsec, dt)

            # Execute the operation with specified params. Then, commit and close the DB.
            cursor.execute(insertWithParams, dataInsert)
            db.commit()
            db.close()
            print(f'''The DB has been successfully updated with new data:

                    id : {id}
                    grid_size : {gs}
                    score : {sc},
                    time_played_sec : {tsec},
                    date_played : {dt}
                    ''')
        # Error handling.
        except sqlite3.Error as e:
            print(f'Failed to update the DB. An error occurred:\n', e)
    else:
        print('No updates to the DB.')

def countDBRows():
    '''
    Counts the rows in the database to assign ID number to a new input.

        Returns:
            counter (int) : Number of rows in the table (used to assign ID).
    '''
    try:
        # Connect with the DB and create the cursor.
        db = sqlite3.connect('scores.db')
        cursor = db.cursor()

        # Count the rows in the DB and return counter.
        cursor.execute('SELECT COUNT(*) FROM scores')
        counter = cursor.fetchone()[0]
        return counter
    # Error handling.
    except sqlite3.Error as e:
        print(f'Failed to count the DB rows. An error occurred:\n', e)

# Initialize the database (executed only at the very beginning).
#initDB()

#updateDB(123, 4, 2048, 60.0, '13-02-2022')

#print(countDBRows())

'''
TO DO:
1. Pandas dataframe for displaying all the records in the DB.
2. Method to get the best score on a particular grid.
'''
