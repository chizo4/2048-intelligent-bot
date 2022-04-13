# 2048-Project

### Python implementations of the popular 2048 game using the Pygame library (for creating GUI). The directory contains two slightly different applications of the game.

##

<p align="center">
  <i>Preview of the board of the 2048 game:</i>
</p>


<p align="center">
  <img src="imageGUI.png" width="400" alt="The Image of 2048 Game Board."/>
</p>

##

1. Implementation 1 <i>~ aimed to be played by a human user</i>
  
- The user might select a grid 3x3, 4x4, 5x5, or 6x6. 
- The grid is initialized with 2 random numbers (either 1 (highest probability rate), 2 or 4).
- The original game 2048, starts from 2, whereas this example starts from the value of 2<sup>0</sup> instead of 2<sup>1</sup> in order to make it more diffcult - and more CS-friendly!
- The game itself is controlled by the user using arrow keys.
- The aim is to obtain the highest possible power of 2 in the board, i.e. the game goes further than 2048.
- The user's scores for each grid, along with time played and date played, are stored in an SQLITE3 database, and are processed using pandas.
- Additionally, the implementation contains a Jupyter Notebook for simple analysis of the data collected in the database using pandas library.

#### Running the Implemenation 1: navigate to the project root directory; then, run the main Python file.

```
cd User-Implementation/
```

```
python main.py
```

##

2. Implementation 2 [STILL UNDER DEVELOPMENT] <i>~ aimed to be solved by an AI bot</i>

- <b>12/04/2022 Development Update: The AI bot is able to win the game on 5x5 grid in about 15-20 sec. Nevertheless, still struggles to exceed the value of 1024 on 4x4 grid.</b>
- The game automatically initializes with a specified grid size and so there is no grid selection.
- The only value inserted into the grid is 2 (100% probability).
- The game is controlled by the AI bot (performing appropriate searching algorithms).
- The aim for the bot is to obtain at one square with the value of 2048 in the 4x4 grid.
- The game is terminated when the bot reaches the score of 2048, which denotes a goal state.

#### Running the Implemenation 2: navigate to the right directory (from the project root directory); then, run the main Python file.

```
cd AI-Implementation/
```

```
python main.py
```
