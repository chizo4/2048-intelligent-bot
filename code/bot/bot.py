'''
code/bot/bot.py

2048-intelligent-bot: AI bot implementation (more info in README.md).

Author: Filip J. Cierkosz 2022 (updated: 2023)
'''


from time import sleep
import numpy as np
import pygame
from pygame.locals import *
from bot.game_board import GameBoard
from bot.graphics import *


class Bot(GameBoard):
    '''
    -----------
    Class to create an AI bot instance to solve 2048.
    -----------
    '''

    def __init__(self):
        '''
        Constructor to initialize the bot and game board (through parent class).

            Parameters:
                self
        '''
        super().__init__()

        # Search-related constants.
        self.EMPTY_SPOT_CONST = 10
        self.SEARCH_DEPTH = 12
        self.SEARCHES_PER_MV = 24

    def search_move(self):
        '''
        AI bot searches the most optimal path by simulating future states of the
        current grid for each of the four moves. The best move is selected
        analyzing the final costs, which are calculated considering consecutive
        max scores on board and empty spots multiplied by the constant.

            Parameters:
                self

            Returns:
                best_mv (str) : Best searched move ('right'/'left'/'up'/'down').
        '''
        original_grid = self.grid.copy()
        costs =  {mv: 0 for mv in self.MOVES}

        for first_mv in self.MOVES:
            self.make_move(first_mv)
            game_over_first_mv = self.check_if_over()
            score_first_mv = np.max(self.grid)

            if (not game_over_first_mv) and (not (self.grid == original_grid).all()):
                self.insert_new_num()
                costs[first_mv] += score_first_mv
                search_board_after_first_insert = self.grid.copy()
            else:
                continue

            for _ in range(self.SEARCHES_PER_MV):
                counter = 1
                self.grid = search_board_after_first_insert.copy()
                game_over = False

                while counter < self.SEARCH_DEPTH and not game_over:
                    random_mv = self.shuffle_move()
                    prev_simulated_grid = self.grid.copy()
                    self.make_move(random_mv)
                    new_simulated_score = self.score
                    game_over = self.check_if_over()

                    if not game_over and not (self.grid == prev_simulated_grid).all():
                        self.insert_new_num()
                        costs[first_mv] += new_simulated_score
                        counter += 1
                costs[first_mv] += self.EMPTY_SPOT_CONST * np.count_nonzero(self.grid == 0)
            self.grid = original_grid.copy()

        # Find the best move (one with the highest costs).
        best_mv = max(costs, key=costs.get)
        # Reset the grid to its original state.
        self.grid = original_grid.copy()

        if all(val == 0 for val in costs.values()):
            return self.shuffle_move()

        return best_mv

    def play(self):
        '''
        Main method to make the bot play the game.

            Parameters:
                self
        '''
        # Initialize the board, with 2 starting numbers in the grid.
        self.insert_new_num(n=2)
        start = self.set_timer()

        try:
            # Play as long as the game is neither over, nor won by the AI bot.
            while True:
                self.draw()
                self.update_score()
                text_area = self.font_score.render(
                    f'SCORE: {self.score:06d}',
                    True,
                    WINDOW_FONT_COLOR
                )
                self.window.blit(
                    text_area,
                    text_area.get_rect(center=(115, 20))
                )
                pygame.display.flip()

                # Case: BOT WIN.
                if self.score == 2048:
                    self.window.fill((GRID_COLOR))
                    self.timer = self.stop_timer(start)
                    text_area = self.font_msg.render(
                        'BOT WON THE GAME!',
                        True,
                        WINDOW_FONT_COLOR
                    )
                    self.window.blit(
                        text_area,
                        text_area.get_rect(
                            center=(self.WIDTH / 2, self.HEIGHT / 2 - 50)
                        )
                    )
                    text_area = self.font_msg.render(
                        f'TIME PLAYED: {self.timer:.1f} SEC',
                        True,
                        WINDOW_FONT_COLOR
                    )
                    self.window.blit(
                        text_area,
                        text_area.get_rect(
                            center=(self.WIDTH / 2, self.HEIGHT / 2 + 20)
                        )
                    )
                    pygame.display.flip()
                    self.win = 1
                    sleep(0.5)
                    return True

                old_grid = self.grid.copy()
                next_move = self.search_move()
                self.make_move(next_move)

                # Case: BOT LOSS.
                if self.check_if_over():
                    self.window.fill((GRID_COLOR))
                    self.timer = self.stop_timer(start)
                    text_area = self.font_msg.render(
                        'BOT LOST.',
                        True,
                        WINDOW_FONT_COLOR
                    )
                    self.window.blit(
                        text_area,
                        text_area.get_rect(
                            center=(self.WIDTH / 2, self.HEIGHT / 2 - 50)
                        )
                    )
                    text_area = self.font_msg.render(
                        f'TIME PLAYED: {self.timer:.1f} SEC',
                        True,
                        WINDOW_FONT_COLOR
                    )
                    self.window.blit(
                        text_area,
                        text_area.get_rect(
                            center=(self.WIDTH / 2, self.HEIGHT / 2 + 20)
                        )
                    )
                    pygame.display.flip()
                    sleep(1)
                    return False

                if not (self.grid == old_grid).all():
                    self.insert_new_num()
        except KeyboardInterrupt:
            print('\nCtrl+C detected. Exiting the game...\n')
