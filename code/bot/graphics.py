'''
code/bot/graphics.py

2048-intelligent-bot: Graphics adjustments for AI bot/game board.

Author: Filip J. Cierkosz (2022)
'''


# Background color for the grid.
GRID_COLOR = '#12023d'

# Font adjustments.
FONT_BOARD = ('Comic Sans MS', 'bold')

# Font colors.
GRID_FONT_COLOR = '#12023d'
WINDOW_FONT_COLOR = '#fafafa'
USER_FONT_COLOR = '#a2ff29'

# Cell colors corresponding with their numerical values on the board.
CELL_COLORS = {
    0: '#fafafa',
    1: '#c4beb5',
    2: '#a89372',
    4: '#c28d3a',
    8: '#c2821d',
    16: '#d4860d',
    32: '#e68d05',
    64: '#f04826',
    128: '#ed3611',
    256: '#ff2b00',
    512: '#e6ae2c',
    1024: '#f0b426',
    2048: '#ffb300',
}

# Font sizes for different usages.
FONT_SIZES = {
    '4': 35,
    'final_msg': 30,
    'score': 25
}
