# Data

## ./combining-data/swing_trans.json

A dictionary that contains the transition probabilities given a batter and pitcher action. The dictionary represents pr(outcome|p_action, b_action), where p_action is comprised of a pitch type and zone location, and b_action is always swing. The five outcomes are [out, base, strike, foul, ball], pitches are [FF, FT, FC, SL, CH, CU] and zones are [0a, 1a, 2a, 3a, 4a, 5a, 6a, 7a, 8a, 9b, 10b, 11b, 12b, 13b, 14b, 15b, 16b] (and some ball zones that are not included). To access pr(outcome|p_action, b_action) you index swing_trans[pitch][zone][outcome]