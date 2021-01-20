"""Zone Module"""


class Zone:
    """Class used to represent a Zone

    Attributes
    ----------
    name : str
        the name of the zone (eg 8a)
    coords: (float, float)
        tuple of floats for the bottom left coords of the zone (x,y coords measured in feet)
    width: float
        the width of the zone (measured in feet)
    height: float
        the height of the zone (measured in feet)

    Methods
    -------
    get_center(x_coord, y_coord)
        returns an (x,y) tuple of the center of the Zone
    in_zone()
        returns true if (x_coord, y_coord) are in the Zone
    """

    def __init__(self, name: str, coords: (float, float), width: float, height: float) -> None:
        """Instantiates Zone object

        Parameters
        ----------
        name : str
            the name of the zone
        coords: (float, float)
            the bottom left coords of the zone
        width: float
            the width of the zone
        height: float
            the height of the zone
        """
        self.name = name
        self.coords = coords
        self.width = width
        self.height = height

    def get_center(self) -> (float, float):
        """Returns the center of the Zone

        Returns
        -------
        (float, float)
            a coordinate tuple of the center of the zone
        """
        return (self.coords[0] + self.width/2, self.coords[1] + self.height/2)

    def in_zone(self, x_coord: float, y_coord: float) -> bool:
        """Checks if (x_coord, y_coord) are in the Zone

        Parameters
        ----------
        x_coord : float
            x coordinate
        y_coord: float
            y coordinate

        Returns
        -------
        bool
            true if (x_coord, y_coord) are in the Zone, false otherwise
        """
        in_x = self.coords[0] <= x_coord <= self.coords[0] + self.width
        in_y = self.coords[1] <= y_coord <= self.coords[1] + self.height
        return in_x and in_y

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return f"Zone({self.name}, {self.coords}, {self.width}, {self.height})"

    def __str__(self):
        """Prints information about the object"""
        return (
            f"Name: {self.name}, Coords: {self.coords},"
            f"Width: {self.width}, Height: {self.height}"
        )
