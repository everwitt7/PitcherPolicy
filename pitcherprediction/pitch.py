"""Pitch Module"""

import numpy as np
import matplotlib.pyplot as plt

from error_dist import ErrorDistribution
from pitch_zone_enums import ObviousZoneNames
from zones import Zones


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

    Methods
    -------
    display_zones()
        plots a visual of our zones
    run_error_simuation(trials)
        generates an accuracy matrix
    """

    def __init__(self, name: str, zones: Zones, error_dist: ErrorDistribution) -> None:
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

    def run_error_simuation(self, trials: int = 1000, seed: int = 0) -> dict:
        """Runs a simulation to create an accuracy matrix based on zones and error dist

        Parameters
        ----------
        trials : int
            the number of times we run the simulation for each zone

        Returns
        -------
        dict
            a dict[int][act] that has % of time the pitch ended in a zone
        """
        # setting seed for reproducibility
        np.random.seed(0)

        acc_matrix = {}
        for zone in self.zones.strike_zones + self.zones.ball_zones:
            acc_matrix[zone.name] = {}
            x_intended, y_intended = zone.get_center()

            for _ in range(trials):
                x_actual, y_actual = self.error_dist.gen_actual_loc(
                    x_intended, y_intended)
                loc = self.zones.return_zone(x_actual, y_actual)

                if loc not in acc_matrix[zone.name].keys():
                    acc_matrix[zone.name][loc] = 0
                acc_matrix[zone.name][loc] += 1
            acc_matrix[zone.name] = {k: v / trials for k,
                                     v in acc_matrix[zone.name].items()}
        return acc_matrix

    def display_zones(self) -> None:
        """Displays an image and name for each Zone in the Zones object"""
        _, axis = plt.subplots(figsize=(8, 10))
        plt.title(f"{self.name} Zones from Umpire Perspective")

        # plotting rectangles for strike zones
        for zone in self.zones.strike_zones:
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
        for zone in self.zones.ball_zones:
            rect = plt.Rectangle(zone.coords,
                                 width=zone.width,
                                 height=zone.height,
                                 facecolor="#FCF387",
                                 edgecolor="black",
                                 zorder=2)
            axis.add_patch(rect)
            # plotting text for each zone
            if zone.name == "10a" or zone.name == "15a":
                plt.text(zone.coords[0] + zone.width/2.2,
                         zone.coords[1] + zone.height/2,
                         zone.name)
            else:
                plt.text(zone.coords[0] + zone.width/4,
                         zone.coords[1] + zone.height/2.2,
                         zone.name)

        # plotting rectangles for obvious zones
        for zone_name, zone_data in self.zones.obvious_zones.get_obv_zones_data().items():
            rect = plt.Rectangle(zone_data["coords"],
                                 width=zone_data["width"],
                                 height=zone_data["height"],
                                 facecolor="#CD654E",
                                 edgecolor="black",
                                 zorder=1)
            axis.add_patch(rect)
            # plotting text for each zone
            if (zone_name == ObviousZoneNames.NINE.value or
                zone_name == ObviousZoneNames.TEN.value or
                    zone_name == ObviousZoneNames.ELEVEN.value):
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.2,
                         zone_data["coords"][1] + zone_data["height"]/1.5,
                         zone_name)
            elif (zone_name == ObviousZoneNames.TWELVE.value or
                  zone_name == ObviousZoneNames.THIRTEEN.value):
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.4,
                         zone_data["coords"][1] + zone_data["height"]/2,
                         zone_name)
            else:
                plt.text(zone_data["coords"][0] + zone_data["width"]/2.2,
                         zone_data["coords"][1] + zone_data["height"]/4,
                         zone_name)

            # plotting home plate pentagon
            y_loc = 2 * self.zones.obvious_zones.bot_y
            y_offset_bot = 1
            y_offset_mid = y_offset_bot - 0.2
            y_offset_top = y_offset_bot - 0.3
            pentagon_x = [self.zones.obvious_zones.left_x, self.zones.obvious_zones.left_x,
                          0, self.zones.obvious_zones.right_x, self.zones.obvious_zones.right_x]
            pentagon_x.append(pentagon_x[0])
            pentagon_y = [y_loc-y_offset_bot, y_loc-y_offset_mid,
                          y_loc-y_offset_top, y_loc-y_offset_mid, y_loc-y_offset_bot]
            pentagon_y.append(pentagon_y[0])
            plt.plot(pentagon_x, pentagon_y)

            # plotting line values in feet of strike zone coordinate cutoffs
            plt.text(self.zones.obvious_zones.left_x - .2,
                     self.zones.obvious_zones.top_y*2 + .1,
                     str(self.zones.obvious_zones.left_x) + " ft")

            plt.text(self.zones.obvious_zones.right_x - .2,
                     self.zones.obvious_zones.top_y*2 + .1,
                     str(self.zones.obvious_zones.right_x) + " ft")

            plt.text(self.zones.obvious_zones.right_x*2 + .1,
                     self.zones.obvious_zones.top_y - .05,
                     str(self.zones.obvious_zones.top_y) + " ft")

            plt.text(self.zones.obvious_zones.right_x*2 + .1,
                     self.zones.obvious_zones.bot_y - .05,
                     str(self.zones.obvious_zones.bot_y) + " ft")

        plt.axis("scaled")
        plt.axis("off")
        plt.show()

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"Pitch({repr(self.name)}, {repr(self.zones)}, {repr(self.error_dist)})"

    def __str__(self):
        """Prints pitch name, error dist, and ball zones"""
        return f"Pitch: {self.name}, Error Dist: {self.error_dist}, {self.zones}"
