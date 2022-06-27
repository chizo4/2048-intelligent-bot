# test for 0, 4, 16, 64, 128
# 25 samples for each assignment

from bot.bot import GameBot

def run_test():
    #sample_costs = [0,4,16,64,128]
    sample_costs = [10]

    for sc in sample_costs:
        print(f'testing with costs constant : {sc}')
        for _ in range(20):
            bot = GameBot(sc)
            bot.play() 
            print(bot.score, end=', ')

        print('\n----------------------\n')

run_test()
