"""file used to run the program"""
import json

from pitch_zone_config import gen_pitches, gen_counts,\
    gen_acc_mat, gen_trans_prob_mat, SWING_TRANS_PATH, gen_swing_trans_matrix, gen_nn_trans_prob_mat
from stochastic_game import StochasticGame

from stochastic_game_new_trans import StochasticGame as SG

if __name__ == "__main__":
    
    pitches = gen_pitches()
    print(SWING_TRANS_PATH)
    swing_trans_mat = {}
    with open(SWING_TRANS_PATH) as json_file:
        swing_trans_mat = json.load(json_file)

    acc_mat = gen_acc_mat(pitches)
    nn_swing_trans_mat = gen_swing_trans_matrix(543037,448801)
  
    trans_prob_mat = gen_trans_prob_mat(swing_trans_mat, acc_mat)
    
    nn_trans_prob_mat = gen_nn_trans_prob_mat(nn_swing_trans_mat, acc_mat)
    print(trans_prob_mat["FF"]["1a"])
    print(nn_trans_prob_mat["FF"]["1a"])
    counts = gen_counts()

    s = StochasticGame(counts, trans_prob_mat)
    s.solve_game()

    s2 = SG(counts, nn_trans_prob_mat)
    s2.solve_game()



