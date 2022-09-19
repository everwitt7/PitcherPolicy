
from tensorflow.keras import models
import json
from inning import Inning


def create_tensor_list_from_ids(ids):
    with open("../tensors/batter_tensors.json") as f:
        batter_tensors = json.load(f)
    tensor_list = []
    for id in ids:
        tensor_list.append(batter_tensors[id])
    return tensor_list

if __name__ == "__main__":
        # load pitcher tensors
    with open("../tensors/pitcher_tensors.json") as f:
        pitcher_tensors = json.load(f)
    # load batter tensors

    
    take_model = models.load_model("../models/take_2015-2018.h5")
    swing_trans_model = models.load_model("../models/transition_model_expanded_outcomes.h5")
    acc_model = models.load_model("../models/error_2015-2018.h5")

    batting_order_ids = ['572761','641933','502671','571448','405395','572816','657557','425877','542303'] 
    batting_order = create_tensor_list_from_ids(batting_order_ids)
    
    pitcher_id = '607536'
    pitcher = pitcher_tensors[pitcher_id]
    

    inning = Inning(pitcher, batting_order, take_model, swing_trans_model, acc_model)
    inning.solve_inning()




