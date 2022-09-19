"""file used to run the program"""
import json
import numpy as np
from tensorflow.keras import models

from pitch_zone_config import (
    gen_pitches,
    gen_counts,
    gen_acc_mat,
    gen_trans_prob_mat,
    SWING_TRANS_PATH,
    NN_SWING_TRANS_PATH,
    gen_swing_trans_matrix,
    gen_take_mat
)
from stochastic_game import StochasticGame


if __name__ == "__main__":


    # load pitcher tensors
    with open("../tensors/pitcher_tensors.json") as f:
        pitcher_tensors = json.load(f)
        

    # load batter tensors
    with open("../tensors/batter_tensors.json") as f:
        batter_tensors = json.load(f)
    # open 3 TensorFlow models
    take_model = models.load_model("../models/take_2015-2018.h5")
    #swing_trans_model = models.load_model("../models/transition_model_2015-2018.h5")
    swing_trans_model = models.load_model("../models/transition_model_expanded_outcomes.h5")
    acc_model = models.load_model("../models/error_2015-2018.h5")

    # Set pitcher/batter matchup for the at bat
    pitcher_id, batter_id = 543037, 448801 #Gerrit Cole, Chris Davis

    pitcher = np.array(pitcher_tensors[str(pitcher_id)])
    batter = np.array(batter_tensors[str(batter_id)])

    pitches = gen_pitches()
    counts = gen_counts()
    
    acc_mat = gen_acc_mat(acc_model,pitcher,pitches)
    take_mat = gen_take_mat(take_model, batter, pitches, .2)
    nn_swing_trans_mat = gen_swing_trans_matrix(swing_trans_model, pitcher, batter, take_mat, pitches)
    nn_trans_prob_mat = gen_trans_prob_mat(nn_swing_trans_mat, acc_mat, take_mat)
    outcome_values = {"single":3,"double":5,"triple":8,"homerun":10}
    s1 = StochasticGame(counts, nn_trans_prob_mat, outcome_values)
    
    s1_vals, s1_pol, s1_outcome_probs = s1.solve_game()


    """
    FOR AGGREGATE TESTING

    selected_thirds =  {'pitchers': {0: [527048, 451596, 501957, 503449, 543022, 460059, 606131, 430912, 453385, 446321, 571800, 572096, 628333, 430580, 572750, 554234, 605541, 605156, 643230, 425386], 1: [489119, 430935, 502043, 592662, 543699, 488768, 461829, 282332, 518633, 608379, 502327, 519455, 434538, 467100, 573186, 458681, 425794, 433587, 592717, 605200], 2: [453286, 452657, 518516, 519242, 527054, 434378, 519144, 500779, 502042, 425844, 594798, 453562, 545333, 502188, 571666, 543294, 477132, 572971, 457918, 544931]}, 'batters': {0: [572287, 429667, 488721, 595978, 543376, 425784, 506560, 542208, 425772, 408299, 572204, 435064, 543216, 641525, 592444, 431171, 571912, 596143, 542194, 571974], 1: [453943, 448801, 405395, 446334, 520471, 516770, 607680, 435622, 543063, 596059, 430945, 457803, 545341, 608365, 595281, 500871, 578428, 461314, 571740, 474568], 2: [502671, 467793, 458015, 605141, 545361, 593428, 592178, 547180, 547989, 518626, 453568, 519203, 474832, 572821, 592518, 518934, 543333, 451594, 429665, 458731]}}


   
    
    

    outcomes_total = {}
    results = {}
    for i in selected_thirds["pitchers"].keys():
        for j in selected_thirds["batters"].keys():
            group_key =str(i)+str(j)
            outcomes_total[group_key] = {}
            results[group_key] = {}
            for b_count in range(4):
                for s_count in range(3):
                    count = str(b_count)+str(s_count)
                    results[group_key][count] = None
                    outcomes_total[group_key][count] = np.array([])

    counter = 0

    for i in selected_thirds["pitchers"].keys():
        for j in selected_thirds["batters"].keys():
            group_key =str(i)+str(j)
            
            for pitcher_id in selected_thirds["pitchers"][i]:
                for batter_id in selected_thirds["batters"][j]:
                    matchup = (str(pitcher_id), str(batter_id))
                    pitches = gen_pitches()
                    counts = gen_counts()

                    pitcher = np.array(pitcher_tensors[str(pitcher_id)])
                    batter = np.array(batter_tensors[str(batter_id)])

                    acc_mat = gen_acc_mat(acc_model,pitcher,pitches)
                    take_mat = gen_take_mat(take_model, batter, pitches, .2)
                    nn_swing_trans_mat = gen_swing_trans_matrix(swing_trans_model, pitcher, batter, take_mat, pitches)
                    nn_trans_prob_mat = gen_trans_prob_mat(nn_swing_trans_mat, acc_mat, take_mat)
                
                    s1 = StochasticGame(counts, nn_trans_prob_mat)
                    
                    s1_vals, s1_pol = s1.solve_game()
                    for count in s1_vals.keys():
                        state_val = s1_vals[count][-1]
                        outcomes_total[group_key][count] = np.append(outcomes_total[group_key][count], (state_val,matchup))
                    print(counter)
                    counter += 1


                    
    for i in selected_thirds["pitchers"].keys():
        for j in selected_thirds["batters"].keys():
            group_key =str(i)+str(j)
            for count in outcomes_total[group_key].keys():
                results[group_key][count] = outcomes_total[group_key][count].tolist()
    with open("value_iter_outcomes.json", "w") as outfile: 
        json.dump(results, outfile)
    print("SAVED")
    """      
   
          