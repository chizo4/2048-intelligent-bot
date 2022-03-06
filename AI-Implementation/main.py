'''
2048 GAME PROJECT: Main program for the game (AI).

Date created:
    03/2022

Author:
    Filip J. Cierkosz
'''

from gameBoard import Game2048

def main():
    '''
    Main method to execute the game for AI bot.
    '''
    game = Game2048()
    game.play()


# Run the main program.
if (__name__=='__main__'):
    main()
