# ```ai_implementation``` 🤖

## About the Implementation

The bot attempts to solve the game and reach the goal state by following the logic of [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search). Essentially, it means that the algorithm expands the decision tree by simulating the future states of the current state of the 4x4 grid in order to calculate ```costs``` for each of the four moves: ```['up', 'down', 'right', 'left']```. The ```costs``` are calculated by combining the highest score obtained in each simulated grid and the number of empty spots mutiplied by specified constants. Each selected best move is denoted by the highest ```costs``` value. The number of searches per move and the search depth values could be increased, but the problem is that, at some point, they dramatically affect the runtime of search without a decent increase in its accuracy. Including the number of empty spots multiplied by the constant might seem unconventional at first, but it definitely affects the speed of the search and also slightly increases the accurracy of the algorithm.

#

## Rules Recap

Rules:
- The goal of the bot is to obtain at least one square with the value of 2048 in the 4x4 grid.
- The game automatically initializes with a specified 4x4 grid size.
- The only value inserted into the grid is 2 (100% probability).
- The game is controlled by the AI bot which selects most optimal moves using - [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).
- The game is terminated when the bot reaches the score of 2048, which denotes a goal state (or when it loses the game).

## Bot Performance

The AI was tested for slightly more than 500 samples and the results were stored in a database. 

Performance highlights based on [data](https://github.com/chizo4/2048-Project/blob/main/ai_implementation/notebook/bot_notebook.ipynb) collected while testing:
- ```Probability of AI winning a game : 30.4%```
- ```Probability of a score greater or equal to 1024 : 88.0%```
- ```Average time to win a game : 68.4 sec```

❗ NB: The average time records can be rather described as biased, since it is mainly dependant on the performance of your machine. The reference point for time measurements in this experiment was 2020 M1 MacBook Pro.

The whole analysis of the results in a Jupyter Notebook can be accessed [here](https://github.com/chizo4/2048-Project/blob/main/ai_implementation/notebook/bot_notebook.ipynb).

#

## Running AI

- Before cloning the remote version of the repo and start playing with the code, please make sure that you have ```python3``` and ```pip``` installed on your machine by running the following commands:

```
python3 -V
```

```
pip -V
```

❗ If your shell failed to recognize these commands, please visit [pip](https://pip.pypa.io/en/stable/installation/) and [python](https://www.python.org/downloads/) to find out more about the installation process.

- Otherwise, if you manage to see the versions of ```python3``` and ```pip``` after running the commands, you can clone the whole repo:

```
git clone https://github.com/chizo4/2048-Project
```

- After cloning it, please navigate into the root directory of the project and run the bash script to install any needed libraries. Do not worry if you have some of them pre-installed, the script will only install the ones that are missing. Please run the commands:

```
cd 2048-Project
```

```
bash setup.sh
```

- The next step to follow is to navigate into the ```ai_implementation``` directory:

```
cd ai_implementation
```

- Finally, you are able to run the AI bot invoking:


```
python main.py
```

#

## Contribution & Collaboration

In case you had an idea on how to improve the performance of the AI bot by either increasing its win percentage or decreasing the time needed to win a game, feel free to contact me via of the links included in my [GitHub bio](https://github.com/chizo4) and then you might contribute to the project by creating a new branch with a pull request.