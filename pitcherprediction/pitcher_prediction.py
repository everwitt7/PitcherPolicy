"""file used to run the program"""
import json

from pitch_zone_config import gen_pitches, gen_counts, gen_acc_mat, gen_trans_prob_mat, SWING_TRANS_PATH
from stochastic_game import StochasticGame

<<<<<<< HEAD

=======
>>>>>>> 0e48e36284773e5a61c6592ea1233fd971dd198f
if __name__ == "__main__":

    pitches = gen_pitches()

    swing_trans_mat = {}
    with open(SWING_TRANS_PATH) as json_file:
        swing_trans_mat = json.load(json_file)

    acc_mat = gen_acc_mat(pitches)

    trans_prob_mat = gen_trans_prob_mat(swing_trans_mat, acc_mat)

    counts = gen_counts()

    s = StochasticGame(counts, trans_prob_mat)
    s.solve_game()
