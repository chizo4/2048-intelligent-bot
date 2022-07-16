'''
main.py

2048 GAME PROJECT: Main program for running AI.

Date created:
    04/2022

Date edited:
    07/2022

Author:
    Filip J. Cierkosz
'''

from bot.bot import GameBot
from db.bot_records_setup import init_db, update_db
from datetime import datetime

def run_bot():
    '''
    Main method to perform one sample run of the AI bot
    and storing the results in DB.
    '''
    bot = GameBot()
    bot.play()
    now = datetime.now()
    update_db(
        win=bot.is_win(),
        score=int(bot.get_score()),
        t_sec=bot.get_time(),
        date=now.strftime('%d %b %Y %I:%M:%S %p')
    )

def run_tests():
    '''
    Performs 500 sample runs of the AI bot and stores 
    the results in the initialized database. 

    NB: Takes several hours to complete!
    '''
    for _ in range(500):
        run_bot()
        

if (__name__=='__main__'):
    # Run only to initialize or reset the database.
    # init_db()

    # Run one sample of the AI bot.
    run_bot()

    # Uncomment to run 500 samples.
    # run_tests()
