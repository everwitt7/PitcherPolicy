"""file used to run the program"""
from pitch_zone_config import generate_pitches


# TODO: State interface - just count, then count and outs, then count, outs, runners on base...
# TODO: Condition AccuracyMatrix on States

# TODO: psuedo code for all helper functions

# TODO: displayzones looks weird - make a legend or something/rethink display

if __name__ == "__main__":
    pitches = generate_pitches()
    pitches['FF'].display_zones()
