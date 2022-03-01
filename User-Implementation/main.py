'''
2048 GAME PROJECT: Main program for the game.

Date created:
    02/2022

Author:
    Filip J. Cierkosz
'''

from gameBoard import Game2048
from gridSelection import GridSelectionWindow
from scores import updateDB, countDBRows
from bestScoresFunc import updateDatafile
from datetime import datetime

def main():
    '''
    Main method to execute the game and related methods.
    '''
    # Create an instance of the grid selection class.
    selection = GridSelectionWindow()

    # Prompt the user for the grid size.
    selection.promptUser()

    # Record the user response.
    gridSize = int(selection.response)
    initGame = selection.playGame
    
    if (initGame):
        # Create an instance of the game class and play.
        game = Game2048(gridSize)
        game.play()

        # Create a datetime object of the current time.
        now = datetime.now()

        # Update the database inserting a new row with the newest data.
        updateDB(id=countDBRows(),
                 gs=game.getGridSize(),
                 sc= game.getScore(),
                 tsec=game.getTime(),
                 dt=now.strftime('%d %b %Y %I:%M:%S %p'))

        # TO BE DELETED
        # Invoke the function to update score. It will be updated
        # if the user beats the current best score.
        #updateDatafile('bestScores.csv', gridSize, score)

# Run the main program.
if (__name__=='__main__'):
    main()