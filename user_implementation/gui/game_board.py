'''
2048 GAME PROJECT: 2048 game board.

Date created: 
    11/2021

Date edited:
    06/2022

Author:
    Filip J. Cierkosz
'''

import random
import numpy as np
import pygame
from pygame.locals import *
from time import sleep, time
from gui.graphics import *
from db.scores import get_grid_best_score

class Game2048:
    '''
    -----------
    Class to create a game board for 2048. 
    -----------
    '''
    def __init__(self, gs):
        '''
        Constructor to initialize an appropriately-sized grid for the game with all attributes.

            Parameters:
                self
                gs (int) : Grid size of the game board.
        '''
        # Set the grid size according to the user response.
        self.GRID_SIZE = gs
        self.HEIGHT = 540
        self.WIDTH = 500
        self.TOP_SPACE = self.HEIGHT-self.WIDTH
        self.SPACE = 5
        self.SQUARE_SIZE = (self.WIDTH-(self.GRID_SIZE+1)*self.SPACE)/self.GRID_SIZE
        self.score = 0
        self.timer = 0
        self.curr_best_score = get_grid_best_score(gs)
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        pygame.init()
        pygame.display.set_caption("2048: GAME")
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.font.init()
        self.font_game = pygame.font.SysFont(FONT_BOARD[0], 
                                            FONT_SIZES[f'{self.GRID_SIZE}'], 
                                            FONT_BOARD[1])
        self.font_score = pygame.font.SysFont(FONT_BOARD[0],
                                             FONT_SIZES['score'], 
                                             FONT_BOARD[1])
        self.font_msg = pygame.font.SysFont(FONT_BOARD[0],
                                           FONT_SIZES['finalMsg'],
                                           FONT_BOARD[1])

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
        temp = [n for n in curr if (n!=0)]
        new = []
        skip = False

        for i in range(len(temp)):
            # Skip an element that was just added (so that it is not repeated).
            if (skip):
                skip = False
                continue
            # If two consecutive elements are equal, add them and append in new.
            if (i!=len(temp)-1 and temp[i]==temp[i+1]):
                skip = True
                new.append(2*temp[i])
            else:
                new.append(temp[i])

        # Fill the rest of the array with zeros, so that it matches the size.
        while (len(new)!=len(curr)):
            new.append(0)

        return np.array(new)

    @staticmethod
    def listen_for_key_press():
        '''
        Listens for the user keyboard press.
                
            Returns:
                str : User's response on keyboard.
        '''
        while (True):
            for event in pygame.event.get():
                if (event.type==QUIT):
                    return 'stop' 
                if (event.type==KEYDOWN):
                    if (event.key==K_LEFT):
                        return 'left'
                    elif (event.key==K_RIGHT):
                        return 'right'
                    elif (event.key==K_UP):
                        return 'up'
                    elif (event.key==K_DOWN):
                        return 'down'
                    elif (event.key==K_q or event.key==K_ESCAPE):
                        return 'stop'

    def draw(self):
        '''
        Draws the game window.

            Parameters:
                self
        '''
        self.window.fill((GRID_COLOR))

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                x = (c+1)*self.SPACE+c*self.SQUARE_SIZE
                y = self.TOP_SPACE+(r+1)*self.SPACE+r*self.SQUARE_SIZE
                num = self.grid[r][c]
                
                # If a number on the grid is greater or equal to 2048, it will not
                # change anymore, since dictionary has colors up to the value of 2048.
                if (num>=2048):
                    color = CELL_COLORS[2048]
                else:
                    color = CELL_COLORS[num]

                pygame.draw.rect(self.window, color,
                                pygame.Rect(x,y,self.SQUARE_SIZE,self.SQUARE_SIZE),
                                border_radius=8)

                # Display numbers for each square. Do NOT draw zeros.
                if (num!=0):
                    text_area = self.font_game.render(f'{num}', True, GRID_FONT_COLOR)
                    self.window.blit(text_area, 
                                     text_area.get_rect(center=(x+self.SQUARE_SIZE/2, y+self.SQUARE_SIZE/2)))

    def insert_new_num(self, n=1):
        '''
        Updates a grid with a new number.

        Probability rates for values: 4 (5%), 2 (20%), 1 (75%)

            Parameters:
                self
                n=1 (int) : Quantity of new numbers to append.
        '''
        available_coords = []

        for row, col in np.ndindex(self.grid.shape):
            if (self.grid[row][col]==0):
                available_coords.append((row, col))

        # Append the new value in the grid according to probabilities.
        for c in random.sample(available_coords, k=n):
            if (random.random()<0.05):
                self.grid[c] = 4
            elif (random.random()<0.2):
                self.grid[c] = 2
            else:
                self.grid[c] = 1

    def make_move(self, move):
        '''
        Makes a move on the board based on the user keyboard press.

        If you wish to move to the left/right, look at the rows of the grid.
        If you wish to move up/down, look at the columns.

                Parameters:
                    self
                    move (str) : String describing the user's move.
        '''
        for i in range(self.GRID_SIZE):
            # Move to the LEFT. Define the row.
            if (move=='left'):
                curr = self.grid[i]
            # Move to the RIGHT. Define the reversed row.
            elif (move=='right'):
                curr = self.grid[i][::-1]
            # Move UP. Define the column.
            elif (move=='up'):
                curr = self.grid[:, i]
            # Move DOWN. Define the reversed column.
            elif (move=='down'):
                curr = self.grid[:, i][::-1]

            new = self.update_arr(curr)

            if (move=='left'):
                self.grid[i] = new
            elif (move=='up'):
                self.grid[:, i] = new
            elif (move=='right'):
                self.grid[i] = new[::-1]
            elif (move=='down'):
                self.grid[:, i] = new[::-1]

    def update_score(self):
        '''
        Updates the score. 
        
        The score is denoted by the maximum value in the grid.

            Parameters:
                self
        '''
        self.score = np.max(self.grid)

    def check_if_over(self):
        '''
        Checks if the game is over.

            Parameters:
                self

            Returns:
                True/False (boolean) : True if game is over; False otherwise.
        '''
        original = self.grid.copy()
        moves = ['right', 'left', 'up', 'down']

        for mv in moves:
            self.make_move(mv)

            # If grids not equal, then possible to continue.
            if (not (self.grid==original).all()):
                self.grid = original
                return False

        return True

    # Returns the score of the game.
    get_score = lambda self: self.score

    # Returns the time elapsed while playing the game.
    get_time = lambda self: self.timer

    # Returns the current size of the grid.
    get_grid_size = lambda self: self.GRID_SIZE
    
    # Sets the timer.
    set_timer = lambda self: time()

    # Stops the timer and returns the time of execution.
    stop_timer = lambda self, start: time()-start

    def play(self):
        '''
        Main method to play the game, initialized with 2 
        values in the grid.

            Parameters:
                self
        '''
        self.insert_new_num(n=2)
        start = self.set_timer()

        # Play as long as the game is neither over, nor quit by the user.
        while (True):
            self.draw()
            self.update_score()
            text_area = self.font_score.render(f'SCORE: {self.score:06d}', True, WINDOW_FONT_COLOR)
            self.window.blit(text_area, text_area.get_rect(center=(115,20)))
            pygame.display.flip()

            kbd_user_response = self.listen_for_key_press()

            # The game stops if the user triggers 'q' or escape the game.
            if (kbd_user_response=='stop'):
                break

            old_grid = self.grid.copy()
            self.make_move(kbd_user_response)
            
            if (self.check_if_over()):
                self.window.fill((GRID_COLOR))
                self.timer = self.stop_timer(start)
                text_area = self.font_msg.render('GAME OVER!', True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-120)))
                text_area = self.font_msg.render(f'TIME PLAYED: {self.timer:.1f} SEC', 
                                                 True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                text_area = self.font_msg.render(f'YOUR SCORE: {self.score}', True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))

                # Notice to the user if the best score was beaten.
                if (self.score>int(self.curr_best_score)):
                    text_area = self.font_msg.render(f'NEW BEST SCORE: {self.score}', 
                                                     True, USER_FONT_COLOR)
                    self.window.blit(text_area,
                                     text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+90)))
                else:
                    text_area = self.font_msg.render(f'BEST SCORE: {self.curr_best_score}', 
                                                     True, WINDOW_FONT_COLOR)
                    self.window.blit(text_area, 
                                     text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+90)))
                
                # Update the final screen and display it for 3 seconds before exiting.
                pygame.display.flip()
                sleep(3)
                break

            if (not (self.grid==old_grid).all()):
                self.insert_new_num()
