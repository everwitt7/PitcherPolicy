"""file used to run the program"""
from zones import Zones, ObviousZones, Zone


# These constants are all based on the diagram of our general strike zone
# we would want zone_coords_config.json file or something
LEFT_X = -0.831
MID_LEFT_X = -0.277
MID_RIGHT_X = 0.277
RIGHT_X = 0.831

TOP_Y = 1.074
MID_TOP_Y = 0.358
MID_BOT_Y = -0.358
BOT_Y = -1.074

# Arbitrary Zone Definitions - For Assertion Testing -
# ORDER SHOULD BE WIDTH THEN HEIGHT (we do (x,y) for coordinates, so stay consistent x before y)
STRIKE_HEIGHT = TOP_Y - MID_TOP_Y
STRIKE_WIDTH = RIGHT_X - MID_RIGHT_X

strike_zone_inputs = {
    "0a": {
        "coords": (LEFT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "1a": {
        "coords": (MID_LEFT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "2a": {
        "coords": (MID_RIGHT_X, MID_TOP_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "3a": {
        "coords": (LEFT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "4a": {
        "coords": (MID_LEFT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "5a": {
        "coords": (MID_RIGHT_X, MID_BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "6a": {
        "coords": (LEFT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "7a": {
        "coords": (MID_LEFT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    },
    "8a": {
        "coords": (MID_RIGHT_X, BOT_Y),
        "height": STRIKE_HEIGHT,
        "width": STRIKE_WIDTH
    }
}

ball_10_11_13_inputs = {
    "10a": {
        "coords": (LEFT_X, TOP_Y),
        "height": 0.4,
        "width": RIGHT_X*2
    },
    "11a": {
        "coords": (RIGHT_X, TOP_Y),
        "height": 0.4,
        "width": 0.3
    },
    "13a": {
        "coords": (RIGHT_X, BOT_Y),
        "height": 1.8,
        "width": 0.3
    }
}

ball_9_12_inputs = {
    "9a": {
        "coords": (-1.1, TOP_Y),
        "height": 0.4,
        "width": abs(-1.1-LEFT_X)
    },
    "12a": {
        "coords": (-1.1, BOT_Y),
        "height": 1.8,
        "width": abs(-1.1-LEFT_X)
    }
}

ball_15_16_inputs = {
    "15a": {
        "coords": (LEFT_X, -1.5),
        "height": abs(-1.5-BOT_Y),
        "width": RIGHT_X*2
    },
    "16a": {
        "coords": (RIGHT_X, -1.5),
        "height": abs(-1.5-BOT_Y),
        "width": 0.3
    }
}

ball_14_inputs = {
    "14a": {
        "coords": (-1.1, -1.5),
        "height": abs(-1.5-BOT_Y),
        "width": abs(-1.1-LEFT_X)
    }
}


if __name__ == "__main__":
    strike_zones = list()
    ball_zones = list()

    for name, v in strike_zone_inputs.items():
        strike_zones.append(Zone(name, v["coords"], v["width"], v["height"]))

    for name, v in ball_10_11_13_inputs.items():
        ball_zones.append(Zone(name, v["coords"], v["width"], v["height"]))

    for name, v in ball_9_12_inputs.items():
        ball_zones.append(Zone(name, v["coords"], v["width"], v["height"]))

    for name, v in ball_15_16_inputs.items():
        ball_zones.append(Zone(name, v["coords"], v["width"], v["height"]))

    for name, v in ball_14_inputs.items():
        ball_zones.append(Zone(name, v["coords"], v["width"], v["height"]))

    obvious_zones = ObviousZones(LEFT_X, BOT_Y)
    myzones = Zones(strike_zones, ball_zones, obvious_zones)
    myzones.display_zones()
