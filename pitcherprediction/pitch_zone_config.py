"""Module that defines our Pitch classes"""
from typing import List

from zone import Zone
from zones import Zones
from obvious_zones import ObviousZones
from pitch import Pitch
from pitch_zone_enums import BallZoneNames, PitchNames, StrikeZoneNames
from error_dist import NormalErrorDistribution

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


def generate_pitches() -> List[Pitch]:
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
