"""Swing Data Module"""
import json, os.path

class SwingData:
    """Class used to represent SwingData

    Attributes
    ----------
    swing_data : dict 
        the empirical data for when batters swing 

    Methods
    -------
    get_hit_proportion(pitcherAction)
        gets the proporiton of hits for a given pitch and actual location 
    get_out_proportion(pitcherAction)
        gets the proporiton of outs for a given pitch and actual location
    get_strike_proportion(pitcherAction)
        gets the proporiton of strikes for a given pitch and actual location
    get_foul_proportion(pitcherAction)
        gets the proporiton of fouls for a given pitch and actual location
    """

    def __init__(self, file_path: str) -> None:
        """Instantiates SwingData object

        Parameters
        ----------
        file_path : str
            relative path to file containing swing data
        """
        self.swing_data = {}
        path_prefix = os.path.abspath(os.path.dirname(__file__))
        full_path = path_prefix + "/" + file_path
        with open (full_path) as swing_data:
            self.swing_data = json.load(swing_data)

    def get_hit_proportion(self, pitch_type: str, actual_loc: str) -> float:
        """returns the proportion of hits for a given pitch and actual location

        Parameters
        ----------
        pitch_type : str
            the name of the pitch type
        actual_loc : str
            the name of the zone
        Returns
        -------
        float
            the proportion of hits for a given pitch type and actual location 
        """
        if self.swing_data[pitch_type]:
            if self.swing_data[pitch_type][actual_loc]:
                return self.swing_data[pitch_type][actual_loc][0]
            else: 
                #TODO: If a zone doesn't exist for a given pitch type it means that it never
                # ended up there right?  
                return 0
        else: 
            #TODO: Should I throw an error here or just return zero? (this is the case where 
            # there is no entry for the given pitch type) 
            return 0

    def get_out_proportion(self, pitch_type: str, actual_loc: str) -> float:
        """returns the proportion of outs for a given pitch and actual location

        Parameters
        ----------
        pitch_type : str
            the name of the pitch type
        actual_loc : str
            the name of the zone
        Returns
        -------
        float
            the proportion of outs for a given pitch type and actual location 
        """
        if self.swing_data[pitch_type]:
            if self.swing_data[pitch_type][actual_loc]:
                return self.swing_data[pitch_type][actual_loc][1]
            else: 
                #TODO: If a zone doesn't exist for a given pitch type it means that it never
                # ended up there right?  
                return 0
        else: 
            #TODO: Should I throw an error here or just return zero? (this is the case where 
            # there is no entry for the given pitch type) 
            return 0

    def get_strike_proportion(self, pitch_type: str, actual_loc: str) -> float:
        """returns the proportion of strikes for a given pitch and actual location

        Parameters
        ----------
        pitch_type : str
            the name of the pitch type
        actual_loc : str
            the name of the zone
        Returns
        -------
        float
            the proportion of strikes for a given pitch type and actual location 
        """
        if self.swing_data[pitch_type]:
            if self.swing_data[pitch_type][actual_loc]:
                return self.swing_data[pitch_type][actual_loc][2]
            else: 
                #TODO: If a zone doesn't exist for a given pitch type it means that it never
                # ended up there right?  
                return 0
        else: 
            #TODO: Should I throw an error here or just return zero? (this is the case where 
            # there is no entry for the given pitch type) 
            return 0

    def get_foul_proportion(self, pitch_type: str, actual_loc: str) -> float:
        """returns the proportion of fouls for a given pitch and actual location

        Parameters
        ----------
        pitch_type : str
            the name of the pitch type
        actual_loc : str
            the name of the zone
        Returns
        -------
        float
            the proportion of fouls for a given pitch type and actual location 
        """
        if self.swing_data[pitch_type]:
            if self.swing_data[pitch_type][actual_loc]:
                return self.swing_data[pitch_type][actual_loc][3]
            else: 
                #TODO: If a zone doesn't exist for a given pitch type it means that it never
                # ended up there right?  
                return 0
        else: 
            #TODO: Should I throw an error here or just return zero? (this is the case where 
            # there is no entry for the given pitch type) 
            return 0