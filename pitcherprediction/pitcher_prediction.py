"""file used to run the program"""
import json

from pitch_zone_config import gen_acc_mat, generate_pitches, gen_trans_prob_mat, SWING_TRANS_PATH


# TODO: State interface - just count, then count and outs, then count, outs, runners on base...
# TODO: Condition AccuracyMatrix on States
# TODO: displayzones looks weird - make a legend or something/rethink display
# TODO: change jupyter paths to from pathlib import Path then abs=Path(__file__).parent / relpath
# TODO: makes a pitch module


if __name__ == "__main__":

    pitches = generate_pitches()
    pitches['FF'].display_zones()

    # swing_trans_mat = {}
    # with open(SWING_TRANS_PATH) as json_file:
    # swing_trans_mat = json.load(json_file)

    # acc_mat = gen_acc_mat(pitches)
    # print(acc_mat)

    # trans_prob_mat = gen_trans_prob_mat(swing_trans_mat, acc_mat)
    # parsed = json.loads(trans_prob_mat)
    # print(json.dumps(parsed, indent=2, sort_keys=True))
