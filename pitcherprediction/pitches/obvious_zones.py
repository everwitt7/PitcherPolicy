"""ObviousZones Module"""
from pitch_zone_enums import ObviousZoneNames


class ObviousZones:
    """Class used to represent ObviousZones

    Attributes
    ----------
    left_x : str
        the left most point of the strike zone (measured in feet)
    right_x: (float, float)
        the right most point of the strike zone (measured in feet)
    top_y: float
        the top most point of the strike zone (measured in feet)
    bot_y: float
        the bottom most point of the strike zone (measured in feet)

    Methods
    -------
    is_obvious(x_coord, y_coord)
        returns true if (x_coord, y_coord) are outside left_x, right_x, top_y, and bot_y
    return_zone(x_coord, y_coord)
        returns the -1 if (x_coord, y_coord) in strike zone, otherwise returns the obvious zone name
    get_obv_zones_data()
        returns a dict of obvious zone data needed to plot a Zones visualization
    """

    def __init__(self, x_width: float, y_width: float) -> None:
        """Instantiates ObviousZones object

        Parameters
        ----------
        x_width : float
            half the width of the strike zone
        y_width: float
            half the height of the strike zone
        """
        self.left_x = -abs(x_width)
        self.right_x = abs(x_width)
        self.top_y = abs(y_width)
        self.bot_y = -abs(y_width)

    def is_obvious(self, x_coord: float, y_coord: float) -> bool:
        """Checks if (x_coord, y_coord) are in an obvious zone

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        bool
            true if (x_coord, y_coord) are in ObviousZones, false otherwise
        """
        if self.left_x < x_coord < self.right_x and self.bot_y < y_coord < self.top_y:
            return False
        return True

    def return_zone(self, x_coord: float, y_coord: float) -> str:
        """Returns either an obvious zone or -1

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        str
            the name of the obvious zone or -1
        """
        if x_coord < self.left_x and y_coord > self.top_y:
            return ObviousZoneNames.NINE.value
        if self.left_x < x_coord < self.right_x and y_coord > self.top_y:
            return ObviousZoneNames.TEN.value
        if x_coord > self.right_x and y_coord > self.top_y:
            return ObviousZoneNames.ELEVEN.value

        if x_coord < self.left_x and self.bot_y < y_coord < self.top_y:
            return ObviousZoneNames.TWELVE.value
        if x_coord > self.right_x and self.bot_y < y_coord < self.top_y:
            return ObviousZoneNames.THIRTEEN.value

        if x_coord < self.left_x and y_coord < self.bot_y:
            return ObviousZoneNames.FOURTEEN.value
        if self.left_x < x_coord < self.right_x and y_coord < self.bot_y:
            return ObviousZoneNames.FIFTEEN.value
        if x_coord > self.right_x and y_coord < self.bot_y:
            return ObviousZoneNames.SIXTEEN.value

        return ObviousZoneNames.ERROR.value

    def get_obv_zones_data(self) -> dict:
        """Returns the information that defines obvious zones

        Returns
        -------
        dict
            coords, width, and height values for each obvious zones
        """
        return {
            "9b": {"coords": (self.left_x-self.right_x, self.top_y),
                   "width": self.right_x,
                   "height": self.top_y},
            "10b": {"coords": (self.left_x, self.top_y),
                    "width": self.right_x-self.left_x,
                    "height": self.top_y},
            "11b": {"coords": (self.right_x, self.top_y),
                    "width": self.right_x,
                    "height": self.top_y},
            "12b": {"coords": (self.left_x-self.right_x, self.bot_y),
                    "width": self.right_x,
                    "height": self.top_y-self.bot_y},
            "13b": {"coords": (self.right_x, self.bot_y),
                    "width": self.right_x,
                    "height": self.top_y-self.bot_y},
            "14b": {"coords": (self.left_x-self.right_x, self.bot_y-self.top_y),
                    "width": self.right_x,
                    "height": self.top_y},
            "15b": {"coords": (self.left_x, self.bot_y-self.top_y),
                    "width": self.right_x-self.left_x,
                    "height": self.top_y},
            "16b": {"coords": (self.right_x, self.bot_y-self.top_y),
                    "width": self.right_x,
                    "height": self.top_y}
        }

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"ObviousZones({self.left_x}, {self.right_x}, {self.top_y}, {self.bot_y})"

    def __str__(self):
        """Prints information about the object"""
        return (
            f"Cutoff Coordinates= > left_x: {self.left_x}, right_x: {self.right_x}"
            f"top_y: {self.top_y}, bot_y: {self.bot_y}"
        )
