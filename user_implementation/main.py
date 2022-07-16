'''
main.py

2048 GAME PROJECT: Main program for the game.

Date created:
    02/2022

Date edited:
    07/2022

Author:
    Filip J. Cierkosz
'''

from gui.game_board import Game2048
from gui.grid_selection import GridSelectionWindow
from db.scores import update_db, count_db_rows
from datetime import datetime

def main():
    '''
    Main method to run the game instance.
    '''
    # Initialize the grid selection windows; collect user's responses.
    selection = GridSelectionWindow()
    selection.prompt_user()
    grid_size = int(selection.get_response())
    init_game = selection.play_game
    
    # Initialze the game.
    if (init_game):
        game = Game2048(grid_size)
        game.play()
        now = datetime.now()
        update_db(
            id=count_db_rows(),
            gs=game.get_grid_size(),
            sc= int(game.get_score()),
            tsec=game.get_time(),
            dt=now.strftime('%d %b %Y %I:%M:%S %p')
        )

if (__name__=='__main__'):
    # Run only if needed to initialize or reset the database.
    # init_db()
    
    # Play the game...
    main()
