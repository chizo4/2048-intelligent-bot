'''
main.py

2048 GAME PROJECT: Main program.

Date created:
    04/2022

Author:
    Filip J. Cierkosz
'''

from bot.bot import GameBot
from db.bot_records_setup import init_db, update_db
from datetime import datetime

def main():
    '''
    Main method to perform one sample run of the AI bot 
    and store the result in the databse.
    '''
    bot = GameBot()
    bot.play()

def run_tests():
    '''
    Performs 500 sample runs of the AI bot and stores 
    the results in the initialized database. 

    NB: Takes several hours to complete!
    '''
    for _ in range(500):
        bot = GameBot()
        bot.play()
        now = datetime.now()
        update_db(win=bot.is_win(),
                score=int(bot.get_score()),
                t_sec=bot.get_time(),
                date=now.strftime('%d %b %Y %I:%M:%S %p'))

if (__name__=='__main__'):
    # Run only to initialize or reset the database.
    #init_db()
    # Uncomment to run one sample.
    #main()
    # Uncomment to run 200 samples.
    run_tests()
