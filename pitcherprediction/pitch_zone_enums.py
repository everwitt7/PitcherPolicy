"""Module that defines enumerations for pitches, strike, ball, and obvious zones"""
from enum import Enum, unique


@unique
class StrikeZoneNames(Enum):
    """Enum for each strike zone"""
    ZERO = "0a"
    ONE = "1a"
    TWO = "2a"
    THREE = "3a"
    FOUR = "4a"
    FIVE = "5a"
    SIX = "6a"
    SEVEN = "7a"
    EIGHT = "8a"


@unique
class BallZoneNames(Enum):
    """Enum for each ball zone"""
    NINE = "9a"
    TEN = "10a"
    ELEVEN = "11a"
    TWELVE = "12a"
    THIRTEEN = "13a"
    FOURTEEN = "14a"
    FIFTEEN = "15a"
    SIXTEEN = "16a"
    ERROR = "-1"


@unique
class ObviousZoneNames(Enum):
    """Enum for each obvious zone"""
    NINE = "9b"
    TEN = "10b"
    ELEVEN = "11b"
    TWELVE = "12b"
    THIRTEEN = "13b"
    FOURTEEN = "14b"
    FIFTEEN = "15b"
    SIXTEEN = "16b"
    ERROR = "-1"


@unique
class PitchNames(Enum):
    """Enum for each pitch type we allow the pitcher to throw"""
    FOUR_SEAM = "FF"
    TWO_SEAM = "FT"
    SLIDER = "SL"
    CHANGEUP = "CH"
    CURVE = "CU"
    CUTTER = "FC"


@unique
class BatterActions(Enum):
    """Enum for all possible batter actions"""
    SWING = 'swing'
    TAKE = 'take'


@unique
class Outcomes(Enum):
    """Enum for all possible outcomes of a given count state"""
    OUT = 'out'
    HIT = 'hit'
    FOUL = 'foul'
    STRIKE = 'strike'
    BALL = 'ball'


@unique
class CountStates(Enum):
    """Enum for all count states not including terminal states"""
    ZEROZERO = '00'
    ZEROONE = '01'
    ZEROTWO = '02'
    ONEZERO = '10'
    ONEONE = '11'
    ONETWO = '12'
    TWOZERO = '20'
    TWOONE = '21'
    TWOTWO = '22'
    THREEZERO = '30'
    THREEONE = '31'
    THREETWO = '32'
