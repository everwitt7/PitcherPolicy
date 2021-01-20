"""this module has ObviousZone class"""


class ObviousZones:
    """ObviousZones represents all zones that are obvious

    Attributes:
      _left_x: float representing the left most point of the strike zone (measured in feet)
      _left_x: float representing the right most point of the strike zone (measured in feet)
      _top_y: float representing the top most point of the strike zone (measured in feet)
      _bot_y: float representing the bot most point of the strike zone (measured in feet)
    """

    def __init__(self, x_width, y_width):
        """Inits ObviousZones"""
        self._left_x = -abs(x_width)
        self._right_x = abs(x_width)
        self._top_y = abs(y_width)
        self._bot_y = -abs(y_width)

    def is_obvious(self, x_coord, y_coord):
        """Returns True if (x,y) coords are outside of the strike zone"""
        if self._left_x < x_coord < self._right_x and self._bot_y < y_coord < self._top_y:
            return False
        return True

    def return_zone(self, x_coord, y_coord):
        """Returns the obvious zone that (x,y) is in, otherwise it returns an error, -1"""
        if x_coord < self._left_x and y_coord > self._top_y:
            return "9b"
        elif self._left_x < x_coord < self._right_x and y_coord > self._top_y:
            return "10b"
        elif x_coord > self._right_x and y_coord > self._top_y:
            return "11b"

        elif x_coord < self._left_x and self._bot_y < y_coord < self._top_y:
            return "12b"
        elif x_coord > self._right_x and self._bot_y < y_coord < self._top_y:
            return "13b"

        elif x_coord < self._left_x and y_coord < self._bot_y:
            return "14b"
        elif self._left_x < x_coord < self._right_x and y_coord < self._bot_y:
            return "15b"
        elif x_coord > self._right_x and y_coord < self._bot_y:
            return "16b"

        return "-1"  # raise valueError here?

    def get_obvious_zones_diagram_data(self):
        """Returns the information that defines obvious zones"""
        return {
            "9b": {"coords": (self._left_x-self._right_x, self._top_y),
                   "width": self._right_x,
                   "height": self._top_y},
            "10b": {"coords": (self._left_x, self._top_y),
                    "width": self._right_x-self._left_x,
                    "height": self._top_y},
            "11b": {"coords": (self._right_x, self._top_y),
                    "width": self._right_x,
                    "height": self._top_y},
            "12b": {"coords": (self._left_x-self._right_x, self._bot_y),
                    "width": self._right_x,
                    "height": self._top_y-self._bot_y},
            "13b": {"coords": (self._right_x, self._bot_y),
                    "width": self._right_x,
                    "height": self._top_y-self._bot_y},
            "14b": {"coords": (self._left_x-self._right_x, self._bot_y-self._top_y),
                    "width": self._right_x,
                    "height": self._top_y},
            "15b": {"coords": (self._left_x, self._bot_y-self._top_y),
                    "width": self._right_x-self._left_x,
                    "height": self._top_y},
            "16b": {"coords": (self._right_x, self._bot_y-self._top_y),
                    "width": self._right_x,
                    "height": self._top_y}
        }

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"ObviousZones({self._left_x}, {self._right_x}, {self._top_y}, {self._bot_y})"

    def __str__(self):
        """Prints information about the object"""
        return (
            f"Cutoff Coordinates= > left_x: {self._left_x}, right_x: {self._right_x}"
            f"top_y: {self._top_y}, bot_y: {self._bot_y}"
        )
