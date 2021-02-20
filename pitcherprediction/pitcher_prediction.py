"""file used to run the program"""
import json

from pitch_zone_config import gen_pitches, gen_counts,\
    gen_acc_mat, gen_trans_prob_mat, SWING_TRANS_PATH


# TODO: State interface - just count, then count and outs, then count, outs, runners on base...
# TODO: Condition AccuracyMatrix on States
# TODO: displayzones looks weird - make a legend or something/rethink display
# TODO: change jupyter paths to from pathlib import Path then abs=Path(__file__).parent / relpath
# TODO: make a pitch module that contains Zone, ObviousZone, ErrorDist, and Pitch information
# TODO: add barcharts to make the outcome/transition probabilities easy to understand visually


if __name__ == "__main__":

    pitches = gen_pitches()
    # pitches['FF'].display_zones()

    # TODO: update the cleaning files so that swing transitions.json is in data-cleaning
    # TODO: instead of using strings use enums for zones
    swing_trans_mat = {}
    with open(SWING_TRANS_PATH) as json_file:
        swing_trans_mat = json.load(json_file)
    acc_mat = gen_acc_mat(pitches)
    trans_prob_mat = gen_trans_prob_mat(swing_trans_mat, acc_mat)
    print(trans_prob_mat)

    counts = gen_counts()
    # print(counts)
