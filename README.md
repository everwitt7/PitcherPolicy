# Pitch-Policy


## Local Setup

1. Clone repository: `https://github.com/everwitt7/Pitch-Prediction.git`
2. Create a virtual environment: `python -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Navigate to subfolder: `cd pitcher_policy`
5. Run `pitcher_policy.py`

## Run Tests

`python -m unittest -v all_test.py`



## Abstract 

The field of quantitative analytics has transformed the world of sports over the last decade. To date, these analytic approaches are statistical at their core, characterizing what is and what was, while using this information to drive decisions about what to do in the future. However, as we often view team sports, such as soccer, hockey, and baseball, as pairwise win-lose encounters, it seems natural to model these as zero-sum games. We propose such a model for one important class of sports encounters: a baseball at-bat, which is a matchup between a pitcher and a batter. Specifically, we propose a novel model of this encounter as a zero-sum stochastic game, in which the goal of the batter is to get on base, an outcome the pitcher aims to prevent. The value of this game is the on-base percentage (i.e., the probability that the batter gets on base). In principle, this stochastic game can be solved using classical approaches. The main technical challenges lie in predicting the distribution of pitch locations as a function of pitcher intention, predicting the distribution of outcomes if the batter decides to swing at a pitch, and characterizing the level of patience of a particular batter. We address these challenges by proposing novel pitcher and batter representations as well as a novel deep neural network architecture for outcome prediction. Our experiments using Kaggle data from the 2015 to 2018 Major League Baseball seasons demonstrate the efficacy of the proposed approach.

Link to full paper:
[ToDo]()

## Raw Data
[Pitch by Pitch Baseball Data](https://www.kaggle.com/pschale/mlb-pitch-data-20152018)
Unfortunately the MLB decided to crackdown on its publicly available data, so it is no longer possible to scrape this data; this is the best data we have access to. We noted some errors in the 2019 scraped data surrounding correct strike and ball counts. As a result, we focus on the available 2015-2018 data.

## Overview
To combine the data look at `./data_cleaning/combining-data/pitch_and_at_bat.ipynb`. This will take these raw files and output comprehensive csv files that clean the raw data. Using this data, we refine the data and train our models in `./model_training`. We also save the pitcher and batter tensors needed to run the stochastic game. Using the saved models and tensors from the training notebooks (saved in `./models` and `./tensors`, respectively ), we run the Stochastic Game in `./pitcher_policy`, specifying the pitcher and batter in `./pitcher_policy/pitcher_policy.py`.
