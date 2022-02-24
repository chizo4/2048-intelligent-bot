'''
2048 GAME PROJECT: Main program for the game.

Date created:
    02/2022

Author:
    Filip J. Cierkosz
'''

from graphics import GRID_COLOR, CELL_COLORS, GRID_FONT_COLOR, FONT_BOARD, FONT_SIZES, USER_FONT_COLOR, WINDOW_FONT_COLOR
from bestScoresFunc import updateDatafile, getCurrBestScore
from gridSelection import GridSelectionWindow
from gameBoard import Game2048

if (__name__=='__main__'):
    # Create an instance of the grid selection class.
    selection = GridSelectionWindow()

    # Prompt the user for the grid size.
    selection.promptUser()

    # Record the user responses.
    gridSize = int(selection.response)
    initGame = selection.playGame
    
    if (initGame):
        # Create an instance of the game class.
        game = Game2048(gridSize)

        # Invoke the method to play the game.
        game.play()

        # Get the user's score.
        score = game.score

        # TESTING: timer
        timePlayed = game.timer

        print(f'{timePlayed}')

        # Invoke the function to update score. It will be updated
        # if the user beats the current best score.
        updateDatafile('bestScores.csv', gridSize, score)
