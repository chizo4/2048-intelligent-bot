# 2048 GAME PROJECT
# Written by: Filip J. Cierkosz
# Date: 11/2021


#~~~~~~~~~~IMPORTS~~~~~~~~~~
import random
import numpy as np
import pygame
from pygame.locals import *
from time import sleep, time
from graphics import GRID_COLOR, CELL_COLORS, GRID_FONT_COLOR, FONT_BOARD, FONT_SIZES, USER_FONT_COLOR, WINDOW_FONT_COLOR
from bestScoresFunc import updateDatafile, getCurrBestScore


#~~~~~~~~~~CLASS: GAME 2048~~~~~~~~~~
class Game2048:
    #~~~~~~~~~~CONSTRUCTOR~~~~~~~~~~
    # Initialize an appropriately-sized grid for the game and set its attributes.
    def __init__(self, gs):
        # Set the grid size according to the user response.
        self.GRID_SIZE = gs

        # Initially, create a proper-sized array full of zeros that will be 
        # later used as the grid in the game.
        self.grid = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)

        # Define the dimensions of the GUI window.
        self.HEIGHT = 540
        self.WIDTH = 500

        # Space at the top of GUI that is left to display time and score.
        self.TOP_SPACE = self.HEIGHT-self.WIDTH

        # Space between squares in the grid.
        self.SPACE = 5

        # Define the size of a single square in the grid.
        self.SQUARE_SIZE = (self.WIDTH-(self.GRID_SIZE+1)*self.SPACE)/self.GRID_SIZE

        # Initialize the score.
        self.score = 0

        # Get the current best score for the grid with the defined size.
        self.currBestScore = getCurrBestScore('bestScores.csv', gs)

        # Initialize the pygame module.
        pygame.init()

        # Set the title of the window.
        pygame.display.set_caption("2048: GAME")

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

        # Initialize the window for the game.
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    #~~~~~~~~~~STATIC METHODS~~~~~~~~~~
    # Static method 1: Return an updated array for row/column of the grid.
    @staticmethod
    def updateArr(curr, self):
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

        # Fill the rest of the array with zeros, so that it matches the size
        # of the curr array.
        while (len(new)!=len(curr)):
            new.append(0)

        return np.array(new)

    # Static method 2: Listen for the user keyboard press.
    @staticmethod
    def listenForKeyPress():
        while (True):
            for event in pygame.event.get():
                if (event.type==QUIT):
                    return 'stop' 
                if (event.type==KEYDOWN):
                    # Left arrow.
                    if (event.key==K_LEFT):
                        return 'left'
                    # Right arrow.
                    elif (event.key==K_RIGHT):
                        return 'right'
                    # Up arrow.
                    elif (event.key==K_UP):
                        return 'up'
                    # Down arrow.
                    elif (event.key==K_DOWN):
                        return 'down'
                    elif (event.key==K_q or event.key==K_ESCAPE):
                        return 'stop'

    #~~~~~~~~~~METHODS~~~~~~~~~~
    # Method 1: draw the game window.
    def draw(self):
        # Set the background color for the window.
        self.window.fill((GRID_COLOR))

        # Iterate in order to display squares in the grid.
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                # Define the coordinates for the current square to display.
                x = (c+1)*self.SPACE+c*self.SQUARE_SIZE
                y = self.TOP_SPACE+(r+1)*self.SPACE+r*self.SQUARE_SIZE

                # Get the number on the grid to define its corresponding color
                # in the dictionary.
                num = self.grid[r][c]
                
                # If a number on the grid is greater or equal to 2048, it will not
                # change anymore, since dictionary has colors up to tha value of 2048.
                if (num>=2048):
                    color = CELL_COLORS[2048]
                else:
                    color = CELL_COLORS[num]

                # Display a square in the grid.
                pygame.draw.rect(self.window,
                                color, 
                                pygame.Rect(x,y,self.SQUARE_SIZE,self.SQUARE_SIZE),
                                border_radius=8)

                # Create the text object to display numbers in the game window at 
                # the specified coordinates. Do NOT draw zeros.
                if (num!=0):
                    textArea = self.fontGame.render(f'{num}', True, GRID_FONT_COLOR)
                    self.window.blit(textArea, textArea.get_rect(center=(x+self.SQUARE_SIZE/2, y+self.SQUARE_SIZE/2)))

    # Method 2: Append a new number in the grid.
    def newNum(self, n=1):
        # Tuple for coordinates that are available in the grid (denoted by 0).
        availableCoords = []

        # Iterate through the rows and columns of the grid.
        for row, col in np.ndindex(self.grid.shape):
            # If the value is equal to 0, append it in the array.
            if (self.grid[row][col]==0):
                availableCoords.append((row, col))

        # The original game 2048, starts from 2 (2**1), whereas this 
        # example starts from the value of 2**0 instead of 2**1 in order
        # to make it harder (and more CS-friendly). In most of the cases,
        # 1 appears in the grid. Nonetheless, 2 and 4 can also appear.
        for c in random.sample(availableCoords, k=n):
            if (random.random()<0.05):
                self.grid[c] = 4
            elif (random.random()<0.2):
                self.grid[c] = 2
            else:
                self.grid[c] = 1

    # Method 3: Make a move based on the user keyboard press.
    # If you wish to move to the left/right, look at the rows of the
    # grid. If you wish to move up/down, look at the columns.
    def makeMove(self, move):
        # Iterate through the elements of a row/column. If two equal
        # elements are next to each other, they should be added.
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
            # LEFT.
            if (move=='left'):
                self.grid[i] = new
            # UP.
            elif (move=='up'):
                self.grid[:, i] = new
            # Update in the grid for the move to the right or down.
            # The updated array has to be reversed again, so that non-zero
            # elements are at the end of the new array.
            # RIGHT.
            elif (move=='right'):
                self.grid[i] = new[::-1]
            # DOWN.
            elif (move=='down'):
                self.grid[:, i] = new[::-1]

    # Method 4: Get the current score. The score is denoted by the maximum value 
    # in the grid.
    def updateScore(self):
        self.score = np.max(self.grid)

    # Method 5: Check if the game is over (returns True if it is).
    def checkIfOver(self):
        # Array of all possible moves on the grid.
        moves = ['right', 'left', 'up', 'down']

        # Make a copy of the grid.
        original = self.grid.copy()

        # Iterate through all the possible moves.
        for mv in moves:
            # Invoke the move.
            self.makeMove(mv)

            # Check if the grids are equal.
            equal = (self.grid==original).all()

            # If the grids are not equal, it means it is possible to 
            # continue the game. Since, there are available moves to make.
            if (not equal):
                self.grid = original
                return False

        # If none of the moves brings any changes to the grid, it means
        # that the user lost the game.
        return True

    # Method 6: Set the timer.
    def setTimer(self):
        start = time()
        return start

    # Method 7: Stop the timer and return the time of execution.
    def stopTimer(self, start):
        stop = time()
        executionTime = stop-start
        return executionTime

    # Method 8: Main method to play the game.
    def play(self):
        # Initialize the board with 2 starting numbers in the grid.
        self.newNum(n=2)

        # Set the timer.
        start = self.setTimer()

        # Play as long as the game is neither over nor quit by the user.
        while (True):
            # Draw the board for the game.
            self.draw()
            
            # Update and show the current score.
            self.updateScore()
            textArea = self.fontScore.render(f'SCORE: {self.score:06d}', True, WINDOW_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(115,20)))

            # Update the screen.
            pygame.display.flip()

            # Get the user keyboard response.
            kbdResponse = self.listenForKeyPress()

            # The game stops if the user triggers 'q' or escape the game.
            if (kbdResponse=='stop'):
                break

            # Make a copy of the old grid.
            oldGrid = self.grid.copy()
            
            # Execute the user command.
            self.makeMove(kbdResponse)
            
            # Check if it is possible to continue the game, i.e. make the next
            # move. If not, the game is over.
            if (self.checkIfOver()):
                # Fill the whole screen with the background color.
                self.window.fill((GRID_COLOR))

                # Stop the timer. Get the time of execution.
                timer = self.stopTimer(start)

                # Show the final message, time played, scores to the user.
                textArea = self.fontMsg.render('GAME OVER!', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-120)))
                textArea = self.fontMsg.render(f'TIME PLAYED: {timer:.1f} SEC', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2-50)))
                textArea = self.fontMsg.render(f'YOUR SCORE: {self.score}', True, WINDOW_FONT_COLOR)
                self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+20)))

                # If the user beats the current best score, inform about this.
                if (self.score>int(self.currBestScore)):
                    textArea = self.fontMsg.render(f'NEW BEST SCORE: {self.score}', True, USER_FONT_COLOR)
                    self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+90)))
                # Otherwise, display the current best score.
                else:
                    textArea = self.fontMsg.render(f'BEST SCORE: {self.currBestScore}', True, WINDOW_FONT_COLOR)
                    self.window.blit(textArea, textArea.get_rect(center=(self.WIDTH/2,self.HEIGHT/2+90)))
                
                # Update the window.
                pygame.display.flip()

                # Wait 5 seconds to display the final screen. Then, end the program.
                sleep(5)
                break

            # Check if the grids are equal.
            equal = (self.grid==oldGrid).all()

            # If the grid after executing command differs from the grid after executing
            # the command, append a new number in a randomly chosen available position.
            if (not equal):
                self.newNum()


#~~~~~~~~~~CLASS: GRID SELECTION~~~~~~~~~~
class GridSelectionWindow:
    #~~~~~~~~~~CONSTRUCTOR~~~~~~~~~~
    # Initialize the the window and set all the attributes.
    def __init__(self):
        # Define the dimensions of the window.
        self.HEIGHT = 200
        self.WIDTH = 500

        # Initialize the pygame module.
        pygame.init()

        # Set the title of the window.
        pygame.display.set_caption("2048: GRID SELECTION")

        # Initialize the font.
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_BOARD[0], FONT_SIZES['select'], FONT_BOARD[1])

        # Create the window for the class.
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # User response which will be used later to determine grid size.
        # By default, it is set to 4.
        self.response = '4'
        
        # Initially, the game window does not show up. The selection grid
        # window disappears and the game window appears when the user clicks
        # enter after inputting an appropriate grid size.
        self.playGame = False

    #~~~~~~~~~~METHODS~~~~~~~~~~
    # Method 1: Get the user response, which defines the size of grid.
    def promptUser(self):
        while (True):
            for event in pygame.event.get():
                if (event.type==KEYDOWN):
                    # Allow only digits as input.
                    if (event.unicode.isdigit()):
                        self.response = event.unicode
                    # If required, clear user's input
                    elif (event.key==K_BACKSPACE):
                        self.response = self.response[:-1]
                    # If user clicks enter and the numerical value is appropriate,
                    # the game starts.
                    elif (event.key==K_RETURN and self.response in '3456'):
                        self.playGame = True
                        return 
                elif (event.type==QUIT):
                    return

            # Set the background color.
            self.window.fill(GRID_COLOR)

            # Display all the instructions to the user.
            textArea = self.font.render('WELCOME TO THE 2048 GAME!', True, WINDOW_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(250,30)))
            textArea = self.font.render('INPUT GRID SIZE (3/4/5/6)', True, WINDOW_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(250,75)))
            textArea = self.font.render('AND CLICK ENTER:', True, WINDOW_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(250,120)))

            # Space for the user input.
            textArea = self.font.render(self.response, True, USER_FONT_COLOR)
            self.window.blit(textArea, textArea.get_rect(center=(250,165)))

            # Update the screen.
            pygame.display.flip()


#~~~~~~~~~~TEST HARNESS~~~~~~~~~~
if (__name__=='__main__'):
    # Create an instance of the grid selection class.
    selection = GridSelectionWindow()

    # Prompts the user for the grid size.
    selection.promptUser()

    # Record the user responses.
    gridSize = int(selection.response)
    initGame = selection.playGame
    
    if (initGame):
        # Create an instance of the game class.
        game = Game2048(gridSize)

        # Invoke the method to play the game.
        game.play()

        # Get the user's score.
        score = game.score

        # Invoke the function to update score. It will be updated
        # if the user beats the current best score.
        updateDatafile('bestScores.csv', gridSize, score)
