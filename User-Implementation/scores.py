'''
2048 GAME PROJECT: Data handling with DB.

Date created:
    02/2022

Author:
    Filip J. Cierkosz
'''

import sqlite3
import pandas as pd

def initDB():
    '''
    Initializes the database to store user's id, grid_size, score, time_played, date.
    '''
    # Connect with the DB.
    db = sqlite3.connect('scores.db')
    # Create the cursor.
    cursor = db.cursor()
    # Create the table.
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute('''
                CREATE TABLE scores (
                    id INTEGER PRIMARY KEY,
                    grid_size INTEGER,
                    score INTEGER,
                    time_played_sec FLOAT
                    date TEXT
                )
            ''')

    # Commit and close the DB.
    db.commit()
    db.close()
    # Confirm successful initialization of the DB in terminal
    print('The DB has been successfully initialized.')

def updateDB(id, gs, score, tsec, date):
    '''
    Updates the database with a new row.
    '''
    try:
        # Connect with the DB.
        db = sqlite3.connect('scores.db')

        # Create the cursor.
        cursor = db.cursor()

        print('insert row')
        cursor.execute('''
            INSERT INTO scores
            (string, number)
            VALUES (?, ?, ?, ?, ?)
        ''')

        print('commit')
        db.commit()


        db.close()
        # Confirm update initialization of the DB in terminal.
        print('The DB has been successfully initialized.')
    # Error handling.
    except sqlite3.Error as error:
        print("Failed to update the database.", error)


# Initialize the database.
#initDB()

'''
def insertVaribleIntoTable(id, name, email, joinDate, salary):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          (id, name, email, joining_date, salary) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (id, name, email, joinDate, salary)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

insertVaribleIntoTable(2, 'Joe', 'joe@pynative.com', '2019-05-19', 9000)
insertVaribleIntoTable(3, 'Ben', 'ben@pynative.com', '2019-02-23', 9500)


'''
