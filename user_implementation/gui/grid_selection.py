'''
user_implementation/gui/grid_selection.py

2048-Project: Grid selection.

Author: Filip J. Cierkosz (2022)
'''


import pygame
from pygame.locals import *
from gui.graphics import *


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
        pygame.display.set_caption('2048: GRID SELECTION')
        pygame.font.init()
        self.font = pygame.font.SysFont(
            FONT_BOARD[0],
            FONT_SIZES['select'],
            FONT_BOARD[1]
        )
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.response = '4'
        # Initially, the game window does not show up. The selection grid
        # window disappears and the game window appears when the user clicks
        # enter after inputting an appropriate grid size.
        self.play_game = False

    def get_response(self):
        '''
        Accessor for the user's response.

            Parameters:
                self

            Returns:
                self.response (string) : Grid size selected by the user.
        '''
        return self.response

    def prompt_user(self):
        '''
        Gets the user response, which defines the size of the grid.

            Parameters:
                self
        '''
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.unicode.isdigit():
                        self.response = event.unicode
                    elif event.key == K_BACKSPACE:
                        self.response = self.response[:-1]
                    elif event.key == K_RETURN and self.response in '3456' and self.response != '':
                        self.play_game = True
                        return 
                elif event.type == QUIT:
                    return

            self.window.fill(GRID_COLOR)
            text_area = self.font.render(
                'WELCOME TO THE 2048 GAME!',
                True, 
                WINDOW_FONT_COLOR
            )
            self.window.blit(
                text_area,
                text_area.get_rect(center=(250, 30))
            )
            text_area = self.font.render(
                'INPUT GRID SIZE - 3 : 4 : 5 : 6',
                True, 
                WINDOW_FONT_COLOR
            )
            self.window.blit(
                text_area,
                text_area.get_rect(center=(250, 75))
            )
            text_area = self.font.render(
                'AND CLICK ENTER:',
                True,
                WINDOW_FONT_COLOR
            )
            self.window.blit(
                text_area,
                text_area.get_rect(center=(250, 120))
            )
            text_area = self.font.render(
                self.response,
                True,
                USER_FONT_COLOR
            )
            self.window.blit(
                text_area,
                text_area.get_rect(center=(250, 165))
            )
            pygame.display.flip()
