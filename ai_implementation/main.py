'''
2048 GAME PROJECT: Main program.

Date created:
    04/2022

Author:
    Filip J. Cierkosz
'''

# TODO: fix the bot so that it solves the 4x4 grid. set up tests to run the bot. collect the results in db. analyze efficiency with notebook.

from bot.bot import GameBot
from db.scores import init_db

def main():
    bot = GameBot()
    # uncomment to play
    bot.play() 
    print(bot.score)

    # testing
    #init_db()


if (__name__=='__main__'):
    main()