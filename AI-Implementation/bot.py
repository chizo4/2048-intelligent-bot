'''
2048 GAME PROJECT: AI Bot.

Date created:
    03/2022

Date edited:
    05/2022

Author:
    Filip J. Cierkosz
'''

import random
import numpy as np
import pygame
from pygame.locals import *
from time import sleep, time
from graphics import *

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
        self.moves = ['right', 'left', 'up', 'down']
        self.GRID_SIZE = 5 
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.score = 0
        self.timer = 0

        # GUI adjustments.
        self.HEIGHT = 540
        self.WIDTH = 500
        self.TOP_SPACE = self.HEIGHT-self.WIDTH
        self.SPACE = 5
        self.SQUARE_SIZE = (self.WIDTH-(self.GRID_SIZE+1)*self.SPACE)/self.GRID_SIZE
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
    def update_arr(curr, self):
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
            # Otherwise, append a single number.
            else:
                new.append(temp[i])

        # Fill the rest of the array with zeros, so that it matches the size.
        while (len(new)!=len(curr)):
            new.append(0)

        return np.array(new)

    def draw(self):
        '''
        Draws the game window.

            Parameters:
                self
        '''
        self.window.fill((GRID_COLOR))

        # Iterate in order to display squares in the NxN grid.
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                x = (c+1)*self.SPACE+c*self.SQUARE_SIZE
                y = self.TOP_SPACE+(r+1)*self.SPACE+r*self.SQUARE_SIZE

                # Get the number from the cell to define its corresponding color.
                num = self.grid[r][c]
                
                # If a number on the grid is greater or equal to 2048, it will not
                # change anymore, since dictionary has colors up to 2048.
                if (num>=2048):
                    color = CELL_COLORS[2048]
                else:
                    color = CELL_COLORS[num]

                pygame.draw.rect(self.window,
                                color,
                                pygame.Rect(x,y,self.SQUARE_SIZE,self.SQUARE_SIZE),
                                border_radius=8)

                # Display numbers for each square. Do NOT draw zeros.
                if (num!=0):
                    text_area = self.font_game.render(f'{num}', True, GRID_FONT_COLOR)
                    self.window.blit(text_area, 
                                     text_area.get_rect(center=(x+self.SQUARE_SIZE/2, 
                                     y+self.SQUARE_SIZE/2)))

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
            if (self.grid[row][col]==0):
                available_coords.append((row, col))

        # Append the new value in the grid in random available position.
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

            # Update the row/column. Add any elements (if possible).
            new = self.update_arr(curr, self)

            # Update the grid for the move to the left or up.
            if (move=='left'):
                self.grid[i] = new
            elif (move=='up'):
                self.grid[:, i] = new

            # Update in the grid for the move to the right or down.
            # The updated array has to be reversed again, so that non-zero
            # elements are at the end of the new array.
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

        for mv in self.moves:
            self.make_move(mv)

            # Check if the grids are equal after invoking a move.
            equal = (self.grid==original).all()

            # If the grids are not equal, it means it is possible to continue.
            if (not equal):
                self.grid = original
                return False

        return True

    def set_timer(self):
        '''
        Sets the timer.

            Parameters:
                self

            Returns:
                start (time) : Started timer.
        '''
        start = time()
        return start

    def stop_timer(self, start):
        '''
        Stops the timer and returns the time of execution.

            Parameters:
                self
                start (time) : Started timer.

            Returns:
                executionTime (time) : Time of execution.
        '''
        stop = time()
        execution_time = stop-start
        return execution_time

    # STILL IN DEVELOPMENT STAGE!!!
    def search_move(self):
        '''
        AI bot searches the best move performing each of the available moves, then
        simulating future states of the game board. Finally, the best move is selected
        analyzing the costs (the higher the cost, the better the choice). The costs
        consist of such aspects as scores on the grid and empty spots.

            Parameters:
                self

            Returns:
                bestMv (st) : Selected best move for the current state of the
                              grid; either 'right', 'left', 'up', or 'down'.
        '''
        # Make a copy of the initial state of the grid.
        orig_grid = self.grid.copy()

        # Dictionary to calculate costs per each move, based on scores and empty spots.
        costs = {mv:0 for mv in self.moves}

        # Determine the number of searches per one move and the depth of the search.
        searches_mv = 100
        depth = 10
        #searchesMv = 64
        #depth = 16

        # Test each available move.
        for mv in self.moves:
            # Execute the move, check if possible to continue and get the score.
            self.make_move(mv)
            game_over_mv = self.check_if_over()
            score_mv = np.max(self.grid)

            # If the game is not over and the move changes the state of the board,
            # insert new number, update scores, and perform the further search.
            if (not game_over_mv and not (self.grid==orig_grid).all()):
                self.insert_new_num()
                costs[mv] += score_mv
                counter_mv = 1
            # Otherwise, restart the grid to the initial state and move to the next move.
            else:
                self.grid = orig_grid.copy()
                continue

            # Perform simulation of later moves.
            for i in range(searches_mv):
                search_board = self.grid.copy()
                game_over = False

                while (not game_over and counter_mv<depth):
                    search_board = self.grid.copy()
                    # Execute a random move.
                    self.make_move(self.shuffle_move())
                    game_over = self.check_if_over()
                    simulated_score = np.max(self.grid)

                    if (not game_over and not (self.grid==search_board).all()):
                        self.insert_new_num()
                        costs[mv] += simulated_score
                        counter_mv += 1

                # Increment the costs by the number of empty spots in the current state of grid.
                costs[mv] += 100*np.count_nonzero(self.grid==0)
            
            # Restart the grid to the initial state for the next move to be tested.
            self.grid = orig_grid.copy()

        # Finally, restart the grid to the initial state one last time.
        self.grid = orig_grid.copy()

        # Find and return the best searched move.
        best_mv = max(costs, key=costs.get)
        return best_mv
        
    def shuffle_move(self):
        '''
        Shuffles a random move.

            Parameters:
                self

            Returns:
                randMv : One randomly selected move; either 'right', 'left',
                         'up', or 'down'.
        '''
        return np.random.choice(self.moves, 1)

    def play(self):
        '''
        Main method to play the game.

            Parameters:
                self

            Returns:
             True/False (boolean) : True if game is won, False otherwise.
        '''
        # Initialize the board, with 2 starting numbers in the grid.
        self.insert_new_num(n=2)
        start = self.set_timer()

        # Play as long as the game is neither over, nor won by the AI bot.
        while (True):
            self.draw()
            self.update_score()
            text_area = self.font_score.render(f'SCORE: {self.score:06d}',
                                               True, WINDOW_FONT_COLOR)
            self.window.blit(text_area, text_area.get_rect(center=(115,20)))
            pygame.display.flip()

            # If the AI bot reaches the goal state, i.e. score: 2048, it denotes win.
            if (self.score==16384):
                self.window.fill((GRID_COLOR))
                self.timer = self.stop_timer(start)

                # Display the final message.
                text_area = self.font_msg.render(f'BOT WON THE GAME!', 
                                                 True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                text_area = self.font_msg.render(f'TIME PLAYED: {self.timer:.1f} SEC', 
                                                 True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))
                pygame.display.flip()

                # Wait 1 second to display the final screen.
                sleep(1)
                return True

            # Make a copy of the old grid.
            old_grid = self.grid.copy()

            # Determine the best AI-searched move and execute it
            mv = self.search_move()
            self.make_move(mv)
            
            if (self.check_if_over()):
                self.window.fill((GRID_COLOR))
                self.timer = self.stop_timer(start)

                # Display the final message.
                text_area = self.font_msg.render(f'BOT LOST.', 
                                                 True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                text_area = self.font_msg.render(f'TIME PLAYED: {self.timer:.1f} SEC', 
                                                 True, WINDOW_FONT_COLOR)
                self.window.blit(text_area, 
                                 text_area.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))
                pygame.display.flip()

                # Delay 1 second to display the final screen.
                sleep(1)
                return False

            if (not (self.grid==old_grid).all()):
                self.insert_new_num()
