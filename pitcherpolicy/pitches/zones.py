"""Zones Module"""
from typing import List

from pitches.obvious_zones import ObviousZones
from pitches.zone import Zone


class Zones:
    """Class used to represent Zones

    Attributes
    ----------
    strike_zones : List[Zone]
        the list of zones that define a strike zone
    ball_zones: List[Zone]
        the list of zones that dfine ball zones
    obvious_zones: ObviousZones
        the object used to define all obvious zones

    Methods
    -------
    in_strike_zone(x_coord, y_coord)
        returns true if (x_coord, y_coord) are in a strike zone
    in_ball_zone(x_coord, y_coord)
        returns true if (x_coord, y_coord) are in a ball zone
    in_obvious_zone(x_coord, y_coord)
        returns true if (x_coord, y_coord) are in an obvious zone
    return_zone(x_coord, y_coord)
        returns the name of the zone the coords are in
    """

    def __init__(self, strike_zones: List[Zone],
                 ball_zones: List[Zone],
                 obvious_zones: ObviousZones) -> None:
        """Instantiates Zones object

        Parameters
        ----------
        strike_zones : float
            the list of zones that define a strike zone
        ball_zones: float
            the list of zones that define a ball zone
        obvious_zones: float
            the object used to define all obvious zones
        """
        self.strike_zones = strike_zones
        self.ball_zones = ball_zones
        self.obvious_zones = obvious_zones

    def in_strike_zone(self, x_coord: float, y_coord: float) -> bool:
        """Checks if (x_coord, y_coord) are in a strike zone

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        bool
            true if (x_coord, y_coord) are in a strike zone, false otherwise
        """
        zone_name = self.return_zone(x_coord, y_coord)
        for zone in self.strike_zones:
            if zone_name == zone.name:
                return True
        return False

    def in_ball_zone(self, x_coord: float, y_coord: float) -> bool:
        """Checks if (x_coord, y_coord) are in a non obvious ball zone

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        bool
            true if (x_coord, y_coord) are in a non obvious ball zone, false otherwise
        """
        zone_name = self.return_zone(x_coord, y_coord)
        for zone in self.ball_zones:
            if zone_name == zone.name:
                return True
        return False

    def in_obvious_zone(self, x_coord: float, y_coord: float) -> bool:
        """Checks if (x_coord, y_coord) are in an obvious ball zone

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        bool
            true if (x_coord, y_coord) are in a obvious ball zone, false otherwise
        """
        zone_name = self.return_zone(x_coord, y_coord)
        if zone_name[-1] == "b":
            return True
        return False

    def return_zone(self, x_coord: float, y_coord: float) -> str:
        """Finds the name of the Zone that contains (x_coord, y_coord)

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        str
            name of the Zone that contains (x_coord, y_coord)
        """
        for zone in self.strike_zones:
            if zone.in_zone(x_coord, y_coord):
                return zone.name

        for zone in self.ball_zones:
            if zone.in_zone(x_coord, y_coord):
                return zone.name

        return self.obvious_zones.return_zone(x_coord, y_coord)

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return (
            f"Zones({repr(self.strike_zones)}, {repr(self.ball_zones)},"
            f"{repr(self.obvious_zones)})"
        )

    def __str__(self):
        """Prints list of ball zones (name, coords, width, height) in the object"""
        return f"Ball Zone: {self.ball_zones}"
