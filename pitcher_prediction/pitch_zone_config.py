"""Module that defines our Pitch classes"""
from typing import List
from pathlib import Path

import tensorflow as tf
from tensorflow import keras        
import numpy as np        
import matplotlib.pyplot as plt
from tensorflow.keras import models, layers, Input, optimizers, callbacks
import json
import numpy as np


from pitches.zone import Zone
from pitches.pitch_zone_enums import BallZoneNames, PitchNames, StrikeZoneNames
from pitches.obvious_zones import ObviousZones
from pitches.zones import Zones
from pitches.pitch import Pitch
from pitches.error_dist import NormalErrorDistribution

from state_action_enums import Outcomes, CountStates, BatActs
from state import Count

# defining the absolute path to our swing_trans matrix
REL_PATH = '../data_cleaning/combining_data/swing_transitions.json'
SWING_TRANS_PATH = Path(__file__).parent / REL_PATH

# defining strike and obvious zone dimensions
LEFT_X = -0.831
MID_LEFT_X = -0.277
MID_RIGHT_X = 0.277
RIGHT_X = 0.831

TOP_Y = 1.074
MID_TOP_Y = 0.358
MID_BOT_Y = -0.358
BOT_Y = -1.074

# dimensions of our strike zones
STRIKE_HEIGHT = TOP_Y - MID_TOP_Y
STRIKE_WIDTH = RIGHT_X - MID_RIGHT_X

s_zone_inputs = {
    StrikeZoneNames.ZERO.value: {
        "coords": (LEFT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.ONE.value: {
        "coords": (MID_LEFT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.TWO.value: {
        "coords": (MID_RIGHT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.THREE.value: {
        "coords": (LEFT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.FOUR.value: {
        "coords": (MID_LEFT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.FIVE.value: {
        "coords": (MID_RIGHT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.SIX.value: {
        "coords": (LEFT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.SEVEN.value: {
        "coords": (MID_LEFT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    StrikeZoneNames.EIGHT.value: {
        "coords": (MID_RIGHT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    }
}

cutoffs = {
    PitchNames.FOUR_SEAM.value: {
        BallZoneNames.NINE.value: (-1.2, 1.4),
        BallZoneNames.TEN.value: (None, 1.5),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.5, None),
        BallZoneNames.THIRTEEN.value: (1.4, None),
        BallZoneNames.FOURTEEN.value: (None, None),
        BallZoneNames.FIFTEEN.value: (None, -1.25),
        BallZoneNames.SIXTEEN.value: (None, None)
    },
    PitchNames.TWO_SEAM.value: {
        BallZoneNames.NINE.value: (-1.3, 1.4),
        BallZoneNames.TEN.value: (None, 1.2),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.5, None),
        BallZoneNames.THIRTEEN.value: (1.2, None),
        BallZoneNames.FOURTEEN.value: (-1.2, -1.4),
        BallZoneNames.FIFTEEN.value: (None, -1.5),
        BallZoneNames.SIXTEEN.value: (None, None)
    },
    PitchNames.CUTTER.value: {
        BallZoneNames.NINE.value: (None, None),
        BallZoneNames.TEN.value: (None, 1.2),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.5, 0.8),
        BallZoneNames.THIRTEEN.value: (1.6, 0.8),
        BallZoneNames.FOURTEEN.value: (-1.5, -1.8),
        BallZoneNames.FIFTEEN.value: (None, -1.9),
        BallZoneNames.SIXTEEN.value: (1.5, -1.8)
    },
    PitchNames.SLIDER.value: {
        BallZoneNames.NINE.value: (None, None),
        BallZoneNames.TEN.value: (None, 1.2),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.4, 0.6),
        BallZoneNames.THIRTEEN.value: (1.5, 0.6),
        BallZoneNames.FOURTEEN.value: (-1.6, -2.1),
        BallZoneNames.FIFTEEN.value: (None, -2.1),
        BallZoneNames.SIXTEEN.value: (1.5, -2.2)
    },
    PitchNames.CURVE.value: {
        BallZoneNames.NINE.value: (None, None),
        BallZoneNames.TEN.value: (None, None),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.4, 0.5),
        BallZoneNames.THIRTEEN.value: (1.5, 0.5),
        BallZoneNames.FOURTEEN.value: (-1.3, -2.1),
        BallZoneNames.FIFTEEN.value: (None, -2.4),
        BallZoneNames.SIXTEEN.value: (1.3, -2.0)
    },
    PitchNames.CHANGEUP.value: {
        BallZoneNames.NINE.value: (None, None),
        BallZoneNames.TEN.value: (None, None),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.4, 0.9),
        BallZoneNames.THIRTEEN.value: (1.5, 0.9),
        BallZoneNames.FOURTEEN.value: (-1.4, -1.8),
        BallZoneNames.FIFTEEN.value: (None, -1.8),
        BallZoneNames.SIXTEEN.value: (1.4, -1.9)
    }
}

norm_err_dist = {
    PitchNames.FOUR_SEAM.value: NormalErrorDistribution(0.18, 0.24),
    PitchNames.TWO_SEAM.value: NormalErrorDistribution(0.24, 0.26),
    PitchNames.CUTTER.value: NormalErrorDistribution(0.21, 0.34),
    PitchNames.SLIDER.value: NormalErrorDistribution(0.23, 0.39),
    PitchNames.CURVE.value: NormalErrorDistribution(0.21, 0.48),
    PitchNames.CHANGEUP.value: NormalErrorDistribution(0.15, 0.25)
}


def gen_pitches() -> List[Pitch]:
    """Instantiates all of our Pitch objects (by instantiating zone, obvious_zones, and zones)

    Returns
    -------
    List[Pitch]
        a list of all our Pitch objects
    """
    pitches = {}

    # these remain the same for all pitches
    o_zones = ObviousZones(LEFT_X, BOT_Y)
    s_zones = list()
    for name, val in s_zone_inputs.items():
        s_zones.append(Zone(name, val["coords"], val["width"], val["height"]))

    for p_name, p_cutoffs in cutoffs.items():
        b_zones = list()
        for z_name, z_cuts in p_cutoffs.items():
            if z_cuts != (None, None):

                if z_name == BallZoneNames.NINE.value:
                    coords = (z_cuts[0], TOP_Y)
                    width = LEFT_X-z_cuts[0]
                    height = z_cuts[1]-TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.TWELVE.value:
                    coords = (z_cuts[0], BOT_Y)
                    width = LEFT_X-z_cuts[0]
                    height = 2*TOP_Y if z_cuts[1] is None else z_cuts[1]+TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.TEN.value:
                    coords = (LEFT_X, TOP_Y)
                    width = 2*RIGHT_X
                    height = z_cuts[1]-TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.ELEVEN.value:
                    coords = (RIGHT_X, TOP_Y)
                    width = z_cuts[0]-RIGHT_X
                    height = z_cuts[1]-TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.THIRTEEN.value:
                    coords = (RIGHT_X, BOT_Y)
                    width = z_cuts[0]-RIGHT_X
                    height = 2*TOP_Y if z_cuts[1] is None else z_cuts[1]+TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.FIFTEEN.value:
                    coords = (LEFT_X, z_cuts[1])
                    width = 2*RIGHT_X
                    height = BOT_Y-z_cuts[1]
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.SIXTEEN.value:
                    coords = (RIGHT_X, z_cuts[1])
                    width = z_cuts[0]-RIGHT_X
                    height = BOT_Y-z_cuts[1]
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.FOURTEEN.value:
                    coords = (z_cuts[0], z_cuts[1])
                    width = LEFT_X-z_cuts[0]
                    height = BOT_Y-z_cuts[1]
                    b_zones.append(Zone(z_name, coords, width, height))

        zones = Zones(s_zones, b_zones, o_zones)
        pitches[p_name] = Pitch(p_name, zones, norm_err_dist[p_name])

    return pitches


def gen_counts() -> List[Count]:
    """Instantiates all of our Count state objects

    Returns
    -------
    List[Count]
        a list of all our Count state objects
    """
    return [Count(Outcomes, int(c.value[0]), int(c.value[1])) for c in CountStates]


def gen_swing_trans_matrix(pitcher_id,batter_id):
    """Creates swing transition matrix indexed by pitch type and count for a given pitcher/batter combination
    Returns
    _______
    dict
        a transition matrix dict to index [pitch_type][pitch_zone][s_count][b_count] = [prob_strike,prob_foul,prob_out,prob_hit]
    """
    #load pitcher tensors
    file = open("../pitcher_tensors.json")
    pitcher_tensors = json.load(file)
    pitcher = np.array(pitcher_tensors[str(pitcher_id)])
    file.close()
    #load batter tensors
    file = open("../batter_tensors.json")
    batter_tensors = json.load(file)
    batter = batter_tensors[str(batter_id)]
    file.close()
    #load model
    model = models.load_model("../transition_model_2015-2019.h5")
    #instantiate the dict
    swing_transition_matrix = {}
    #iterate over list of pitch types
    for pitch_type in ["FF", "FT", "CU", "CH", "FC", "SL"]:
        #iterate over zones
        swing_transition_matrix[pitch_type] = {}
        for zone in range(17):
            zone_key = str(zone) + "a"
            #generate pitch matrix
            pitch_tensor = get_pitch_matrix(zone, pitch_type)
            #iterate over s_count
            swing_transition_matrix[pitch_type][zone_key] = {}

            if zone >= 9 :
                swing_transition_matrix[pitch_type][str(zone)+"b"] = {}
            for s_count in range(3):
                #iterate over b_count
                swing_transition_matrix[pitch_type][zone_key][s_count] = {}
                if zone >= 9 :
                    swing_transition_matrix[pitch_type][str(zone)+"b"][s_count] = {}
                for b_count in range(4):
                    #generate prediction from model
                    prediction = model.predict([np.array([pitcher]),np.array([batter]),np.array([s_count]),np.array([b_count]),np.array([pitch_tensor])])[0]
                    cleaned_prediction = {
                        Outcomes.OUT.value: prediction[2],
                        Outcomes.HIT.value: prediction[3],
                        Outcomes.FOUL.value: prediction[1],
                        Outcomes.STRIKE.value: prediction[0]
                    }
                    swing_transition_matrix[pitch_type][zone_key][s_count][b_count] = cleaned_prediction
                    if zone >= 9 :
                        swing_transition_matrix[pitch_type][str(zone)+"b"][s_count][b_count] = {Outcomes.BALL.value:1}

                    
    #return dict
    return swing_transition_matrix

def get_pitch_matrix(zone, pitch_type):
    pitch_types = ["FF", "FT", "CU", "CH", "FC", "SL"]
    pitch_tensor = np.zeros((5,5,6))
    p_ind = pitch_types.index(pitch_type)
    zone_index_map = {
        0:(1,1), #(x,y)
        1:(2,1),
        2:(3,1),
        3:(1,2),
        4:(2,2),
        5:(3,2),
        6:(1,3),
        7:(2,3),
        8:(3,3),
        9:(0,0),
        10:(np.s_[1:4],0),
        11:(4,0),
        12:(0,np.s_[1:4]),
        13:(4,np.s_[1:4]),
        14:(0,4),
        15:(np.s_[1:4],4),
        16:(4,4)
    }
    pitch_tensor[zone_index_map[zone][0],zone_index_map[zone][1], p_ind] = 1
   
    return pitch_tensor
def gen_acc_mat(pitches: List[Pitch]) -> dict:
    """Generates accuracy matrix by running error simulation for each pitch

    Parameters
    ----------
    pitches : List[Pitch]
        the list pitches a pitcher may throw

    Returns
    -------
    dict
        an accuracy matrix dict to index [pitch][int_zone][act_zone] = %in_act_zone
    """
    acc_mat = {}
    for p_name, pitch in pitches.items():
        acc_mat[p_name] = pitch.run_error_simuation()
    
    return acc_mat


def gen_trans_prob_mat(swing_trans_mat: dict, acc_mat: dict) -> dict:
    """Generates tansition probability matrix

    Parameters
    ----------
    swing_trans_mat : dict
        dict that defines the probability of an outcome (foul, swing, out, hit, ball)
        access probs by swing_trans_mat[pitch][zone][outcome] = %outcome
    acc_mat : dict
        dict that defines the accuracy matrix dict[pitch][int_zone][act_zone] = %in_act

    Returns
    -------
    dict
        a trans_prob_mat that contains the transition probabilities across all outcomes
        for a given pitcher and batter action; trans_prob_mat[pitch][zone][swing] = outcome probs
    """
    trans_prob_mat = {}
   
    for pitch, zones in swing_trans_mat.items():
        trans_prob_mat[pitch] = {}

        for int_zone in zones:
            trans_prob_mat[pitch][int_zone] = {
                BatActs.TAKE.value: {
                    Outcomes.STRIKE.value: 0,
                    Outcomes.BALL.value: 0
                },
                BatActs.SWING.value: {
                    Outcomes.OUT.value: 0,
                    Outcomes.HIT.value: 0,
                    Outcomes.FOUL.value: 0,
                    Outcomes.STRIKE.value: 0,
                    Outcomes.BALL.value: 0
                }
            }
          
            if int_zone[-1] == 'b':
                trans_prob_mat[pitch][int_zone][BatActs.TAKE.value][Outcomes.BALL.value] = 1

            # pitches for which we ran an error simulation
            if int_zone in acc_mat[pitch]:

                for s_zone in [s.value for s in StrikeZoneNames]:
                    if s_zone in acc_mat[pitch][int_zone]:
                        trans_prob_mat[pitch][int_zone][BatActs.TAKE.value][Outcomes.STRIKE.value]\
                            += acc_mat[pitch][int_zone][s_zone]
                trans_prob_mat[pitch][int_zone][BatActs.TAKE.value][Outcomes.BALL.value] =\
                    1-trans_prob_mat[pitch][int_zone][BatActs.TAKE.value][Outcomes.STRIKE.value]

                for act_zone, prob_in_zone in acc_mat[pitch][int_zone].items():

                    for outcome, prob_outcome in swing_trans_mat[pitch][act_zone].items():

                        trans_prob_mat[pitch][int_zone][BatActs.SWING.value][outcome]\
                            += prob_in_zone * prob_outcome
            else:
                trans_prob_mat[pitch][int_zone][BatActs.SWING.value]\
                    = swing_trans_mat[pitch][int_zone]
  
    return trans_prob_mat


def gen_nn_trans_prob_mat(swing_trans_mat: dict, acc_mat: dict) -> dict:
    """Generates tansition probability matrix

    Parameters
    ----------
    swing_trans_mat : dict
        dict that defines the probability of an outcome (foul, swing, out, hit, ball)
        access probs by swing_trans_mat[pitch][zone][outcome] = %outcome
    acc_mat : dict
        dict that defines the accuracy matrix dict[pitch][int_zone][act_zone] = %in_act

    Returns
    -------
    dict
        a trans_prob_mat that contains the transition probabilities across all outcomes
        for a given pitcher and batter action; trans_prob_mat[pitch][zone][swing] = outcome probs
    """
    trans_prob_mat = {}

    for pitch in swing_trans_mat.keys():
        trans_prob_mat[pitch] = {}

        for int_zone in swing_trans_mat[pitch].keys():
            trans_prob_mat[pitch][int_zone] = {}

            for s_count in swing_trans_mat[pitch][int_zone].keys():
                trans_prob_mat[pitch][int_zone][s_count] = {}

                for b_count in swing_trans_mat[pitch][int_zone][s_count].keys():
        
                    trans_prob_mat[pitch][int_zone][s_count][b_count] = {
                        BatActs.TAKE.value: {
                            Outcomes.STRIKE.value: 0,
                            Outcomes.BALL.value: 0
                        },
                        BatActs.SWING.value: {
                            Outcomes.OUT.value: 0,
                            Outcomes.HIT.value: 0,
                            Outcomes.FOUL.value: 0,
                            Outcomes.STRIKE.value: 0,
                            Outcomes.BALL.value: 0
                        }
                    }
                    if int_zone[-1] == 'b':
                       trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.TAKE.value][Outcomes.BALL.value] = 1
                    if int_zone in acc_mat[pitch]:

                        for s_zone in [s.value for s in StrikeZoneNames]:
                            if s_zone in acc_mat[pitch][int_zone]:
                                trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.TAKE.value][Outcomes.STRIKE.value]\
                                    += acc_mat[pitch][int_zone][s_zone]

                        trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.TAKE.value][Outcomes.BALL.value] =\
                            1-trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.TAKE.value][Outcomes.STRIKE.value]

                        for act_zone, prob_in_zone in acc_mat[pitch][int_zone].items():
                        
                            #print(swing_trans_mat[pitch])
                            #print(swing_trans_mat[pitch][act_zone])
                            #print(swing_trans_mat[pitch][act_zone][s_count])
                            #print(swing_trans_mat[pitch][act_zone][s_count][b_count])
                            for outcome, prob_outcome in swing_trans_mat[pitch][act_zone][s_count][b_count].items():

                                trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.SWING.value][outcome]\
                                    += prob_in_zone * prob_outcome
                    else:
                        trans_prob_mat[pitch][int_zone][s_count][b_count][BatActs.SWING.value]\
                            = swing_trans_mat[pitch][int_zone][s_count][b_count]
    
    return trans_prob_mat




    