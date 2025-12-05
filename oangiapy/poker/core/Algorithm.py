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

    def get_card_class(self):
        return self._CardClass

    def get_hand_class(self):
        return self._HandClass

    def get_hands_class(self):
        return self._HandsClass

    def fast_scan(self):
        return (False, None)
