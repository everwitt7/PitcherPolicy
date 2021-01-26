"""Swing Data Module"""


class SwingData:
    """Class used to represent SwingData

    Attributes
    ----------
    swingData : dict 
        the empirical data for when batters swing 

    Methods
    -------
    getHitProportion(pitcherAction)
        gets the proporiton of hits for a given pitch and actual location 
    getOutProportion(pitcherAction)
        gets the proporiton of outs for a given pitch and actual location
    getStrikeProportion(pitcherAction)
        gets the proporiton of strikes for a given pitch and actual location
    getFoulProportion(pitcherAction)
        gets the proporiton of fouls for a given pitch and actual location
    """

    def __init__(self, url: str) -> None:
        """Instantiates SwingData object

        Parameters
        ----------
        url : str
            url to github
        """
        #TODO 