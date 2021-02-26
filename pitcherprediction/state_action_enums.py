"""Module that defines enumerations for batter actions, outcomes, and count state"""
from enum import Enum, unique


@unique
class BatActs(Enum):
    """Enum for all possible batter actions"""
    SWING = "swing"
    TAKE = "take"


@unique
class Outcomes(Enum):
    """Enum for all possible outcomes of a given count state"""
    OUT = "out"
    HIT = "hit"
    FOUL = "foul"
    STRIKE = "strike"
    BALL = "ball"


@unique
class CountStates(Enum):
    """Enum for all count states not including terminal states"""
    ZEROZERO = "00"
    ZEROONE = "01"
    ZEROTWO = "02"
    ONEZERO = "10"
    ONEONE = "11"
    ONETWO = "12"
    TWOZERO = "20"
    TWOONE = "21"
    TWOTWO = "22"
    THREEZERO = "30"
    THREEONE = "31"
    THREETWO = "32"
