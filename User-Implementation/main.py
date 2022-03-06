'''
2048 GAME PROJECT: Main program for the game.

Date created:
    02/2022

Date edited:
    03/2022

Author:
    Filip J. Cierkosz
'''

from gameBoard import Game2048
from gridSelection import GridSelectionWindow
from scores import updateDB, countDBRows
from datetime import datetime

def main():
    '''
    Main method to execute the game and all related methods.
    '''
    # Initialize the grid selection windows. Collect user's responses.
    selection = GridSelectionWindow()
    selection.promptUser()
    gridSize = int(selection.getResponse())
    initGame = selection.playGame
    
    # If the user intializes the game, initialize the game window and play.
    if (initGame):
        game = Game2048(gridSize)
        game.play()

        # Create a datetime object of the current time.
        now = datetime.now()

        # Update the database with a new row with the latest data.
        updateDB(id=countDBRows(),
                 gs=game.getGridSize(),
                 sc= int(game.getScore()),
                 tsec=game.getTime(),
                 dt=now.strftime('%d %b %Y %I:%M:%S %p'))

# Run the main program.
if (__name__=='__main__'):
    main()
