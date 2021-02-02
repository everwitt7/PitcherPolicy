"""Module that defines our Pitch classes"""
from typing import List

from zone import Zone
from zones import Zones
from obvious_zones import ObviousZones
from pitch import Pitch
from pitch_zone_enums import BallZoneNames, PitchNames, StrikeZoneNames

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

# TODO: all cutoffs currently taken from old values - need to validate then update
# TODO: create mapping from coordinate cutoffs to input JSON, the latter is currently hardcoded
# TODO: something to keep in mind, our cutoffs are based on Righty and Lefty Hitter joint data
cutoffs = {
    PitchNames.FOUR_SEEM.value: {
        BallZoneNames.NINE.value: (-1.2, 1.4),
        BallZoneNames.TEN.value: (None, 1.5),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.5, None),
        BallZoneNames.THIRTEEN.value: (1.4, None),
        BallZoneNames.FOURTEEN.value: (None, None),
        BallZoneNames.FIFTEEN.value: (None, -1.25),
        BallZoneNames.SIXTEEN.value: (None, None)
    }
}


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


ft_cutoffs = {
    BallZoneNames.NINE.value: (-1.3, 1.4),
    BallZoneNames.TEN.value: (None, 1.2),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.5, None),
    BallZoneNames.THIRTEEN.value: (1.2, None),
    BallZoneNames.FOURTEEN.value: (-1.2, -1.4),
    BallZoneNames.FIFTEEN.value: (None, -1.5),
    BallZoneNames.SIXTEEN.value: (None, None)
}

fc_cutoffs = {
    BallZoneNames.NINE.value: (None, None),
    BallZoneNames.TEN.value: (None, 1.2),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.5, 0.8),
    BallZoneNames.THIRTEEN.value: (1.6, 0.8),
    BallZoneNames.FOURTEEN.value: (-1.5, -1.8),
    BallZoneNames.FIFTEEN.value: (None, -1.9),
    BallZoneNames.SIXTEEN.value: (1.5, -1.8)
}

sl_cutoffs = {
    BallZoneNames.NINE.value: (None, None),
    BallZoneNames.TEN.value: (None, 1.2),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.4, 0.6),
    BallZoneNames.THIRTEEN.value: (1.5, 0.6),
    BallZoneNames.FOURTEEN.value: (-1.6, -2.1),
    BallZoneNames.FIFTEEN.value: (None, -2.1),
    BallZoneNames.SIXTEEN.value: (1.5, -2.2)
}

cu_cutoffs = {
    BallZoneNames.NINE.value: (None, None),
    BallZoneNames.TEN.value: (None, None),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.4, 0.5),
    BallZoneNames.THIRTEEN.value: (1.5, 0.5),
    BallZoneNames.FOURTEEN.value: (-1.3, -2.1),
    BallZoneNames.FIFTEEN.value: (None, -2.4),
    BallZoneNames.SIXTEEN.value: (1.3, -2.0)
}

ch_cutoffs = {
    BallZoneNames.NINE.value: (None, None),
    BallZoneNames.TEN.value: (None, None),
    BallZoneNames.ELEVEN.value: (None, None),
    BallZoneNames.TWELVE.value: (-1.4, 0.9),
    BallZoneNames.THIRTEEN.value: (1.5, 0.9),
    BallZoneNames.FOURTEEN.value: (-1.4, -1.8),
    BallZoneNames.FIFTEEN.value: (None, -1.8),
    BallZoneNames.SIXTEEN.value: (1.4, -1.9)
}


# TODO: clean this up or define elsewhere
norm_err_dist_params = {
    PitchNames.FOUR_SEEM.value: [0.18, 0.24],
    "SL": [0.23, 0.39],
    "FT": [0.24, 0.26],
    "CH": [0.15, 0.25],
    "CU": [0.21, 0.48],
    "FC": [0.21, 0.34]
}
err = norm_err_dist_params[PitchNames.FOUR_SEEM.value]

# TODO:maybe iterate through cutoff
"""
have cutoffs{PitchNames.FOUR_SEEM.value:{
        BallZoneNames.NINE.value: (None, None),
        BallZoneNames.TEN.value: (None, 1.2),
        BallZoneNames.ELEVEN.value: (None, None),
        BallZoneNames.TWELVE.value: (-1.5, 0.8),
        BallZoneNames.THIRTEEN.value: (1.6, 0.8),
        BallZoneNames.FOURTEEN.value: (-1.5, -1.8),
        BallZoneNames.FIFTEEN.value: (None, -1.9),
        BallZoneNames.SIXTEEN.value: (1.5, -1.8)
    }
}

Iterate through cutoffs(this is how we create each pitch, based on key)

We already have s_zone and o_zone defined, we need to create b_zones
if both the tuple = (None, None), continue because we do not need to create a zone

otherwise, we do different things FOR EACH ZONE
we just calculate width,heigh,coords on the fly...

The tricky part is zones 12 and 13 (for now this is not the case for 10 and 15)
have b_zones that are smaller than the height of the o_zone. I can probably
check if y=None, if so do something normal, else do the custom height
"""


def return_height_width_name():
    pass


def create_pitches() -> List[Pitch]:
    """Add docstring

    """
    pitches = list()

    # these remain the same for all pitches
    o_zones = ObviousZones(LEFT_X, BOT_Y)
    s_zones = list()
    for name, val in s_zone_inputs.items():
        s_zones.append(Zone(name, val["coords"], val["width"], val["height"]))

    for p_name, p_cutoffs in cutoffs.items():
        b_zones = list()
        for z_name, z_cutoffs in p_cutoffs.items():
            if z_cutoffs != (None, None):

                # TODO: each zone will be unique, the issue is some zones will have y[1] != none for 12,13
                if z_name == BallZoneNames.NINE.value:
                    coords = (z_cutoffs[0], TOP_Y)
                    width = LEFT_X - z_cutoffs[0]
                    height = z_cutoffs[1] - TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.TWELVE.value:
                    coords = (z_cutoffs[0], BOT_Y)
                    width = LEFT_X - z_cutoffs[0]
                    height = 2 * TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.TEN.value:
                    coords = (LEFT_X, TOP_Y)
                    width = 2 * RIGHT_X
                    height = z_cutoffs[1] - TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.ELEVEN.value:
                    coords = (RIGHT_X, TOP_Y)
                    width = z_cutoffs[0] - RIGHT_X
                    height = z_cutoffs[1] - TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.THIRTEEN.value:
                    coords = (RIGHT_X, BOT_Y)
                    width = z_cutoffs[0] - RIGHT_X
                    height = 2 * TOP_Y
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.FIFTEEN.value:
                    coords = (LEFT_X, z_cutoffs[1])
                    width = 2 * RIGHT_X
                    height = BOT_Y - z_cutoffs[1]
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.SIXTEEN.value:
                    coords = (RIGHT_X, z_cutoffs[1])
                    width = z_cutoffs[0] - RIGHT_X
                    height = BOT_Y - z_cutoffs[1]
                    b_zones.append(Zone(z_name, coords, width, height))

                elif z_name == BallZoneNames.FOURTEEN.value:
                    coords = (z_cutoffs[0], z_cutoffs[1])
                    width = LEFT_X - z_cutoffs[0]
                    height = BOT_Y - z_cutoffs[1]
                    b_zones.append(Zone(z_name, coords, width, height))

        zones = Zones(s_zones, b_zones, o_zones)
        pitches.append(Pitch(p_name, zones, err))

    return pitches
