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

        self.SEARCH_PER_MOVE_COEFF = 10
        self.SEARCH_DEPTH_COEFF = 4
        self.SEARCH_COEFF = 200
        self.EMPTY_SPOT_COEFF = 10

        self.searches_per_move = 0
        self.search_depth = 0
        self.move_num = 0

    def update_search_params(self):
        '''
        Dynamically update the values for search expansion. The further stage 
        of the game, the deeper the expansion of the game tree.

            Parameters:
                self
        '''
        self.searches_per_move = self.SEARCH_PER_MOVE_COEFF * (1 + (self.move_num // self.SEARCH_COEFF))
        self.search_depth = self.SEARCH_DEPTH_COEFF * (1 + (self.move_num // self.SEARCH_COEFF))

        print(f'self.searches_per_move : {self.searches_per_move}')
        print(f'self.move_num : {self.move_num}')
        print(f'self.search_depth : {self.search_depth}')


    def search_move(self):
        '''
        AI bot searches the most optimal path by simulating future states of the
        current grid for each of the four moves. The best move is selected
        analyzing the final costs, which are calculated considering consecutive
        max scores on board and empty spots multiplied by the constant.

            Parameters:
                self

            Returns:
                best_move (str) : Best searched move ('right'/'left'/'up'/'down').
        '''
        original_grid = self.grid.copy()
        costs = {mv: 0 for mv in self.MOVES}

        for first_move in self.MOVES:
            self.make_move(first_move)

            # State of the game after first move.
            score_first_move = np.max(self.grid)
            game_over_first_move = self.check_if_over()
            diff_first_move = (not (self.grid == original_grid).all())

            if not game_over_first_move and diff_first_move:
                self.insert_new_num()
                search_board_after_first_insert = self.grid.copy()

                # Update the costs for the current move.
                costs[first_move] += score_first_move
                costs[first_move] += self.EMPTY_SPOT_COEFF * np.count_nonzero(self.grid == 0)
            else:
                continue

            # Simulate the future state of the game for the current first move.
            for _ in range(self.searches_per_move):
                self.grid = search_board_after_first_insert.copy()
                counter = 1
                game_over = False

                while counter < self.search_depth and not game_over:
                    prev_simulated_grid = self.grid.copy()
                    random_move = self.shuffle_move()
                    self.make_move(random_move)

                    # State of the game after random move.
                    new_simulated_score = self.score
                    game_over = self.check_if_over()
                    diff_random_move = (not (self.grid == prev_simulated_grid).all())

                    if not game_over and diff_random_move:
                        self.insert_new_num()
                        counter += 1

                        # Update the costs for the current score in simulations.
                        costs[first_move] += new_simulated_score

                # Update the costs by the number of empty spots heuristics.
                costs[first_move] += self.EMPTY_SPOT_COEFF * np.count_nonzero(self.grid == 0)
            self.grid = original_grid.copy()

        # Find the best move (one with the highest costs).
        best_move = max(costs, key=costs.get)

        # Reset the grid to its original state.
        self.grid = original_grid.copy()

        if all(val == 0 for val in costs.values()):
            return self.shuffle_move()

        return best_move

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
                    sleep(1)
                    return True

                # Perform search for the next move.
                old_grid = self.grid.copy()
                next_move = self.search_move()

                # Make the move.
                self.make_move(next_move)
                self.move_num += 1

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
                    # Update the search-related params and insert new number.
                    self.update_search_params()
                    self.insert_new_num()
        except KeyboardInterrupt:
            print('\nCtrl+C detected. Exiting the game...\n')
