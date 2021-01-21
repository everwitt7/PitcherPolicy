"""Zones Module"""
from typing import List

import matplotlib.pyplot as plt

from obvious_zones import ObviousZones
from zone import Zone


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
    display_zones()
        plots a visual of our zones
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

    def display_zones(self):
        """Displays an image and name for each Zone in the Zones object"""
        _, axis = plt.subplots(figsize=(8, 10))
        plt.title("Zones from Umpire Perspective")

        # plotting rectangles for strike zones
        for zone in self.strike_zones:
            rect = plt.Rectangle(zone.coords,
                                 width=zone.width,
                                 height=zone.height,
                                 facecolor="#85DEF8",
                                 edgecolor="black",
                                 zorder=2)
            axis.add_patch(rect)
            plt.text(zone.coords[0] + zone.width/2.5,
                     zone.coords[1] + zone.height/2,
                     zone.name)

        # plotting rectangles for ball zones
        for zone in self.ball_zones:
            rect = plt.Rectangle(zone.coords,
                                 width=zone.width,
                                 height=zone.height,
                                 facecolor="#FCF387",
                                 edgecolor="black",
                                 zorder=2)
            axis.add_patch(rect)
            # plotting text for each zone
            # TODO: replace strings with enumerations
            if zone.name == "10a" or zone.name == "15a":
                plt.text(zone.coords[0] + zone.width/2.2,
                         zone.coords[1] + zone.height/2,
                         zone.name)
            else:
                plt.text(zone.coords[0] + zone.width/4,
                         zone.coords[1] + zone.height/2.2,
                         zone.name)

        # plotting rectangles for obvious zones
        for zone_name, zone_data in self.obvious_zones.get_obvious_zones_diagram_data().items():
            rect = plt.Rectangle(zone_data["coords"],
                                 width=zone_data["width"],
                                 height=zone_data["height"],
                                 facecolor="#CD654E",
                                 edgecolor="black",
                                 zorder=1)
            axis.add_patch(rect)
            # plotting text for each zone
            if zone_name == "9b" or zone_name == "10b" or zone_name == "11b":
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.2,
                         zone_data["coords"][1] + zone_data["height"]/1.5,
                         zone_name)
            elif zone_name == "12b" or zone_name == "13b":
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.4,
                         zone_data["coords"][1] + zone_data["height"]/2,
                         zone_name)
            else:
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.2,
                         zone_data["coords"][1] + zone_data["height"]/4,
                         zone_name)

            # plotting home plate pentagon
            y_loc = 2 * self.obvious_zones.bot_y
            y_offset_bot = 1
            y_offset_mid = y_offset_bot - 0.2
            y_offset_top = y_offset_bot - 0.3
            pentagon_x = [self.obvious_zones.left_x, self.obvious_zones.left_x,
                          0, self.obvious_zones.right_x, self.obvious_zones.right_x]
            pentagon_x.append(pentagon_x[0])
            pentagon_y = [y_loc-y_offset_bot, y_loc-y_offset_mid,
                          y_loc-y_offset_top, y_loc-y_offset_mid, y_loc-y_offset_bot]
            pentagon_y.append(pentagon_y[0])
            plt.plot(pentagon_x, pentagon_y)

            # plotting line values in feet of strike zone coordinate cutoffs
            plt.text(self.obvious_zones.left_x - .2,
                     self.obvious_zones.top_y*2 + .1,
                     str(self.obvious_zones.left_x) + " ft")

            plt.text(self.obvious_zones.right_x - .2,
                     self.obvious_zones.top_y*2 + .1,
                     str(self.obvious_zones.right_x) + " ft")

            plt.text(self.obvious_zones.right_x*2 + .1,
                     self.obvious_zones.top_y - .05,
                     str(self.obvious_zones.top_y) + " ft")

            plt.text(self.obvious_zones.right_x*2 + .1,
                     self.obvious_zones.bot_y - .05,
                     str(self.obvious_zones.bot_y) + " ft")

        # TODO: we want to print the pitch type when displaying the zone -> move this to Pitch
        plt.axis("scaled")
        plt.axis("off")
        plt.show()

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return (
            f"Zones({repr(self.strike_zones)}, {repr(self.ball_zones)},"
            f"{repr(self.obvious_zones)})"
        )

    def __str__(self):
        """Prints list of ball zones (name, coords, width, height) in the object"""
        return f"Ball Zone: {self.ball_zones}"
