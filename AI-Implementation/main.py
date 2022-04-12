'''
2048 GAME PROJECT: Main program.

Date created:
    04/2022

Author:
    Filip J. Cierkosz
'''

from bot import GameBot

def main():
    '''
    Run an instance of the bot.
    '''
    bot = GameBot()
    bot.play()

if (__name__=='__main__'):
    main()