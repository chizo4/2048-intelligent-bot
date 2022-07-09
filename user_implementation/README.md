# ```user_implementation``` 👷🏻‍♂️

## Rules Recap

- The user might select a grid 3x3, 4x4, 5x5, or 6x6. 
- The grid is initialized with 2 random numbers (either 1 (highest probability rate), 2 or 4).
- The original game of 2048, starts from 2, whereas this example starts from the value of 2<sup>0</sup> instead of 2<sup>1</sup> in order to make it more diffcult (and more CS-friendly)!
- The game itself is controlled by the user using arrow keys.
- The aim is to obtain the highest possible power of 2 in the board, i.e. the game goes further than 2048 and user plays after as long as they do not lose.
- The user's scores for each grid (along with time played and date played) are stored in a local SQLITE3 database; the DB records are processed using pandas dataframe.
- Additionally, the implementation contains a Jupyter Notebook for simple analysis of the data collected in the database using several Python libraries, such as: pandas, matplotlib, etc., to possibly identify any patterns.

# 

## Running Application

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

- The next step to follow is to navigate into the ```user_implementation``` directory:

```
cd user_implementation
```

- Finally, you are able to play the game running:


```
python main.py
```

# ENJOY PLAYING THE GAME! 😊
