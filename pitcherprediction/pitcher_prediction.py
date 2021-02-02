"""file used to run the program"""
from pitch_zone_config import create_pitches

# TODO: clean up this garbage code - move constants into config.py file
# TODO: create a config to create Zones for each Pitch

# TODO: State interface - just count, then count and outs, then count, outs, runners on base...
# TODO: Condition AccuracyMatrix on States

# TODO: pseudo code for all csv cleaning functions
# TODO: psuedo code for all helper functions

if __name__ == "__main__":
    ff = create_pitches()
    ff.display_zones()
