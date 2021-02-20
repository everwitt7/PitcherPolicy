"""State Module"""
from pitch_zone_enums import Outcomes


class State:
    """State is the parent class of all state distributions

    Attributes
    ----------
    outcomes : Outcomes
        all the possible outcomes for a state (e.g. foul, out, hit, strike, ball)

    Methods
    -------
    get_successors():
        returns all possible successor states based on all possible outcomes
    """

    def __init__(self, outcomes: Outcomes) -> None:
        """Instatiates State object"""
        self.outcomes = outcomes

    def get_successors(self) -> dict:
        """Returns a dictionary of key, outcome and value, resulting state

        Returns
        -------
        dict
            a dict of outcome and resulting state dict[outcome] = State
        """

    def get_state(self, balls: int, strikes: int) -> str:
        """Returns the name of the state as a string

        Returns
        -------
        str
            name of the state
        """


class Count(State):
    """Class used to represent CountState

    Attributes
    ----------
    ball_count : int
        number of balls in the count
    strike_count : int
        number of strikes in the count

    Methods
    -------
    get_successors()
        returns all possible successor states given outcomes
    """

    def __init__(self, outcomes: Outcomes, num_balls: int, num_strikes: int) -> None:
        """Instantiates CountState object

        Parameters
        ----------
        ball_count : int
            number of balls in the count in range (0,3)
        strike_count : int
            number of strikes in the count in range (0,2)
        """
        super().__init__(outcomes)
        self.num_balls = num_balls
        self.num_strikes = num_strikes

    def get_successors(self) -> dict:
        """Returns a dictionary of possible successor states over outcomes (excluding out)

        Returns
        -------
        dict
            a dict of outcome and resulting state dict[outcome] = str(Count)
        """
        successors = {}
        # count is full 3-2, ball -> hit, strike -> out
        if self.num_balls == 3 and self.num_strikes == 2:
            successors[self.outcomes.FOUL.value] = self.get_state(
                self.num_balls, self.num_strikes)
            successors[self.outcomes.HIT.value] = self.outcomes.HIT.value
            successors[self.outcomes.BALL.value] = self.outcomes.HIT.value

        # count is x-2, strike -> out
        elif self.num_balls != 3 and self.num_strikes == 2:
            successors[self.outcomes.FOUL.value] = self.get_state(
                self.num_balls, self.num_strikes)
            successors[self.outcomes.HIT.value] = self.outcomes.HIT.value
            successors[self.outcomes.BALL.value] = self.get_state(
                self.num_balls+1, self.num_strikes)

        # count is 3-x, ball -> hit
        elif self.num_balls == 3 and self.num_strikes != 2:
            successors[self.outcomes.FOUL.value] = self.get_state(
                self.num_balls, self.num_strikes+1)
            successors[self.outcomes.HIT.value] = self.outcomes.HIT.value
            successors[self.outcomes.STRIKE.value] = self.get_state(
                self.num_balls, self.num_strikes+1)
            successors[self.outcomes.BALL.value] = self.outcomes.HIT.value

        else:
            successors[self.outcomes.FOUL.value] = self.get_state(
                self.num_balls, self.num_strikes+1)
            successors[self.outcomes.HIT.value] = self.outcomes.HIT.value
            successors[self.outcomes.STRIKE.value] = self.get_state(
                self.num_balls, self.num_strikes+1)
            successors[self.outcomes.BALL.value] = self.get_state(
                self.num_balls+1, self.num_strikes)

        return successors

    def get_state(self, balls: int, strikes: int) -> str:
        """Returns the name of the state as a string

        Returns
        -------
        str
            name of the state
        """
        return str(balls) + str(strikes)

    def __repr__(self):
        """Displays the inputs used to instantiate the object"""
        return (
            f"Count({self.outcomes}, {self.num_balls}, {self.num_strikes})"
        )

    def __str__(self):
        """Prints information about the object"""
        return (
            f"outcomes: {self.outcomes},\
            num_balls: {self.num_balls},\
            num_strikes: {self.num_strikes}"
        )
