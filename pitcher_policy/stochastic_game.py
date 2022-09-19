"""Stochastic Game Module"""
from typing import List
from state import Count
from ortools.linear_solver import pywraplp
from state_action_enums import BatActs, Outcomes


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

    def __init__(self, states: List[Count], trans_prob_mat: dict, outcome_values) -> None:
        """Instantiates StochasticGame object

        Parameters
        ----------
        counts : List[Count]
            the list of states that define our game
        trans_prob_mat : dict
            dict[pitch][zone][batact][outcome] = transition_probability
        """
        self.states = states
        self.trans_prob_mat = trans_prob_mat
        self.outcome_values = outcome_values


    def solve_game(self) -> None:
        """Solves the stochastic game given state and tranisition probabilities

        Returns
        -------
        (dict, dict)
            state_val the value of each state,
            policy the optimal pitcher actions to minimize batter OBP
            (which determines state_val)
        """
        state_vals, state_policy, outcome_probabilities = self.run_val_iter()
        #self.print_solution(state_vals, state_policy)
        return state_vals, state_policy, outcome_probabilities

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
                we set the range as 0...+infinity for state_val and x_optimal to
                fulfill this

            writing state_val - Sum(...) >= 0 to conform to GLOP syntax
            state_val: float, the value of the state
            x_optimal: dict, the optimal policy of a pitcher to minimize state_val
            One can think of state_val as the OBP of a batter at a given state
        """
        """solver = pywraplp.Solver(
            "SolveSimpleSystem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        """
        solver = pywraplp.Solver.CreateSolver("GLOP")

        # defining state value
        state_val = solver.NumVar(0, solver.infinity(), "state_val")

        # defining pitcher actions
        p_actions = {}
        for pitch in q_vals:
            p_actions[pitch] = {}
            for zone in q_vals[pitch]:
                p_actions[pitch][zone] = solver.NumVar(
                    0, max_pitch_pct, pitch + str(zone)
                )

        # Constraint 1: state_val - sum(i = 0...n) { policy(i) * q(i,swing) } >= 0
        constraint1 = solver.Constraint(0, solver.infinity())
        constraint1.SetCoefficient(state_val, 1)
        for pitch in q_vals:
            for zone in q_vals[pitch]:
                constraint1.SetCoefficient(
                    p_actions[pitch][zone],
                    -1 * q_vals[pitch][zone][BatActs.SWING.value],
                )

        # Constraint 2: state_val - sum(i = 0...n) { policy(i) * q(i, take) } >= 0
        constraint2 = solver.Constraint(0, solver.infinity())
        constraint2.SetCoefficient(state_val, 1)
        for pitch in q_vals:
            for zone in q_vals[pitch]:
                constraint2.SetCoefficient(
                    p_actions[pitch][zone], -1 * q_vals[pitch][zone][BatActs.TAKE.value]
                )

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
                if p_actions[pitch][zone].solution_value() > 0:
                    optimal_policy[pitch][zone] = p_actions[pitch][
                        zone
                    ].solution_value()

        swing_take_probs = {BatActs.SWING.value: constraint1.dual_value(), BatActs.TAKE.value: constraint2.dual_value()}

        return state_val.solution_value(), optimal_policy, swing_take_probs

    def run_val_iter(self, theta: float = 0.001):
        """Runs value iteration until we see state value changes less than theta

        Parameters
        ----------
        theta : float
            the threshold at which we stop performing value iteration

        Returns
        -------
        (dict, dict)
            state_val the value of each state,
            policy the optimal pitcher actions to minimize batter OBP
            (which determines state_val)
        """
        q_vals = {}
        policy = {}
        state_val = {}
        swing_take_probs = {}
        outcome_probabilities = {}
        for state in self.states:
            policy[state.state_name] = {}
            state_val[state.state_name] = [0]

        # to keep track of the previous state value (storing in a list rather than last prev)
        iters = 0
        while True:
            all_states_done = True if iters > 0 else False
            for state in self.states:
                count = state.state_name
                outcome_probabilities[state.state_name] = {}
                q_vals[state.state_name] = {}

                for pitch in self.trans_prob_mat:
                    q_vals[state.state_name][pitch] = {}
                    outcome_probabilities[state.state_name][pitch] = {}
                    for zone in self.trans_prob_mat[pitch]:
                        # we reset the q_vals everytime our state_vals change
                        q_vals[state.state_name][pitch][zone] = {
                            BatActs.SWING.value: 0,
                            BatActs.TAKE.value: 0,
                        }
                        outcome_probabilities[state.state_name][pitch][zone] = {
                            Outcomes.SINGLE.value: 0,
                            Outcomes.DOUBLE.value: 0,
                            Outcomes.TRIPLE.value: 0,
                            Outcomes.HOMERUN.value: 0,
                            Outcomes.OUT.value: 0
                        }

                        # compute swing q_vals
                        for res, res_prob in self.trans_prob_mat[pitch][zone][count][
                            BatActs.SWING.value
                        ].items():
                            # given a state and outcome, what is the next state
                            nxt_state = state.get_successor(res)
                            """
                            if nxt_state in [Outcomes.SINGLE.value,Outcomes.DOUBLE.value,Outcomes.TRIPLE.value,Outcomes.HOMERUN.value,Outcomes.OUT.value]:
                                outcome_probabilities[state.state_name][pitch][zone][nxt_state] += res_prob
                            """
                            if nxt_state == Outcomes.SINGLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.SWING.value
                                ] += res_prob * self.outcome_values[Outcomes.SINGLE.value]
                            elif nxt_state == Outcomes.DOUBLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.SWING.value
                                ] += res_prob * self.outcome_values[Outcomes.DOUBLE.value]
                            elif nxt_state == Outcomes.TRIPLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.SWING.value
                                ] += res_prob * self.outcome_values[Outcomes.TRIPLE.value]
                            elif nxt_state == Outcomes.HOMERUN.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.SWING.value
                                ] += res_prob * self.outcome_values[Outcomes.HOMERUN.value]
                            elif nxt_state != Outcomes.OUT.value:
                                # print(state_val[nxt_state][iters])
                                # print(res_prob)
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.SWING.value
                                ] += (res_prob * state_val[nxt_state][iters])


                        # compute take q_vals
                        for res, res_prob in self.trans_prob_mat[pitch][zone][count][
                            BatActs.TAKE.value
                        ].items():

                            # given a state and outcome, what is the next state
                            nxt_state = state.get_successor(res)
                            """
                            if nxt_state in [Outcomes.SINGLE.value,Outcomes.DOUBLE.value,Outcomes.TRIPLE.value,Outcomes.HOMERUN.value,Outcomes.OUT.value]:
                                outcome_probabilities[state.state_name][pitch][zone][nxt_state] += res_prob
                            """
                            if nxt_state == Outcomes.SINGLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.TAKE.value
                                ] += res_prob * self.outcome_values["single"]
                                outcome_probabilities[state.state_name][pitch][zone][nxt_state] += res_prob
                            elif nxt_state == Outcomes.DOUBLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.TAKE.value
                                ] += res_prob * self.outcome_values["double"]
                            elif nxt_state == Outcomes.TRIPLE.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.TAKE.value
                                ] += res_prob * self.outcome_values["triple"]
                            elif nxt_state == Outcomes.HOMERUN.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.TAKE.value
                                ] += res_prob * self.outcome_values["homerun"]
                            elif nxt_state != Outcomes.OUT.value:
                                q_vals[state.state_name][pitch][zone][
                                    BatActs.TAKE.value
                                ] += (res_prob * state_val[nxt_state][iters])
                # passing q_vals into LP to get state_val and policy
                new_state_val, policy[state.state_name], swing_take_probs[state.state_name] = self.solve_lp(
                    q_vals[state.state_name]
                )
                state_val[state.state_name].append(new_state_val)

                # checking if any state val difference is >= theta... if so do not exit
                if iters > 0:
                    if (
                        abs(
                            state_val[state.state_name][iters]
                            - state_val[state.state_name][iters - 1]
                        )
                        >= theta
                    ):
                        all_states_done = False

            # if all state differences are < theta, then exit while loop
            if all_states_done:
                break
            
            iters += 1
        outcome_probabilities = self.get_outcome_probs(policy, swing_take_probs)
        return state_val, policy, outcome_probabilities
    def get_outcome_probs(self, policy, swing_take_probs):
        outcome_probabilities = {}
        initial_state = self.states[0]
        outcome_probabilities = self.get_state_outcome_prob(initial_state, policy, swing_take_probs, outcome_probabilities)
        return outcome_probabilities

    def get_state_outcome_prob(self, state, policy,swing_take_probs, outcome_probabilities):
        count = state.state_name
        if count in outcome_probabilities.keys():
            return outcome_probabilities
        else:
            outcome_probabilities[count] = {
                Outcomes.SINGLE.value: 0,
                Outcomes.DOUBLE.value: 0,
                Outcomes.TRIPLE.value: 0,
                Outcomes.HOMERUN.value: 0,
                Outcomes.OUT.value: 0
            }
            p_same_state = 0
            for pitch, zones in policy[count].items():
                for zone, p_action in zones.items():
                    for b_action, b_prob in swing_take_probs[count].items():
                        for res, res_prob in self.trans_prob_mat[pitch][zone][count][b_action].items():
                            # given a state and outcome, what is the next state
                            nxt_state = state.get_successor(res)
                            if nxt_state in [Outcomes.SINGLE.value,Outcomes.DOUBLE.value,Outcomes.TRIPLE.value,Outcomes.HOMERUN.value,Outcomes.OUT.value]:
                                outcome_probabilities[count][nxt_state] += res_prob*p_action*b_prob

                            else:
                                if nxt_state == count: #next state is same is the current, we use geometric sum
                                    p_same_state += p_action*b_prob*res_prob
                                else:
                                    nxt_state_obj = Count(state.outcomes, int(nxt_state[0]), int(nxt_state[1]))
                                    updated_outcomes = self.get_state_outcome_prob(nxt_state_obj,policy, swing_take_probs, outcome_probabilities)
                                    for final_state, final_state_prob in updated_outcomes[nxt_state].items():
                                        outcome_probabilities[count][final_state] += res_prob*p_action*b_prob*final_state_prob
            if p_same_state>0:
                #print(state.state_name)
                #print(p_same_state)
                #next state is same is the current, we use geometric sum
                for outcome, p_outcome in outcome_probabilities[count].items():
                    outcome_probabilities[count][outcome] += p_same_state*(p_outcome/(1-p_same_state))

        return outcome_probabilities


    def print_solution(self, state_vals: List[dict], state_policy: dict) -> None:
        """Prints the state_value and optimal policy for each state

        Parameters
        ----------
        state_vals : List[dict]
            list of state_value dicts that has state_val (val) for each state (key)
            the list of length iters needed to break out of value iteration so we can
            see how state_values updated
        state_policy : dict
            a dict that has the optimal policy (val) for each state (key)
        """
        for state in self.states:
            print(
                f"Count: {state.state_name}, Value: {state_vals[state.state_name][-1]}"
            )
            for pitch in state_policy[state.state_name]:
                for zone in state_policy[state.state_name][pitch]:
                    if state_policy[state.state_name][pitch][zone] > 0:
                        print(
                            f"{pitch} {zone}:\
                            {round(state_policy[state.state_name][pitch][zone], 5)}"
                        )
