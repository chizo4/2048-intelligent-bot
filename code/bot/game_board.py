'''
code/bot/game_board.py

2048-intelligent-bot: Basis for the 2048 game board used by bot.

Author: Filip J. Cierkosz 2022 (updated: 2023)

(NB: The class does nothing in particular on its own!)
'''


import random
import numpy as np
import pygame
from pygame.locals import *
from time import time
from bot.graphics import *


class GameBoard:
    '''
    -----------
    Class to initialize a 2048 game board. 
    -----------
    '''

    def __init__(self):
        '''
        Constructor to initialize an appropriately-sized grid for the game with all attributes.

            Parameters:
                self
        '''
        self.GRID_SIZE = 4
        self.MOVES = ['right', 'left', 'up', 'down']

        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.score = 0
        self.timer = 0
        self.win = 0

        # Pygame GUI settings.
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
            FONT_SIZES['final_msg'],
            FONT_BOARD[1]
        )

    @staticmethod
    def update_arr(curr):
        '''
        Returns an updated array for row/column of the grid.

            Parameters:
                self
                cur (np.array) : Array of numbers in the current state of column/row.

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

    def update_score(self):
        '''
        Updates the score. The score is denoted by the single max value in the grid.

            Parameters:
                self
        '''
        self.score = np.max(self.grid)

    def draw(self):
        '''
        Draws the initialized game window.

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
                color = CELL_COLORS[2048] if num >= 2048 else CELL_COLORS[num]

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
                        text_area.get_rect(center=(x + self.SQUARE_SIZE / 2, y + self.SQUARE_SIZE / 2))
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
        Makes a move on the board (based on bot decision).

        If moving to the left/right - check the rows of the grid.
        If moving up/down - check the columns.

            Parameters:
                self
                move (str) : String describing the user's move (one from self.MOVES).
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
                True/False (bool) : True if over; False otherwise.
        '''
        original = self.grid.copy()

        for mv in self.MOVES:
            self.make_move(mv)

            if not (self.grid == original).all():
                self.grid = original
                return False

        return True

    def shuffle_move(self):
        '''
        Shuffles a random move (either: 'right', 'left', 'up', or 'down').

            Parameters:
                self

            Returns:
                (str) : Randomly selected move.
        '''
        return np.random.choice(self.MOVES, 1)

    def set_timer(self):
        '''
        Sets the timer for a game attempt.

            Parameters:
                self
            
            Returns:
                (time) : Current time.
        '''
        return time()

    def stop_timer(self, start):
        '''
        Stops the timer after a game attempt.

            Parameters:
                self
                start : Start time of the game attempt.
            
            Returns:
                (time) : Attempt time (delta).
        '''
        return time() - start

    def play(self):
        '''
        Main method to initialize the game board window.

            Parameters:
                self
        '''
        try:
            while True:
                self.draw()
        except KeyboardInterrupt:
            print('\nCtrl+C detected. Exiting the game...\n')
