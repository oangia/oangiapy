from oangiapy.poker.core import Card as BaseCard
from oangiapy.poker.core import HandDetector as BaseHandDetector
from oangiapy.poker.core import HandType, PokerAlgo, Player

class Card(BaseCard):
    def __init__(self, name):
        super().__init__(name)
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point

class HandDetector(BaseHandDetector):
    def __init__(self, cards):
        self.cards = cards

        self.zitch_point = sum(card.get_rank_point() for card in self.cards)
        self.suit_str = ''.join(card.get_suit() for card in self.cards)
        if self._hasDup():
            detect = self._detectPair()
        else:
            detect = self._detectZitch()

        self._type, self._point = detect
        
    def get_type(self):
        return self._type

    def get_point(self):
        return self._point

    def _hasDup(self):
        return any(self.cards[i].get_rank() == self.cards[i+1].get_rank() for i in range(len(self.cards) - 1))

    def _detectZitch(self):
        self.straight = self.zitch_point in [
            4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936
        ]
        self.flush = self.suit_str in ['sssss', 'ccccc', 'ddddd', 'hhhhh']

        if self.straight and self.flush:
            return (HandType.STRAIGHTFLUSH, self.zitch_point)
        if self.straight:
            return (HandType.STRAIGHT, self.zitch_point)
        if self.flush:
            return (HandType.FLUSH, self.zitch_point)

        return (HandType.ZITCH, self.zitch_point)

    def _detectPair(self):
        ranks = [card.get_rank() for card in self.cards]
        freqs = {}
        for r in ranks:
            freqs[r] = freqs.get(r, 0) + 1

        counts = sorted(freqs.values(), reverse=True)

        if counts[0] == 4:
            return (HandType.FOURKIND, self.cards[2].get_rank_value())

        if counts[0] == 3 and counts[1] == 2:
            return (HandType.FULLHOUSE, self.cards[2].get_rank_value())

        if counts[0] == 3:
            return (HandType.THREEKIND, self.cards[2].get_rank_value())

        if counts[0] == 2 and counts[1] == 2:
            point = self.cards[1].get_rank_point() + self.cards[3].get_rank_point()
            zitch = sum(
                c.get_rank_value() if c.get_rank() not in (self.cards[1].get_rank(), self.cards[3].get_rank())
                else 0
                for c in self.cards
            )
            return (HandType.TWOPAIR, point + zitch / 7937)

        if counts[0] == 2:
            for i in range(4):
                if self.cards[i].get_rank() == self.cards[i+1].get_rank():
                    point = self.cards[i].get_rank_value()
                    zitch = self.zitch_point - self.cards[i].get_rank_point() * 2
                    break
            return (HandType.ONEPAIR, point + zitch / 7937)
          
