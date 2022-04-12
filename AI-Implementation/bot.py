'''
2048 GAME PROJECT: AI Bot.

Date created:
    03/2022

Date edited:
    04/2022

Author:
    Filip J. Cierkosz
'''

import random
import numpy as np
import pygame
from pygame.locals import *
from time import sleep, time
from graphics import GRID_COLOR, CELL_COLORS, GRID_FONT_COLOR, FONT_BOARD, FONT_SIZES, WINDOW_FONT_COLOR

class GameBot:
    '''
    -----------
    Class to create a game board for 2048 to be solved by an AI bot. 
    -----------
    '''
    def __init__(self):
        '''
        Constructor to initialize an appropriately-sized grid for the game and set all attributes.

            Parameters:
                self
        '''
        # Permitted moves on the grid.
        self.moves = ['right', 'left', 'up', 'down']
        # Default grid size.
        self.GRID_SIZE = 5
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.score = 0
        self.timer = 0
        # GUI adjustments.
        self.HEIGHT = 540
        self.WIDTH = 500
        # Space at the top of GUI that is left to display time and score.
        self.TOP_SPACE = self.HEIGHT-self.WIDTH
        # Space between squares in the grid.
        self.SPACE = 5
        self.SQUARE_SIZE = (self.WIDTH-(self.GRID_SIZE+1)*self.SPACE)/self.GRID_SIZE
        pygame.init()
        pygame.display.set_caption("2048: GAME")
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # Initialize all the fonts for the game.
        pygame.font.init()
        self.fontGame = pygame.font.SysFont(FONT_BOARD[0], 
                                            FONT_SIZES[f'{self.GRID_SIZE}'], 
                                            FONT_BOARD[1])
        self.fontScore = pygame.font.SysFont(FONT_BOARD[0],
                                             FONT_SIZES['score'], 
                                             FONT_BOARD[1])
        self.fontMsg = pygame.font.SysFont(FONT_BOARD[0],
                                           FONT_SIZES['finalMsg'],
                                           FONT_BOARD[1])

    @staticmethod
    def updateArr(curr, self):
        '''
        Returns an updated array for row/column of the grid.

            Parameters:
                self
                cur (array) : Array of numbers in the current state of column/row.

            Returns:
                new (np.array) : Updated column/row to the grid.
        '''
        # Append all the non-zero elements of the curr array.
        temp = [n for n in curr if (n!=0)]
        new = []
        skip = False

        # Iterate through the elements of the temp array.
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
        # Set the background color.
        self.window.fill((GRID_COLOR))

        # Iterate in order to display squares in the grid.
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                # Define the coordinates for the current square to draw.
                x = (c+1)*self.SPACE+c*self.SQUARE_SIZE
                y = self.TOP_SPACE+(r+1)*self.SPACE+r*self.SQUARE_SIZE

                # Get the number from the cell to define its corresponding color.
                num = self.grid[r][c]
                
                # If a number on the grid is greater or equal to 2048, it will not
                # change anymore, since dictionary has colors up to the value of 2048.
                if (num>=2048):
                    color = CELL_COLORS[2048]
                else:
                    color = CELL_COLORS[num]

                # Draw the square in the grid.
                pygame.draw.rect(self.window,
                                color,
                                pygame.Rect(x,y,self.SQUARE_SIZE,self.SQUARE_SIZE),
                                border_radius=8)

                # Display numbers for each square. Do NOT draw zeros.
                if (num!=0):
                    textArea = self.fontGame.render(f'{num}', True, GRID_FONT_COLOR)
                    self.window.blit(textArea, textArea.get_rect(center=(x+self.SQUARE_SIZE/2, y+self.SQUARE_SIZE/2)))

    def insertNewNum(self, n=1):
        '''
        Updates a grid with a new number.

        Probability rates for values: 2 (100%).

            Parameters:
                self
                n (int) : Quantity of new numbers to be inserted.
        '''
        availableCoords = []

        for row, col in np.ndindex(self.grid.shape):
            # If the value is equal to 0, it means it is available.
            if (self.grid[row][col]==0):
                availableCoords.append((row, col))

        # Append the new value in the grid in random available position.
        for c in random.sample(availableCoords, k=n):
            self.grid[c] = 2

    def makeMove(self, move):
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
            new = self.updateArr(curr, self)

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

    def updateScore(self):
        '''
        Updates the score. 
        
        The score is denoted by the maximum value in the grid.

            Parameters:
                self
        '''
        self.score = np.max(self.grid)

    def checkIfOver(self):
        '''
        Checks if the game is over.

            Parameters:
                self

            Returns:
                True/False (boolean) : True if game is over; False otherwise.
        '''
        original = self.grid.copy()

        for mv in self.moves:
            self.makeMove(mv)

            # Check if the grids are equal after invoking a move.
            equal = (self.grid==original).all()

            # If the grids are not equal, it means it is possible to 
            # continue the game. Since, there are still available moves to make.
            if (not equal):
                self.grid = original
                return False

        # If none of the moves changes the state of the grid, it denotes the bot loses.
        return True

    def setTimer(self):
        '''
        Sets the timer.

            Parameters:
                self

            Returns:
                start (time) : Started timer.
        '''
        start = time()
        return start

    def stopTimer(self, start):
        '''
        Stops the timer and returns the time of execution.

            Parameters:
                self
                start (time) : Started timer.

            Returns:
                executionTime (time) : Time of execution.
        '''
        stop = time()
        executionTime = stop-start
        return executionTime

    def play(self):
        '''
        Main method to play the game.

            Parameters:
                self

            Returns:
             True/False (boolean) : True if game is won, False otherwise.
        '''
        # Initialize the board with 2 starting numbers in the grid.
        self.insertNewNum(n=2)
        start = self.setTimer()

        # Play as long as the game is neither over, nor won by the AI bot.
        while (True):
            # Draw the board, update and display the current score.
            self.draw()
            self.updateScore()
            textArea = self.fontScore.render(f'SCORE: {self.score:06d}', True, WINDOW_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(115,20)))

            # Update the screen.
            pygame.display.flip()

            # If the AI bot reaches the goal state, i.e. score: 2048, it denotes win.
            if (self.score==2048):
                self.window.fill((GRID_COLOR))
                self.timer = self.stopTimer(start)

                # Display the final message.
                textArea = self.fontMsg.render(f'BOT WON THE GAME!', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                textArea = self.fontMsg.render(f'TIME PLAYED: {self.timer:.1f} SEC', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))

                # Update the window.
                pygame.display.flip()

                # Wait 1 second to display the final screen.
                sleep(1)
                return True

            # Make a copy of the old grid.
            oldGrid = self.grid.copy()

            # Determine the best AI-searched move.
            mv = self.searchMove()

            # Execute the AI selected move.
            self.makeMove(mv)
            
            # Check if it is possible to continue the game after the move.
            if (self.checkIfOver()):
                self.window.fill((GRID_COLOR))
                self.timer = self.stopTimer(start)

                # Display the final message.
                textArea = self.fontMsg.render(f'BOT LOST.', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                textArea = self.fontMsg.render(f'TIME PLAYED: {self.timer:.1f} SEC', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))

                # Update the window.
                pygame.display.flip()

                # Delay 1 second to display the final screen.
                sleep(1)
                return False

            # Check if the grids are equal. If the grids differ insert a new number.
            if (not (self.grid==oldGrid).all()):
                self.insertNewNum()

    # STILL IN DEVELOPMENT STAGE!
    def searchMove(self):
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
        origGrid = self.grid.copy()

        # Dictionary to calculate costs per each move, based on scores and empty spots.
        costs = {mv:0 for mv in self.moves}

        # Determine the number of searches per one move and the depth of the search.
        searchesMv = 100
        depth = 10

        # Test each available move.
        for mv in self.moves:
            # Execute the move, check if possible to continue and get the score.
            self.makeMove(mv)
            gameOverMv = self.checkIfOver()
            scoreMv = np.max(self.grid)

            # If the game is not over and the move changes the state of the board,
            # insert new number, update scores, and perform the further search.
            if (not gameOverMv and not (self.grid==origGrid).all()):
                self.insertNewNum()
                costs[mv] += scoreMv
                counterMv = 1
            # Otherwise, restart the grid to the initial state and move to the next move.
            else:
                self.grid = origGrid.copy()
                continue

            # Perform simulation of later moves.
            for i in range(searchesMv):
                searchBoard = self.grid.copy()
                gameOver = False

                while (not gameOver and counterMv<depth):
                    searchBoard = self.grid.copy()
                    # Execute a random move.
                    self.makeMove(self.shuffleMove())
                    gameOver = self.checkIfOver()
                    simulatedScore = np.max(self.grid)

                    if (not gameOver and not (self.grid==searchBoard).all()):
                        self.insertNewNum()
                        costs[mv] += simulatedScore
                        counterMv += 1

                # Increment the costs by the number of empty spots in the current state of grid.
                costs[mv] += 10*np.count_nonzero(self.grid==0)
            
            # Restart the grid to the initial state for the next move to be tested.
            self.grid = origGrid.copy()

        # Finally, restart the grid to the initial state one last time.
        self.grid = origGrid.copy()

        # Find and return the best searched move.
        print(costs)
        bestMv = max(costs, key=costs.get)
        return bestMv
        
    def shuffleMove(self):
        '''
        Shuffles a random move.

            Parameters:
                self

            Returns:
                randMv : One randomly selected move; either 'right', 'left',
                         'up', or 'down'.
        '''
        randMv = np.random.choice(self.moves, 1)
        return randMv
