'''
2048 GAME PROJECT: Main program.

Date created:
    04/2022

Author:
    Filip J. Cierkosz
'''

from bot.bot import GameBot

def main():
    bot = GameBot()
    bot.play()
    print(bot.score)

if (__name__=='__main__'):
    main()