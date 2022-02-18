# CSV Datafile Adjustments
# Written by: Filip J. Cierkosz
# Date: 11/2021

import csv

# Function 1: Initialize/Reset the datafile.
def initDatafile(filename):
    # Open the file.
    with open(filename, 'w', encoding='UTF8', newline='') as file:
        # Insert all the data.
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    # Confirm the successful execution of the function.
    print('The datafile has been successfully initialized.')

# Function 2: Update the contents of the datafile.
def updateDatafile(filename, gs, score):
    update = False

    # Read-in the data.
    reader = csv.reader(open(filename))
    rows = list(reader)

    # Iterate to access the desired cell. Omit the first row (headers).
    for i in range(1, len(rows)):
        if (int(rows[i][0])==gs):
            if (int(rows[i][1])<score):
                rows[i][1] = f'{score}'
                update = True

                # Write-in the updated data into the datafile.
                writer = csv.writer(open('bestScores.csv', 'w'))
                writer = writer.writerows(rows)

                # Confirm the successful update.
                print('The datafile has been successfully updated.')

    # If there were no updates, also inform about this in the terminal.
    if (not update):
        print('There were no updates to the datafile.')

# Function 3: Get the current best score in a particular grid.
def getCurrBestScore(filename, gs):
    # Read-in the data.
    reader = csv.reader(open(filename))
    rows = list(reader)

    # Iterate through the rows. Find the best score for a particular
    # grid and return it. Omit the first row (headers).
    for i in range(1, len(rows)):
        if (int(rows[i][0])==gs):
            return rows[i][1]

# Array of headers.
headers = ['GRID SIZE', 'BEST SCORE']

# Dictionary with the data to initialize the datfile.
data = [
    {'GRID SIZE': 3, 'BEST SCORE': 0},
    {'GRID SIZE': 4, 'BEST SCORE': 0},
    {'GRID SIZE': 5, 'BEST SCORE': 0},
    {'GRID SIZE': 6, 'BEST SCORE': 0}
]

# Initialize the datafile.
#initDatafile('bestScores.csv')
