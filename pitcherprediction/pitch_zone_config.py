"""Module that defines our Pitch classes"""
from typing import List

from zone import Zone
from zones import Zones
from obvious_zones import ObviousZones
from pitch import Pitch
from pitch_zone_enums import BallZoneNames, PitchNames, StrikeZoneNames

# defining the bounds of our strike and obvious zones
LEFT_X = -0.831
MID_LEFT_X = -0.277
MID_RIGHT_X = 0.277
RIGHT_X = 0.831

TOP_Y = 1.074
MID_TOP_Y = 0.358
MID_BOT_Y = -0.358
BOT_Y = -1.074

# creating the dimensions of our strike zones
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

# these are the values we update, not the inputs JSON
# TODO: change NONE... but if there are None here, than there are None in inputs...
ff_cutoffs = {
    BallZoneNames.NINE.value: (-1.2, 1.4),
    BallZoneNames.TEN.value: (None, 1.5),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.5, None),
    BallZoneNames.THIRTEEN.value: (1.4, None),
    BallZoneNames.FOURTEEN.value: (None, None),
    BallZoneNames.FIFTEEN.value: (None, -1.25),
    BallZoneNames.SIXTEEN.value: (None, None)
}

ff_b_zone_inputs = {
    BallZoneNames.NINE.value: {
        "coords": (-1.2, TOP_Y),
        "height": 1.4-TOP_Y,
        "width": LEFT_X-(-1.2)
    },
    BallZoneNames.TWELVE.value: {
        "coords": (-1.5, BOT_Y),
        "height": 2*TOP_Y,
        "width": LEFT_X-(-1.5)
    },
    BallZoneNames.TEN.value: {
        "coords": (LEFT_X, TOP_Y),
        "height": 1.5-TOP_Y,  # the 1.5 is what can change
        "width": 2*RIGHT_X  # this can change
    },
    BallZoneNames.THIRTEEN.value: {
        "coords": (RIGHT_X, BOT_Y),
        "height": 2*TOP_Y,
        "width": 1.4-RIGHT_X
    },
    BallZoneNames.FIFTEEN.value: {
        "coords": (LEFT_X, -1.25),
        "height": BOT_Y-(-1.25),
        "width": 2*RIGHT_X
    }
}


ft_cutoffs = {}

fc_cutoffs = {}

sl_cutoffs = {}

cu_cutoffs = {}

ch_cutoffs = {}

# TODO: clean this up or define elsewhere
norm_err_dist_params = {
    PitchNames.FOUR_SEEM.value: [0.18, 0.24],
    "SL": [0.23, 0.39],
    "FT": [0.24, 0.26],
    "CH": [0.15, 0.25],
    "CU": [0.21, 0.48],
    "FC": [0.21, 0.34],
    "SI": [0.24, 0.28]
}


# I need to create a big JSON to go from those coordinates to rectangle notation to create Zone objects
# I need left/right/top/bottom for Obvious_Zone object

def create_pitches() -> List[Pitch]:
    """Add docstring

    """
    s_zones = list()
    b_zones = list()
    o_zones = ObviousZones(LEFT_X, BOT_Y)

    for name, val in s_zone_inputs.items():
        s_zones.append(Zone(name, val["coords"], val["width"], val["height"]))

    for name, val in ff_b_zone_inputs.items():
        b_zones.append(Zone(name, val["coords"], val["width"], val["height"]))

    zones = Zones(s_zones, b_zones, o_zones)

    return Pitch(PitchNames.FOUR_SEEM.value, zones,
                 norm_err_dist_params[PitchNames.FOUR_SEEM.value])
