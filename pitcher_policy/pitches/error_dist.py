"""ErrorDistribution Module"""
import numpy as np


class ErrorDistribution:
    """ErrorDistribution is the parent class of all error distribution implementations

    Methods
    -------
    gen_actual_loc(x_intended, y_intended)
        returns the actual coordinates
    """

    def __init__(self) -> None:
        """Instantiates ErrorDistribution object"""

    def gen_actual_loc(self, x_intended: float, y_intended: float) -> (float, float):
        """Applies error to intended location and returns actual location

        Parameters
        ----------
        intended_location : (float, float)
            coordinates of the intended location

        Returns
        -------
        (float, float)
            the actual location
        """


class NormalErrorDistribution(ErrorDistribution):
    """Class used to represent NormalErrorDistribution

    Attributes
    ----------
    sigma_x : float
        the standard deviation along the x axis (in feet)
    sigma_y: float
        the standard deviation along the y axis (in feet)
    mu_x: float
        the center of the x axis (should be zero)
    mu_y: float
        the center of the y axis (should be zero)

    Methods
    -------
    gen_actual_loc(x_intended, y_intended)
        returns the actual coordinates
    """

    def __init__(self, sigma_x: float, sigma_y: float,
                 mu_x: float = None, mu_y: float = None) -> None:
        """Instantiates NormalErrorDistribution object

        Parameters
        ----------
        sigma_x : float
            the standard deviation along the x axis (in feet)
        sigma_y: float
            the standard deviation along the y axis (in feet)
        mu_x: float
            the center of the x axis (should be zero)
        mu_y: float
            the center of the y axis (should be zero)
        """
        super().__init__()
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        if mu_x is None:
            self.mu_x = 0
        else:
            self.mu_x = mu_x
        if mu_y is None:
            self.mu_y = 0
        else:
            self.mu_y = mu_y

    def gen_actual_loc(self, x_intended: float, y_intended: float) -> (float, float):
        """Returns coords of actual location based on error dist and intended location

        Parameters
        ----------
        x_intended : float
            x coordinate
        y_intended: float
            y coordinate

        Returns
        -------
        (float, float)
            returns the actual coordinates, (x_actual, y_actual)
        """
        x_actual = x_intended + np.random.normal(self.mu_x, self.sigma_x, 1)
        y_actual = y_intended + np.random.normal(self.mu_y, self.sigma_y, 1)
        return (x_actual, y_actual)

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return (
            f"NormalErrorDistribution({self.sigma_x}, {self.sigma_y}, {self.mu_x}, {self.mu_y})"
        )

    def __str__(self):
        """Prints information about the object"""
        return (
            f"sigma_x: {self.sigma_x}, sigma_y: {self.sigma_y},"
            f"mu_x: {self.mu_x}, mu_y: {self.mu_y}"
        )
