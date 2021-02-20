"""Stochastic Game Module"""
from typing import List
from state import Count


class StochasticGame:
    """Class used to represent CountState

    Attributes
    ----------
    counts : List[Count]
        the list of states that define our game
    trans_prob_mat : dict
        dict[pitch][zone][batact][outcome] = transition_probability
    state_val: dict
        a dict that maps each state to a value
    qvals: dict
        qvalsue, a dict that we sum outcomes across pitcher and batter actions
        q[state][pitch][zone][batact] = trans_prob_mat * state_vals[next_state]
    policy: dict
        the optimal actions a pitcher should take to minimize a batter's OBP

    Methods
    -------
    solve_game()
        runts value iteration and solve_lp to solve the game
    solve_lp(q, max_pitch_pct)
        given qvalsues and max_pitch_pct, solves the linear program
    run_val_iter(theta)
        runs value iteration until we see changes less than theta
    """

    # Notes: the thing we will receive from the CNN is just a trans_prob_mat... nothing else changes
    def __init__(self, counts: List[Count], trans_prob_mat: dict) -> None:
        """Instantiates StochasticGame object

        Parameters
        ----------
        counts : List[Count]
            the list of states that define our game
        trans_prob_mat : dict
            dict[pitch][zone][batact][outcome] = transition_probability
        """
        self.counts = counts
        self.trans_prob_mat = trans_prob_mat

    def solve_game(self) -> None:
        """Solves the stochastic game given state and tranisition probabilities

        Returns
        -------
        (dict, dict)
            state_val the value of each state,
            policy the optimal pitcher actions to minimize batter OBP (which determines state_val)
        """

    def solve_lp(self, qvals, max_pitch_pct) -> (int, dict):
        """Solves the linear program to get state value and policy

        Parameters
        ----------
        qvals : dict
            qvalues calculated by summing state values across transition probabilities
        max_pitch_pct : float
            the maximum percent of the time a pitcher is allowed to perform an action

        Returns
        -------
        (int, dict)
            state value, policy of the state to minimize the state value
        """

    def run_val_iter(self, theta):
        """Runs value iteration until we see state value changes less than theta

        Parameters
        ----------
        theta : float
            the threshold at which we stop performing value iteration

        Returns
        -------
        (dict, dict)
            state_val the value of each state,
            policy the optimal pitcher actions to minimize batter OBP (which determines state_val)
        """
