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
    ERROR = "-1"


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
