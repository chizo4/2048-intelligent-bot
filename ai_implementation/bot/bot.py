'''
ai_implementation/bot/bot.py

2048-Project: AI bot implementation (more info in README.md).

Author: Filip J. Cierkosz (2022)
'''


import random
import numpy as np
import pygame
from pygame.locals import *
from time import sleep, time
from bot.graphics_bot import *


class GameBot:
    '''
    -----------
    Class to create a game board for 2048 to be solved by an AI bot. 
    -----------
    '''

    def __init__(self):
        '''
        Constructor to initialize an appropriately-sized grid for the game with all attributes.

            Parameters:
                self
        '''
        self.EMPTY_SPOT_CONST = 10
        self.SEARCH_DEPTH = 12
        self.SEARCHES_PER_MV = 24
        self.moves = ['right', 'left', 'up', 'down']
        self.score = 0
        self.timer = 0
        self.win = 0
        self.GRID_SIZE = 4
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.HEIGHT = 540
        self.WIDTH = 500
        self.TOP_SPACE = self.HEIGHT - self.WIDTH
        self.SPACE = 5
        self.SQUARE_SIZE = (self.WIDTH - (self.GRID_SIZE + 1) * self.SPACE) / self.GRID_SIZE
        pygame.init()
        pygame.display.set_caption('2048: AI BOT')
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.font.init()
        self.font_game = pygame.font.SysFont(
            FONT_BOARD[0],
            FONT_SIZES[f'{self.GRID_SIZE}'],
            FONT_BOARD[1]
        )
        self.font_score = pygame.font.SysFont(
            FONT_BOARD[0],
            FONT_SIZES['score'],
            FONT_BOARD[1]
        )
        self.font_msg = pygame.font.SysFont(
            FONT_BOARD[0],
            FONT_SIZES['finalMsg'],
            FONT_BOARD[1]
        )

    def update_score(self):
        '''
        Updates the score. The score is denoted by the max value in the grid.

            Parameters:
                self
        '''
        self.score = np.max(self.grid)

    @staticmethod
    def update_arr(curr):
        '''
        Returns an updated array for row/column of the grid.

            Parameters:
                self
                cur (array) : Array of numbers in the current state of column/row.

            Returns:
                new (np.array) : Updated column/row to the grid.
        '''
        temp = [n for n in curr if (n != 0)]
        new = []
        skip = False

        for i in range(len(temp)):
            # Skip an element that was just added (so that it is not repeated).
            if skip:
                skip = False
                continue
            # If two consecutive elements are equal, add them and append in new.
            if (i != len(temp) - 1) and (temp[i] == temp[i + 1]):
                skip = True
                new.append(2 * temp[i])
            else:
                new.append(temp[i])

        while len(new) != len(curr):
            new.append(0)

        return np.array(new)

    def draw(self):
        '''
        Draws the game window.

            Parameters:
                self
        '''
        self.window.fill((GRID_COLOR))

        # Display squares in the NxN grid.
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                x = (c + 1) * self.SPACE + c * self.SQUARE_SIZE
                y = self.TOP_SPACE + (r + 1) * self.SPACE + r * self.SQUARE_SIZE
                num = self.grid[r][c]
                
                # If a number on the grid is greater or equal to 2048, it will not
                # change anymore, since dictionary has colors up to 2048.
                if num >= 2048:
                    color = CELL_COLORS[2048]
                else:
                    color = CELL_COLORS[num]

                pygame.draw.rect(
                    self.window,
                    color,
                    pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE),
                    border_radius=8
                )

                if num != 0:
                    text_area = self.font_game.render(
                        f'{num}',
                        True,
                        GRID_FONT_COLOR
                    )
                    self.window.blit(
                        text_area,
                        text_area.get_rect(
                            center=(x + self.SQUARE_SIZE / 2, y + self.SQUARE_SIZE / 2)
                        )
                    )

    def insert_new_num(self, n=1):
        '''
        Updates a grid with a new number.

        Probability rates for values: 2 (100%).

            Parameters:
                self
                n (int) : Quantity of new numbers to be inserted.
        '''
        available_coords = []

        for row, col in np.ndindex(self.grid.shape):
            if self.grid[row][col] == 0:
                available_coords.append((row, col))

        for c in random.sample(available_coords, k=n):
            self.grid[c] = 2

    def make_move(self, move):
        '''
        Makes a move on the board based on the AI choice.

        If you wish to move to the left/right, look at the rows of the grid.
        If you wish to move up/down, look at the columns.

            Parameters:
                self
                move (str) : String describing the user's move; either 'right',
                                'left', 'up', or 'down'.
        '''
        for i in range(self.GRID_SIZE):
            if move == 'left':
                curr = self.grid[i]
            elif move == 'right':
                curr = self.grid[i][::-1]
            elif move == 'up':
                curr = self.grid[:, i]
            elif move == 'down':
                curr = self.grid[:, i][::-1]

            new = self.update_arr(curr)

            if move == 'left':
                self.grid[i] = new
            elif move == 'up':
                self.grid[:, i] = new
            elif move == 'right':
                self.grid[i] = new[::-1]
            elif move == 'down':
                self.grid[:, i] = new[::-1]

    def check_if_over(self):
        '''
        Checks if the game is over.

            Parameters:
                self

            Returns:
                True/False (boolean) : True if game is over; False otherwise.
        '''
        original = self.grid.copy()

        for mv in self.moves:
            self.make_move(mv)

            if not (self.grid == original).all():
                self.grid = original
                return False

        return True

    def search_move(self):
        '''
        AI bot searchs the most optimal path by simulating future states of the
        current grid for each of the four moves. The best move is selected
        analyzing the final costs, which are calculated considering consecutive
        max scores on board and empty spots multiplied by the constant.

            Parameters:
                self

            Returns:
                best_mv (str) : best searched move ('right'/'left'/'up'/'down').
        '''
        original_grid = self.grid.copy()
        costs =  {mv: 0 for mv in self.moves}

        for first_mv in self.moves:
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
                    new_simulated_score = self.get_score()
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
        else:
            return best_mv
                    
    # Shuffles a random move (either: 'right', 'left', 'up', or 'down').
    shuffle_move = lambda self: np.random.choice(self.moves, 1)

    # Sets the timer.
    set_timer = lambda self: time()

    # Stops the timer and returns the time of execution.
    stop_timer = lambda self, start: time() - start

    # Returns boolean denoting if bot won the game.
    is_win = lambda self: self.win

    # Returns the score of the game.
    get_score = lambda self: self.score

    # Returns the time elapsed while playing the game.
    get_time = lambda self: self.timer

    def play(self):
        '''
        Main method to make the bot play the game.

            Parameters:
                self
        '''
        # Initialize the board, with 2 starting numbers in the grid.
        self.insert_new_num(n=2)
        start = self.set_timer()

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
                    f'BOT WON THE GAME!',
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
                    f'BOT LOST.',
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
