'''
2048 GAME PROJECT: Grid selection.

Date created: 
    11/2021

Date edited:
    03/2022

Author:
    Filip J. Cierkosz
'''

import pygame
from pygame.locals import *
from graphics import GRID_COLOR, FONT_BOARD, FONT_SIZES, USER_FONT_COLOR, WINDOW_FONT_COLOR

class GridSelectionWindow:
    '''
    -----------
    Class to create a grid selection window.
    -----------
    '''

    def __init__(self):
        '''
        Constructor to initialize the window and set all the attributes.

            Parameters:
                self
        '''
        self.HEIGHT = 200
        self.WIDTH = 500
        pygame.init()
        pygame.display.set_caption("2048: GRID SELECTION")
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_BOARD[0], FONT_SIZES['select'], FONT_BOARD[1])
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.response = '4'
        # Initially, the game window does not show up. The selection grid
        # window disappears and the game window appears when the user clicks
        # enter after inputting an appropriate grid size.
        self.playGame = False

    def getResponse(self):
        '''
        Accessor for the user's response.

            Parameters:
                self

            Returns:
                self.response (string) : Grid size selected by the user.
        '''
        return self.response

    def promptUser(self):
        '''
        Gets the user response, which defines the size of the grid.

            Parameters:
                self
        '''
        while (True):
            for event in pygame.event.get():
                if (event.type==KEYDOWN):
                    # Allow only digits as input.
                    if (event.unicode.isdigit()):
                        self.response = event.unicode
                    # If required, clear user's input
                    elif (event.key==K_BACKSPACE):
                        self.response = self.response[:-1]
                    # If user clicks enter and numerical value is correct, the game starts.
                    elif (event.key==K_RETURN and self.response in '3456' and self.response!=''):
                        self.playGame = True
                        return 
                elif (event.type==QUIT):
                    return

            # Set background color.
            self.window.fill(GRID_COLOR)

            # Display all the instructions.
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
