'''
2048 GAME PROJECT: Main program for the game.

Date created:
    02/2022

Date edited:
    03/2022

Author:
    Filip J. Cierkosz
'''

from game_board import Game2048
from grid_selection import GridSelectionWindow
from scores import update_db, count_db_rows
from datetime import datetime

def main():
    '''
    Main method to execute the game and all related methods.
    '''
    # Initialize the grid selection windows. Collect user's responses.
    selection = GridSelectionWindow()
    selection.prompt_user()
    grid_size = int(selection.get_response())
    init_game = selection.play_game
    
    if (init_game):
        game = Game2048(grid_size)
        game.play()
        now = datetime.now()

        # Update the database with a new row with the latest data.
        update_db(id=count_db_rows(),
                  gs=game.get_grid_size(),
                  sc= int(game.get_score()),
                  tsec=game.get_time(),
                  dt=now.strftime('%d %b %Y %I:%M:%S %p'))

# Run the main program.
if (__name__=='__main__'):
    main()
