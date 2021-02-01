"""State Interface/Metaclass Module"""



class State:
    """
    Class used to represent State interface for CountState

    Methods
    __________

    get_successors(pticher_action, batter_action): 
        returns all possible successor states given optional pitcher and batter actions


    """

    def __init__(self) -> None:
        """Instatiates State class"""

    def get_successors(self, pitcher_action=None,batter_action=None):
        """Returns a list of possible next states"""
        



class CountState(State):
    """

   Methods
    __________

    get_successors(pticher_action, batter_action): 
        returns all possible successor states given optional pitcher and batter actions


    Member variables
    __________

    ball_count: int
        number of balls in the count
    strike_count: int
        number of strikes in the count
    
    """

    def __init__(self, ball_count:int, strike_count:int):
        if ball_count<0 or ball_count>=4 or strike_count<0 or strike_count>=3:
            raise "Invalid ball or strike count"
        else:
            self.ball_count= ball_count
            self.strike_count= strike_count


    def get_successors(self, pitcher_action=None,batter_action=None):
        #TODO
        #Include Out/Base? Is that out of scope of CountState/ will these be different classes of the State metaclass
        if pitcher_action == None and batter_action == None:
            """if no actions are specified, return all possible successor states"""
            possible_successors=[]
            if self.ball_count<=2:
                possible_successors.append(CountState(self.ball_count+1,self.strike_count))
            if self.strike_count<=1:
                possible_successors.append(CountState(self.ball_count,self.strike_count+1))
            if self.strike_count==2:
                #Remove?
                """Foul ball"""
                possible_successors.append(CountState(self.ball_count,self.strike_count))
            return possible_successors
        elif pitcher_action != None and batter_action !=None:
            """if actions are specified, return all possible successor states given actions"""
            #TODO
            #Unsure of what form pitcher_action and batter_action takes on and how this narrows possible CountStates
            return None
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
