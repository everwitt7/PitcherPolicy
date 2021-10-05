"""Config file for tests"""
from pitches.obvious_zones import ObviousZones
from pitches.zone import Zone
from pitches.zones import Zones
from pitches.error_dist import NormalErrorDistribution

LEFT_X = -3
MID_LEFT_X = -1
MID_RIGHT_X = 1
RIGHT_X = 3

TOP_Y = 3
MID_TOP_Y = 1
MID_BOT_Y = -1
BOT_Y = -3

strike_zone_inputs = {
    "0a": {
        "coords": (LEFT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "1a": {
        "coords": (MID_LEFT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "2a": {
        "coords": (MID_RIGHT_X, MID_TOP_Y),
        "height": 2,
        "width": 2
    },
    "3a": {
        "coords": (LEFT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "4a": {
        "coords": (MID_LEFT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "5a": {
        "coords": (MID_RIGHT_X, MID_BOT_Y),
        "height": 2,
        "width": 2
    },
    "6a": {
        "coords": (LEFT_X, BOT_Y),
        "height": 2,
        "width": 2
    },
    "7a": {
        "coords": (MID_LEFT_X, BOT_Y),
        "height": 2,
        "width": 2
    },
    "8a": {
        "coords": (MID_RIGHT_X, BOT_Y),
        "height": 2,
        "width": 2
    }
}
ball_zone_inputs = {
    "10a": {
        "coords": (LEFT_X, TOP_Y),
        "height": 1,
        "width": 6
    },
    "11a": {
        "coords": (RIGHT_X, TOP_Y),
        "height": 1,
        "width": 1
    },
    "13a": {
        "coords": (RIGHT_X, BOT_Y),
        "height": 5,
        "width": 1
    },
    "9a": {
        "coords": (-1+LEFT_X, TOP_Y),
        "height": 1,
        "width": 1
    },
    "12a": {
        "coords": (-1+LEFT_X, BOT_Y),
        "height": 5,
        "width": 1
    },
    "15a": {
        "coords": (LEFT_X, -1+BOT_Y),
        "height": 1,
        "width": 6
    },
    "16a": {
        "coords": (RIGHT_X, -1+BOT_Y),
        "height": 1,
        "width": 1
    },
    "14a": {
        "coords": (-1+LEFT_X, -1+BOT_Y),
        "height": 1,
        "width": 1
    }
}

STRIKE_ZONES = list()
BALL_ZONES = list()
OBV_ZONES = ObviousZones(LEFT_X, TOP_Y)


for name, val in strike_zone_inputs.items():
    STRIKE_ZONES.append(
        Zone(name, val["coords"], val["width"], val["height"]))

for name, val in ball_zone_inputs.items():
    BALL_ZONES.append(
        Zone(name, val["coords"], val["width"], val["height"]))

TEST_ZONES = Zones(STRIKE_ZONES, BALL_ZONES, OBV_ZONES)

TEST_ERR_DIST = NormalErrorDistribution(1, 1)
