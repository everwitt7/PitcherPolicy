"""file used to run the program"""
from pitch_zone_config import generate_pitches

# TODO: clean up this garbage code - move constants into config.py file
# TODO: create a config to create Zones for each Pitch

# TODO: State interface - just count, then count and outs, then count, outs, runners on base...
# TODO: Condition AccuracyMatrix on States

# TODO: pseudo code for all csv cleaning functions
# TODO: psuedo code for all helper functions

# TODO: displayzones looks weird - make a legend or something/rethink display

if __name__ == "__main__":
    pitches = generate_pitches()
    pitches[4].display_zones()
