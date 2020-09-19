# import standard
from dataclasses import dataclass


@dataclass
class TripleBarrier:
    """
    Consist of four components:
    Upper: multiplier of price move field to set the profit booking level.
    Lower: multiplier of price move field to set the stop loss level.
        definition of upper and lower will be reversed fro short position.
    Vertical: # of bars to set the investment time stamp.
    Price move field: % return field based on which barrier will be calculated. Default wil be set to 1.
    if price move is none, barriers will be calculated based on entry point price.
    """
    upper: float = 0.0
    lower: float = 0.0
    vertical: int = 0
    price_move_field: str = None
