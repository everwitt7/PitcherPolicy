"""Stochastic Game Module"""
from typing import List
from state import Count
from ortools.linear_solver import pywraplp
from pitch_zone_enums import BatActs, Outcomes

# TODO: rename count to state


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
    q_vals: dict
        q_vals, a dict that we sum outcomes across pitcher and batter actions
        q[state][pitch][zone][batact] = trans_prob_mat * state_vals[next_state]
    policy: dict
        the optimal actions a pitcher should take to minimize a batter's OBP

    Methods
    -------
    solve_game()
        runts value iteration and solve_lp to solve the game
    solve_lp(q_vals, max_pitch_pct)
        given q_vals and max_pitch_pct, solves the linear program
    run_val_iter(theta)
        runs value iteration until we see changes less than theta
    """

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
        state_vals, state_policy = self.run_val_iter()
        self.print_solution(state_vals, state_policy)

        # we want this to get the results and then print them too

    def solve_lp(self, q_vals: dict, max_pitch_pct: float = 0.7) -> (int, dict):
        """Solves the linear program to get state value and policy

        Parameters
        ----------
        q_vals : dict
            q_vals calculated by summing state values across transition probabilities
        max_pitch_pct : float
            the maximum percent of the time a pitcher is allowed to perform an action

        Returns
        -------
        (int, dict)
            state value, policy of the state to minimize the state value

        Linear Program:
            min: state_val, x_optimal(i = 0...n)
            subject to:
            state_val >= sum(i = 0...n) { policy(i) * q(i, swing) }
            state_val >= sum(i = 0...n) { policy(i) * q(i, take)  }
            sum(x_optimal) = 1
            x_optimal(i) >= 0 for all i = 0...n
                we set the range as 0...+infinity for state_val and x_optimal to fulfill this

            writing state_val - Sum(...) >= 0 to conform to GLOP syntax
            state_val: float, the value of the state
            x_optimal: dict, the optimal policy of a pitcher to minimize state_val
            One can think of state_val as the OBP of a batter at a given state
        """
        solver = pywraplp.Solver(
            'SolveSimpleSystem', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        # defining state value
        state_val = solver.NumVar(0, solver.infinity(), 'state_val')

        # defining pitcher actions
        p_actions = {}
        for pitch in q_vals:
            p_actions[pitch] = {}
            for zone in q_vals[pitch]:
                p_actions[pitch][zone] = solver.NumVar(
                    0, max_pitch_pct, pitch+zone)

        # Constraint 1: state_val - sum(i = 0...n) { policy(i) * q(i,swing) } >= 0
        constraint1 = solver.Constraint(0, solver.infinity())
        constraint1.SetCoefficient(state_val, 1)
        for pitch in q_vals:
            for zone in q_vals[pitch]:
                constraint1.SetCoefficient(
                    p_actions[pitch][zone], -1 * q_vals[pitch][zone][BatActs.SWING.value])

        # Constraint 2: state_val - sum(i = 0...n) { policy(i) * q(i, take) } >= 0
        constraint2 = solver.Constraint(0, solver.infinity())
        constraint2.SetCoefficient(state_val, 1)
        for pitch in q_vals:
            for zone in q_vals[pitch]:
                constraint2.SetCoefficient(
                    p_actions[pitch][zone], -1 * q_vals[pitch][zone][BatActs.TAKE.value])

        # Constraint 3: sum(x_optimal) = 1
        constraint3 = solver.Constraint(1, 1)
        for pitch in p_actions:
            for zone in p_actions[pitch]:
                constraint3.SetCoefficient(p_actions[pitch][zone], 1)

        # Objective Function: minimize state_val
        objective = solver.Objective()
        objective.SetCoefficient(state_val, 1)
        objective.SetMinimization()

        # Solve the game and return state_val and x_optimal
        solver.Solve()

        optimal_policy = {}
        for pitch in p_actions:
            optimal_policy[pitch] = {}
            for zone in p_actions[pitch]:
                optimal_policy[pitch][zone] = p_actions[pitch][zone].solution_value()

        return state_val.solution_value(), optimal_policy

    def run_val_iter(self, theta: float = 0.007):
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
        q_vals = {}
        policy = {}
        state_val = {}
        for count in self.counts:
            policy[count.state_name] = {}
            state_val[count.state_name] = [0]

        # to keep track of the previous state value (storing in a list rather than last prev)
        iters = 0
        while True:
            all_states_done = True if iters > 0 else False
            for count in self.counts:
                q_vals[count.state_name] = {}
                for pitch in self.trans_prob_mat:
                    q_vals[count.state_name][pitch] = {}
                    for zone in self.trans_prob_mat[pitch]:
                        # we need to reset the q_vals everytime our state_vals change
                        q_vals[count.state_name][pitch][zone] = {
                            BatActs.SWING.value: 0,
                            BatActs.TAKE.value: 0
                        }

                        # compute swing q_vals
                        for res, res_prob in\
                                self.trans_prob_mat[pitch][zone][BatActs.SWING.value].items():

                            # given a state and outcome, what is the next
                            nxt_state = count.get_successor(res)

                            if nxt_state == Outcomes.HIT.value:
                                q_vals[count.state_name][pitch][zone][BatActs.SWING.value]\
                                    += res_prob

                            elif nxt_state != Outcomes.OUT.value:
                                q_vals[count.state_name][pitch][zone][BatActs.SWING.value]\
                                    += res_prob * state_val[nxt_state][iters]

                        # compute take q_vals
                        for res, res_prob in\
                                self.trans_prob_mat[pitch][zone][BatActs.TAKE.value].items():

                            # given a state and outcome, what is the next
                            nxt_state = count.get_successor(res)

                            if nxt_state == Outcomes.HIT.value:
                                q_vals[count.state_name][pitch][zone][BatActs.TAKE.value]\
                                    += res_prob

                            elif nxt_state != Outcomes.OUT.value:
                                q_vals[count.state_name][pitch][zone][BatActs.TAKE.value]\
                                    += res_prob * state_val[nxt_state][iters]

                # passing q_vals into LP to get state_val and policy
                new_state_val, policy[count.state_name] = self.solve_lp(
                    q_vals[count.state_name])
                state_val[count.state_name].append(new_state_val)

                # checking if any state val difference is >= theta... if so do not exit
                if iters > 0:
                    if abs(state_val[count.state_name][iters] -
                           state_val[count.state_name][iters-1]) >= theta:
                        all_states_done = False

            # if all state differences are < theta, then exit while loop
            if all_states_done:
                break

        return state_val, policy

    def print_solution(self, state_vals: dict, state_policy: dict) -> None:
        """ADD PRINTSOL DOCSTRING"""
        for count in self.counts:
            print(
                f'Count: {count.state_name}, Value: {state_vals[count.state_name][-1]}')
            for pitch in state_policy[count.state_name]:
                for zone in state_policy[count.state_name][pitch]:
                    if state_policy[count.state_name][pitch][zone] > 0:
                        print(
                            f'{pitch} {zone}:\
                            {round(state_policy[count.state_name][pitch][zone], 5)}'
                        )
