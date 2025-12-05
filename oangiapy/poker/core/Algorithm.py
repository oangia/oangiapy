from itertools import combinations
from oangiapy.poker.core.Card import Card
from oangiapy.poker.core.Hand import Hand
from oangiapy.poker.core.Hands import Hands

class Algorithm:
    def __init__(self, cards):
        self._CardClass = Card
        self._HandClass = Hand
        self._HandsClass = Hands
        self._cards = [self.get_card_class()(x) for x in cards.split(",")]
        self._cards.sort(key=lambda c: (c.get_rank(), c.get_suit()))

    def split_5_5_3_index(self):
        index = range(13)
        res = []
        for back in combinations(index, 5):
            remain1 = [c for c in index if c not in back]
            for middle in combinations(remain1, 5):
                remain2 = [c for c in remain1 if c not in middle]
                for front in combinations(remain2, 3):
                    res.append((
                        back, 
                        middle, 
                        front
                    ))
        return res
        
    def get_card_class(self):
        return self._CardClass

    def get_hand_class(self):
        return self._HandClass

    def get_hands_class(self):
        return self._HandsClass

    def fast_scan(self):
        return (False, None)
