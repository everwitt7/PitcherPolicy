"""Pitch Module"""

from enum import Enum, unique

from zones import Zones
from error_dist import ErrorDistribution


@unique
class PitchTypes(Enum):
    """Enum for each pitch type we allow the pitcher to throw"""
    FOUR_SEEM = 1
    TWO_SEEM = 2
    SLIDER = 3
    CHANGEUP = 4
    CURVE = 5
    CUTTER = 6


class Pitch:
    """Class used to represent Pitch

    Attributes
    ----------
    name : str
        name of the pitch
    zones: Zones
        the object used to define all zones for the pitch
    error_dist: ErrorDistribution
        the object used to define the error distribution of the pitch
    """

    def __init__(self, name: str, zones: Zones, error_dist: ErrorDistribution):
        """Instantiates Pitch object

        Parameters
        ----------
        name : str
            name of the pitch
        zones: Zones
            the object used to define all zones for the pitch
        error_dist: ErrorDistribution
            the object used to define the error distribution of the pitch
        """
        self.name = name
        self.zones = zones
        self.error_dist = error_dist

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"Pitch({repr(self.name)}, {repr(self.zones)}, {repr(self.error_dist)})"

    def __str__(self):
        """Prints pitch name, error dist, and ball zones"""
        return f"Pitch: {self.name}, Error Dist: {self.error_dist}, {self.zones}"
