# 2048-Project 📟

## The repository contains my own implementation of [2048](https://en.wikipedia.org/wiki/2048_(video_game)), which used to be recognized as a very popular mobile game back in the day. The game was developed in Python using number of popular libraries, e.g. [pygame](https://www.pygame.org/news), [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), etc. The repo contains two slightly different versions of the game. Please follow the descriptions below to find out more about the code!

## ```ai_implementation``` ~ aimed to be solved by an intelligent bot

Rules:
- The game automatically initializes with a specified 4x4 grid size.
- The only value inserted into the grid is 2 (100% probability).
- The game is controlled by the AI bot which selects most optimal moves using - [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).
- The aim for the bot is to obtain at least one square with the value of 2048 in the 4x4 grid.
- The game is terminated when the bot reaches the score of 2048, which denotes a goal state (or when it loses the game).

<b>To read more information about the AI implementation and running the bot - [FOLLOW THE LINK](https://github.com/chizo4/2048-Project/tree/main/ai_implementation).</b>

#

## ```user_implementation``` ~ aimed to be played by a human user

Rules:
- The user might select a grid 3x3, 4x4, 5x5, or 6x6. 
- The grid is initialized with 2 random numbers (either 1 (highest probability rate), 2 or 4).
- The original game of 2048, starts from 2, whereas this example starts from the value of 2<sup>0</sup> instead of 2<sup>1</sup> in order to make it more diffcult (and more CS-friendly)!
- The game itself is controlled by the user using arrow keys.
- The aim is to obtain the highest possible power of 2 in the board, i.e. the game goes further than 2048 and user plays after as long as they do not lose.
- The user's scores for each grid (along with time played and date played) are stored in a local SQLITE3 database; the DB records are processed using pandas.
- Additionally, the implementation contains a Jupyter Notebook for simple analysis of the data collected in the database using several Python libraries, such as: pandas, matplotlib, etc.

<b>To read more information about the user implementation and running it - [FOLLOW THE LINK](https://github.com/chizo4/2048-Project/tree/main/user_implementation).</b>

#

<p align="center">
  <b>Preview of the Game Board</b>
</p>


<p align="center">
  <img src="./images/image_gui.png" width="400" alt="The Image of 2048 Game Board."/>
</p>

#
