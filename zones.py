"""this module has Zones class"""
import matplotlib.pyplot as plt
from zone import Zone
from obvious_zones import ObviousZones


class Zones:
    """Zones represents a list of Zone objects to which the pitcher may throw

    Attributes:
        strike_zones: a list of Zone objects that define the strike zones
        ball_zones: a list of Zone objects that define the ball zones
        obvious_zones: an object of ObviousZones that defines all obvious zones
    """

    def __init__(self, strike_zones, ball_zones, obvious_zones):
        """Inits Zones"""
        self._strike_zones = strike_zones
        self._ball_zones = ball_zones
        self._obvious_zones = obvious_zones

    def in_strike_zone(self, x, y):
        """Returns True if the (x,y) coordinates are in the strike zone"""
        zone_name = self.return_zone(x, y)
        for zone in self._strike_zones:
            if zone_name == zone._name:
                return True
        return False

    def in_ball_zone(self, x, y):
        """Returns True if the (x,y) coordinates are in a non obvious ball zone"""
        zone_name = self.return_zone(x, y)
        for zone in self._ball_zones:
            if zone_name == zone.name:
                return True
        return False

    def in_obvious_zone(self, x, y):
        """Returns True if the (x,y) coordinates are in an obvious ball zone"""
        zone_name = self.return_zone(x, y)
        if zone_name[-1] == "b":
            return True
        return False

    def return_zone(self, x, y):
        """Returns the name of Zone that contains the (x,y) coordinates"""
        for zone in self._strike_zones:
            if zone.in_zone(x, y):
                return zone._name

        for zone in self._ball_zones:
            if zone.in_zone(x, y):
                return zone._name

        return self._obvious_zones.return_zone(x, y)

    def display_zones(self):
        """Displays an image and name for each Zone in the Zones object"""
        fig, ax = plt.subplots(figsize=(8, 10))
        plt.title("Zones from Umpire Perspective")

        # plotting rectangles for strike zones
        for zone in self._strike_zones:
            rect = plt.Rectangle(zone._coords,
                                 width=zone._width,
                                 height=zone._height,
                                 facecolor="#85DEF8",
                                 edgecolor="black",
                                 zorder=2)
            ax.add_patch(rect)
            plt.text(zone._coords[0] + zone._width/2.5,
                     zone._coords[1] + zone._height/2,
                     zone._name)

        # plotting rectangles for ball zones
        for zone in self._ball_zones:
            rect = plt.Rectangle(zone._coords,
                                 width=zone._width,
                                 height=zone._height,
                                 facecolor="#FCF387",
                                 edgecolor="black",
                                 zorder=2)
            ax.add_patch(rect)
            # plotting text for each zone
            if zone._name == "10a" or zone._name == "15a":
                plt.text(zone._coords[0] + zone._width/2.2,
                         zone._coords[1] + zone._height/2,
                         zone._name)
            else:
                plt.text(zone._coords[0] + zone._width/4,
                         zone._coords[1] + zone._height/2.2,
                         zone._name)

        # plotting rectangles for obvious zones
        for zone_name, zone_data in self._obvious_zones.get_obvious_zones_diagram_data().items():
            rect = plt.Rectangle(zone_data["coords"],
                                 width=zone_data["width"],
                                 height=zone_data["height"],
                                 facecolor="#CD654E",
                                 edgecolor="black",
                                 zorder=1)
            ax.add_patch(rect)
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
            y_loc = 2 * self._obvious_zones._bot_y
            y_offset_bot = 1
            y_offset_mid = y_offset_bot - 0.2
            y_offset_top = y_offset_bot - 0.3
            pentagon_x = [self._obvious_zones._left_x, self._obvious_zones._left_x,
                          0, self._obvious_zones._right_x, self._obvious_zones._right_x]
            pentagon_x.append(pentagon_x[0])
            pentagon_y = [y_loc-y_offset_bot, y_loc-y_offset_mid,
                          y_loc-y_offset_top, y_loc-y_offset_mid, y_loc-y_offset_bot]
            pentagon_y.append(pentagon_y[0])
            plt.plot(pentagon_x, pentagon_y)

            # plotting line values in feet of strike zone coordinate cutoffs
            plt.text(self._obvious_zones._left_x - .2,
                     self._obvious_zones._top_y*2 + .1,
                     str(self._obvious_zones._left_x) + " ft")

            plt.text(self._obvious_zones._right_x - .2,
                     self._obvious_zones._top_y*2 + .1,
                     str(self._obvious_zones._right_x) + " ft")

            plt.text(self._obvious_zones._right_x*2 + .1,
                     self._obvious_zones._top_y - .05,
                     str(self._obvious_zones._top_y) + " ft")

            plt.text(self._obvious_zones._right_x*2 + .1,
                     self._obvious_zones._bot_y - .05,
                     str(self._obvious_zones._bot_y) + " ft")

        # we would actually want to print the pitch type when displaying the zone,
        plt.axis("scaled")
        plt.axis("off")
        plt.show()

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"Zones({repr(self._strike_zones)}, {repr(self._ball_zones)}, {repr(self._obvious_zones)})"

    def __str__(self):
        """Prints list of ball zones (name, coords, width, height) in the object"""
        return f"Ball Zone: {self._ball_zones}"
