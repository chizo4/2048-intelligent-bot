'''
code/bot/bot.py

2048-intelligent-bot: AI bot implementation (more info in README.md).

Author: Filip J. Cierkosz 2022 (updated: 2023)
'''


import numpy as np
import pygame
from pygame.locals import *
from bot.game_board import GameBoard
from bot.graphics import *


class Bot(GameBoard):
    '''
    -----------
    Class to create an AI bot instance that solves 2048.
    -----------
    '''

    def __init__(self):
        '''
        Constructor to initialize the bot (and game GUI through parent class).

            Parameters:
                self
        '''
        super().__init__()

        # Constant coefficient for dynamic search.
        self.SEARCH_PER_MOVE_COEFF = 10
        self.SEARCH_DEPTH_COEFF = 4
        self.SEARCH_COEFF = 200
        self.EMPTY_SPOT_COEFF = 10

        # Dictionary for calculating costs while searching.
        self.costs = {mv: 0 for mv in self.MOVES}

        self.searches_per_move = 0
        self.search_depth = 0
        self.move_num = 0

    def update_costs(self, move, score):
        '''
        Updates the cost using score sum and the heuristics for counting empty
        spots in the grid.

            Parameters:
                self
                move (str)  : Current move.
                score (int) : Score sum for the current move after simulations.
        '''
        self.costs[move] += score
        self.costs[move] += self.EMPTY_SPOT_COEFF * np.count_nonzero(self.grid == 0)

    def update_search_params(self):
        '''
        Dynamically update the values for search expansion. The further stage 
        of the game, the deeper the expansion of the game tree (search tree).

            Parameters:
                self
        '''
        self.search_depth = self.SEARCH_DEPTH_COEFF * (1 + (self.move_num // self.SEARCH_COEFF))
        self.searches_per_move = self.SEARCH_PER_MOVE_COEFF * (1 + (self.move_num // self.SEARCH_COEFF))
    
    def select_best_move(self):
        '''
        Selects the best move after full run of simulations. The best move
        is denoted by the max costs in the costs dictionary.

            Parameters:
                self

            Returns:
                (str) : Name of the most optimal move.
        '''
        if all(val == 0 for val in self.costs.values()):
            return self.shuffle_move()
        
        return max(self.costs, key=self.costs.get)

    def simulate_move(self):
        '''
        Simulates the future state of the game for a given move.

            Parameters:
                self
            
            Returns:
                total_score (int) : Total score obtained in the simulations.
        '''
        counter = 1
        total_score = 0
        game_over = False

        while counter < self.search_depth and not game_over:
            prev_simulated_grid = self.grid.copy()
            random_move = self.shuffle_move()
            self.make_move(random_move)

            # State of the game after random move.
            new_simulated_score = self.score
            game_over = self.check_if_over()
            diff_random_move = (not np.array_equal(self.grid, prev_simulated_grid))

            if not game_over and diff_random_move:
                self.insert_new_num()
                counter += 1
                total_score += new_simulated_score

        return total_score

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
                self.update_costs(first_move, score_first_move)
            else:
                continue

            # Simulate the future state of the game for the current first move.
            for _ in range(self.searches_per_move):
                self.grid = search_board_after_first_insert.copy()
                total_score = self.simulate_move()

                # Update the costs after simulation.
                self.update_costs(first_move, total_score)

            self.grid = original_grid.copy()

        # Find the best (most optimal) move denoted by highest cost.
        best_move = self.select_best_move()

        # Reset the grid and the dictionary to their original states.
        self.grid = original_grid.copy()
        self.costs = {mv: 0 for mv in self.MOVES}

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
                    self.timer = self.stop_timer(start)
                    self.win = 1
                    self.draw_win_screen()
                    return

                # Perform search for the next move.
                old_grid = self.grid.copy()
                next_move = self.search_move()

                # Peform the most optimal move.
                self.make_move(next_move)
                self.move_num += 1

                # Case: BOT LOSS.
                if self.check_if_over():
                    self.timer = self.stop_timer(start)
                    self.draw_loss_screen()
                    return

                if not (self.grid == old_grid).all():
                    # Update the search-related params and insert new number.
                    self.update_search_params()
                    self.insert_new_num()
        except KeyboardInterrupt:
            print('\nCtrl+C detected. Exiting the game...\n')
