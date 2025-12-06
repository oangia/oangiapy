from oangiapy.poker.core import Card as BaseCard
from oangiapy.poker.core import Hand as BaseHand
from oangiapy.poker.core import Hands as BaseHands
from oangiapy.poker.detector import HandTypeDetector, HandPointCalculator, HandsPointCalculator

class Card(BaseCard):
    def __init__(self, name):
        super().__init__(name)
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point

class Hand(BaseHand):
    def __init__(self, cards):
        super().__init__(cards);
        self._typeDetector = HandTypeDetector(self)
        self._pointCalculator = HandPointCalculator(self)
        
    def get_type(self):
        return self._typeDetector.get_type()

    def get_point(self):
        return self._pointCalculator.get_point()
            
class Hands(BaseHands):
    def __init__(self, back, middle, front):
        super().__init__(back, middle, front)
        self._pointCalculator = HandsPointCalculator(self)
        
    def get_point(self):
        return self._pointCalculator.get_point()
            
          
