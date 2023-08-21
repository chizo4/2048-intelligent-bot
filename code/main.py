'''
code/main.py

2048-intelligent-bot: Main program for running AI bot.

Author: Filip J. Cierkosz 2022 (updated: 2023)
'''


from bot.bot import Bot
from db.db_tools import init_db, update_db
from datetime import datetime


def run_bot():
    '''
    Main method to perform one sample run of the AI bot
    and storing the results in DB.
    '''
    bot = Bot()
    bot.play()
    now = datetime.now()
    update_db(
        win=bot.win,
        score=int(bot.score),
        t_sec=bot.timer,
        date=now.strftime('%d %b %Y %I:%M:%S %p')
    )

def run_tests():
    '''
    Performs 100 sample runs of the AI bot and stores 
    the results in the initialized database. 

    NB: Takes several hours to complete!
    '''
    for _ in range(100):
        run_bot()


if __name__=='__main__':
    # Run only to initialize or reset the database.
    # init_db()

    # Run one sample of the AI bot.
    run_bot()

    # Uncomment below to run 100 samples.
    # run_tests()
