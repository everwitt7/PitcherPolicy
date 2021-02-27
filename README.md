# Pitch-Prediction

## Local Setup

1. Clone Repository: `https://github.com/everwitt7/Pitch-Prediction.git`
2. Create a Virtual Enviornment: `python -m venv venv`
2. Source It: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run `pitcher_prediction.py`

## Run Tests

`python -m unittest -v all_test.py`

## Raw Data
[Pitch by Pitch Baseball Data](https://www.kaggle.com/pschale/mlb-pitch-data-20152018)
Unfortunately the MLB decided to crackdown on its publicly available data, so it is no longer possible to scrape this data; this is the best data we have access to. To combine the data look at `./data-cleaning/combining-data` jupyter notebooks. They will take these raw files and output a comprehensive csv that combines all available seasons. Using those CSVs we compute the Transition Probabilities of a Batter Swinging (`./data-cleaning/combining-data/swing_transitions.json`) 

## Overview

In a two-player zero-sum Markov game, two adaptive agents interact in a defined environment with probabilistic transition functions. This stochastic game is thus a useful framework when trying to model two agents with opposite goals. An at-bat in the game of baseball has two agents, pitcher and batter, with competing goals, and this paper aims to model this environment as a Markov game in order to find the optimal probabilistic policy for the pitcher to minimize the batter’s utility. Because we have the data readily available, we are not learning the optimal policy but rather solving for it analytically.

In short, we consider baseball to be a two player zero sum stochastic game for the pitcher and batter. The batter hopes to get on base, the pitchers hopes to get the batter out - their goals are diametrically opposed. We consider the states of the game to be all possible counts (one can make the states more complex by considering runners on base, outs, etc...), the batter actions to be swing and take, and the pitcher actions to be a combination of pitch type and pitch location. We can solve this game by running value iteration, where at each state we formulate the state value and pitcher policy by framing the problem as a minimax game (the pitcher tries to get the batter out, the batter tries to get on base). We can solve this linear program to get state value and the pitcher's optimal policy. We do this for each state until every state value changes be less than theta, in which case we are done and can return state values and state pitcher policies. 

We consider all states to have 0 reward except for the terminal state of getting on base, in which case we give a reward with 1 (to make the game more realistic, it would make sense to consider more complex states and a reward of 1 any time a runner scores, then we can minimize runs instead of OBP). Given the problem formulation, state values actually represent the OBP of a batter, so we can compare the OBP of a new count, 0-0, with historical OBP to see if pitchers can perform better by simply changing their decision making at certain counts.

Link to full paper:
[ToDo]()
