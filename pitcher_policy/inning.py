import pandas as pd
import numpy as np
from tensorflow.keras import models
from pitch_zone_config import gen_pitches, gen_counts, gen_acc_mat, gen_take_mat, gen_swing_trans_matrix, gen_trans_prob_mat
from stochastic_game import StochasticGame




class AtBat: #An at bat, the state within an inning
    def __init__(self, pitcher, batting_order:list, batting_index:int, first: bool, second: bool, third: bool, outs: int, runs: int, acc_matrix, take_model, swing_trans_model):
        self.batting_order = batting_order
        self.batting_index = batting_index  % len(batting_order)
        self.batter = batting_order[self.batting_index]
        self.first = first
        self.second = second
        self.third = third
        self.outs = outs
        self.pitcher = pitcher
        self.value = None
        self.runs = runs
        self.terminal = False
        self.outcome_values = None
        self.acc_matrix = acc_matrix
        self.take_model = take_model
        self.swing_trans_model = swing_trans_model
    def __print__(self):
        return "At Bat... Batting:%s, ROB:(%s,%s,%s), Outs:%s"%(self.batter, self.first, self.second, self.third, self.outs)
    def __repr__(self):
        return "BI:%s,1:%s,2:%s,3:%s,O:%s,R:%s"%(self.batting_index, self.first, self.second, self.third, self.outs, self.runs)
    def __str__(self):
        return "BI:%s,1:%s,2:%s,3:%s,O:%s,R:%s"%(self.batting_index, self.first, self.second, self.third, self.outs, self.runs)
    def get_transition_probabilities(self):
        #Solve game, passing in outcome_values
      
        pitcher = np.array(self.pitcher)
        batter = np.array(self.batter)

        pitches = gen_pitches()
        counts = gen_counts()

        take_matrix = gen_take_mat(self.take_model, batter, pitches, .2)
        nn_swing_trans_matrix = gen_swing_trans_matrix(self.swing_trans_model, pitcher, batter, take_matrix, pitches)
        nn_trans_prob_matrix = gen_trans_prob_mat(nn_swing_trans_matrix, self.acc_matrix, take_matrix)
        outcome_values = self.outcome_values

        s1 = StochasticGame(counts, nn_trans_prob_matrix, outcome_values)

        s1_vals, s1_pol, s1_outcome_probs = s1.solve_game()
        transition_matrix = s1_outcome_probs["00"]

        return transition_matrix
    def set_outcome_values(self, outcome_values):
        self.outcome_values = outcome_values

            
class TerminalState:
    def __init__(self, runs):
        self.value = runs
        self.terminal = True
    def get_value(self, iteration):
        return self.runs
    def __str__(self):
        return "Inning Done...Runs: %s"%(self.value)
    def __repr__(self):
        return "Inning Done...Runs: %s"%(self.value)
        
class Outcome:
    def __init__(self, outcome):
        self.base_progression = 0
        self.outcome= None
        if outcome == "single":
            self.base_progression = 1
            self.outcome = outcome
        elif outcome == "double":
            self.base_progression = 2
            self.outcome = outcome
        elif outcome == "triple":
            self.base_progression = 3
            self.outcome = outcome
        elif outcome == "homerun":
            self.base_progression = 4
            self.outcome = outcome
        elif outcome == "out":
            self.base_progression = 0
            self.outcome = outcome
        else:
            raise "invalid outcome"
    def __repr__(self):
        return self.base_progression
    
class Inning:
    def __init__(self, pitcher, batting_order:list, take_model, swing_trans_model, acc_model, batting_order_start_index = 0, runs = 0, outs=0):
        self.batting_order = batting_order
        self.pitcher = pitcher
        self.start_runs = runs
        self.start_outs = outs
        self.batting_index = batting_order_start_index
        self.states_values = []
        self.states_expanded = 0
        self.take_model = take_model
        self.swing_trans_model = swing_trans_model
        self.acc_model = acc_model
        self.acc_matrix = self.gen_acc_matrix(self.acc_model)
        self.start_state = AtBat(self.pitcher, self.batting_order, self.batting_index, False, False, False, self.start_runs, self.start_outs, self.acc_matrix, self.take_model, self.swing_trans_model) 
    
    
    def gen_acc_matrix(self, acc_model):
        pitches = gen_pitches()
        acc_mat = gen_acc_mat(acc_model,self.pitcher,pitches)
        return acc_mat

    def solve_inning(self, epsilon = .1):
        iteration = 0
        self.states_values = []
        print("------ITER %s -------" %(iteration))
        previous_iter = self.get_state_values(iteration)
        done = False
        self.previous_values = previous_iter
        if not done:
            iteration +=1
            print("------ITER %s -------" %(iteration))
            current_iter = self.get_state_values(iteration)
            done = self.check_less_than_epsilon(current_iter, previous_iter, epsilon)
            self.previous_values = previous_iter
            previous_iter = current_iter
        print("DONE IN %s ITERATIONS")
        print(current_iter)

           
    def check_less_than_epsilon(self, curr_iter, prev_iter, epsilon):
        for key in curr_iter.keys():
            if curr_iter[key] - prev_iter[key] > epsilon:
                return False
        return True
    
    def get_state_values(self,iteration):
        states_values_at_iter = {}
        states_values_at_iter = self.get_state_value(self.start_state,iteration, states_values_at_iter)
        self.states_values.append(states_values_at_iter)
        return states_values_at_iter
    
    def get_state_value(self, state, iteration, states_values_at_iter):
        states_values_at_iter[str(state)] = None
        self.states_expanded += 1
        if state.terminal:
            states_values_at_iter[str(state)] = state.value          
        if not state.terminal:
            outcomes = ["out", "single", "double", "triple", "homerun"]
            successor_states = self.get_successor_states(state)
            outcome_values = self.get_outcome_values(successor_states)
            state.set_outcome_values(outcome_values)
            transition_probabilities = state.get_transition_probabilities()
            value = 0
            for outcome in outcomes:
                successor_state = successor_states[outcome]
                if str(successor_state) not in states_values_at_iter.keys():
                    states_values_at_iter = self.get_state_value(successor_state, iteration, states_values_at_iter)
                successor_value = states_values_at_iter[str(successor_state)]
                value += successor_value * transition_probabilities[outcome]
            states_values_at_iter[str(state)] = value
        return states_values_at_iter
                
    def get_new_runners_and_runs(self, outcome, state):
        runners_and_runs = {
            "first":False,
            "second":False,
            "third":False,
            "runs": state.runs
        }
        if outcome == "single":
            runners_and_runs["first"] = True
            if state.first:
                runners_and_runs["third"] = True
            if state.second:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.third:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
        elif outcome == "double":
            runners_and_runs["second"] = True
            if state.first:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.second:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.third:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
        elif outcome == "triple":
            runners_and_runs["third"] = True
            if state.first:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.second:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.third:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
        elif outcome == "homerun":
            runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.first:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.second:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
            if state.third:
                runners_and_runs["runs"] = runners_and_runs["runs"]+1
        elif outcome == "out":
            if state.second and not state.third:
                runners_and_runs["third"] = True
            elif state.second and state.third:
                runners_and_runs["second"] = True
                runners_and_runs["third"] = True
            if state.first and not runners_and_runs["second"]:
                runners_and_runs["second"] = True
            elif state.first and runners_and_runs["second"]:
                runners_and_runs["first"]=True
        return runners_and_runs 
    
    def get_successor_states(self, state):
        successor_states = {}
        new_batting_index = state.batting_index + 1
        
        #out
        if state.outs<2:
            runners_runs = self.get_new_runners_and_runs("out",state)
            successor_states["out"] = AtBat(state.pitcher, state.batting_order, new_batting_index, runners_runs["first"], runners_runs["second"], runners_runs["third"], state.outs+1, runners_runs["runs"], self.acc_matrix, self.take_model, self.swing_trans_model)
        else:
            successor_states["out"] = TerminalState(state.runs)
        #single
        runners_runs = self.get_new_runners_and_runs("single",state)
        if runners_runs["runs"]>= 10:
            successor_states["single"] = TerminalState(runners_runs["runs"])
        else:
            successor_states["single"] = AtBat(state.pitcher, state.batting_order, new_batting_index, runners_runs["first"], runners_runs["second"], runners_runs["third"], state.outs, runners_runs["runs"], self.acc_matrix, self.take_model, self.swing_trans_model)
        #double
        runners_runs = self.get_new_runners_and_runs("double",state)
        if runners_runs["runs"]>= 10:
            successor_states["double"] = TerminalState(runners_runs["runs"])
        else:
            successor_states["double"] = AtBat(state.pitcher, state.batting_order, new_batting_index, runners_runs["first"], runners_runs["second"], runners_runs["third"], state.outs, runners_runs["runs"], self.acc_matrix, self.take_model, self.swing_trans_model)
        #triple
        runners_runs = self.get_new_runners_and_runs("triple",state)
        if runners_runs["runs"]>= 10:
            successor_states["triple"] = TerminalState(runners_runs["runs"])
        else:
            successor_states["triple"] = AtBat(state.pitcher, state.batting_order, new_batting_index, runners_runs["first"], runners_runs["second"], runners_runs["third"], state.outs, runners_runs["runs"], self.acc_matrix, self.take_model, self.swing_trans_model)
        #homerun
        runners_runs = self.get_new_runners_and_runs("homerun",state)
        if runners_runs["runs"]>= 10:
            successor_states["homerun"] = TerminalState(runners_runs["runs"])
        else:
            successor_states["homerun"] = AtBat(state.pitcher, state.batting_order, new_batting_index, runners_runs["first"], runners_runs["second"], runners_runs["third"], state.outs, runners_runs["runs"], self.acc_matrix, self.take_model, self.swing_trans_model)

        return successor_states
    
    def get_outcome_values(self, successor_states):
        outcome_values = {}
        if len(self.states_values) >= 1:
            for outcome in successor_states.keys():
                outcome_values[outcome] = self.states_values[-1][str(successor_states[outcome])]
        else:
            outcome_values = {'single':1,'double':2,'triple':3,'homerun':4,'out':0}
        
        return outcome_values
                 
       