"""State Module"""



class State:
    """State is the parent class of all state distributions

    Methods
    -------
    get_successors(pticher_action, batter_action): 
        returns all possible successor states given optional pitcher and batter actions
    """

    def __init__(self) -> None:
        """Instatiates State object"""

    def get_successors(self, pitcher_action=None,batter_action=None) -> list:
        """Returns a list of possible next states
        
        Parameters
        ----------
        pitcher_action : string (optional)
            pitcher's action
        batter_action : string (optional)
            batter's action (swing, take)

        Returns
        -------
        [State,...]
            list of possible next states
        """
        



class CountState(State):
    """Class used to represent CountState

    Attributes
    ----------
    ball_count : int
        number of balls in the count
    strike_count : int
        number of strikes in the count
  

    Methods
    -------
    get_successors(pticher_action, batter_action)
        returns all possible successor states given optional pitcher and batter actions
    """

    def __init__(self, ball_count:int, strike_count:int):
        """Instantiates CountState object

        Parameters
        ----------
        ball_count : int
            number of balls in the count in range (0,3)
        strike_count : int
            number of strikes in the count in range (0,2)
        """

        if 0<=ball_count<=3 and 0<=strike_count<=2: 
            self.ball_count= ball_count
            self.strike_count= strike_count

        else:
            raise "Invalid ball or strike count"

    def get_successors(self, pitcher_action=None,batter_action=None):
        """Returns a list of possible successor CountStates

        Parameters
        ----------
        pitcher_action : string
            action of the pitcher in the at bat
        batter_action : string
            action of the batter in the at bat

        Returns
        -------
        [CountState,...]
            a list of possible successor CountStates
        """
        
        if pitcher_action == None and batter_action == None:
            """If no actions are specified, return all possible successor states"""
            possible_successors=[]
            if self.ball_count<=2:
                possible_successors.append(CountState(self.ball_count+1,self.strike_count))
            if self.strike_count<=1:
                possible_successors.append(CountState(self.ball_count,self.strike_count+1))
            if self.strike_count==2:
                """Foul ball"""
                possible_successors.append(CountState(self.ball_count,self.strike_count))
            return possible_successors
        elif pitcher_action != None and batter_action != None:
            """If actions are specified, return all possible successor states given actions"""
            possible_successors=[]
            if self.ball_count<=2:
                possible_successors.append(CountState(self.ball_count+1,self.strike_count))
            if self.strike_count<=1:
                possible_successors.append(CountState(self.ball_count,self.strike_count+1))
            if self.strike_count==2:
                """Foul ball"""
                possible_successors.append(CountState(self.ball_count,self.strike_count))
            return possible_successors
            
        else:
            raise "Specify either both pitcher_action and batter_action or neither"
    

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return (
            f"CountState({self.ball_count}, {self.strike_count})"
        )

    def __str__(self):
        """Prints information about the object"""
        return (
            f"ball_count: {self.ball_count}, strike_count: {self.strike_count},"
        )
    def __eq__(self, other):
        """Returns True if __repr__() of two objects are equal"""
        return repr(other) == repr(self)