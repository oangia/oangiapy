class HandDetector:
    def __init__(self, hand):
        self._hand = hand
        self._type = Hand.ZITCH
        self._point = 0

        self._zitch_point = sum(card.get_rank_point() for card in hand.get_cards())
        self.suit_str = ''.join(card.get_suit() for card in hand.get_cards())
        if self._hasDup():
            self._type = self._detectPair()
        else:
            self._type = self._detectZitch()
        self._point = self.calc_point()
        
    def get_type(self):
        return self._type

    def get_point(self):
        return self._point

    def _hasDup(self):
        return any(self._hand.get_cards()[i].get_rank() == self._hand.get_cards()[i+1].get_rank() for i in range(len(self._hand.get_cards()) - 1))

    def _detectZitch(self):
        self.straight = self._zitch_point in [
            4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936
        ]
        self.flush = self.suit_str in ['sssss', 'ccccc', 'ddddd', 'hhhhh']

        if self.straight and self.flush:
            return Hand.STRAIGHTFLUSH
        if self.straight:
            return Hand.STRAIGHT
        if self.flush:
            return Hand.FLUSH
        return Hand.ZITCH

    def _detectPair(self):
        ranks = [card.get_rank() for card in self._hand.get_cards()]
        freqs = {}
        for r in ranks:
            freqs[r] = freqs.get(r, 0) + 1

        counts = sorted(freqs.values(), reverse=True)

        if counts[0] == 4:
            return Hand.FOURKIND
        if counts[0] == 3 and counts[1] == 2:
            return Hand.FULLHOUSE
        if counts[0] == 3:
            return Hand.THREEKIND
            
        if counts[0] == 2 and counts[1] == 2:
            return Hand.TWOPAIR
        if counts[0] == 2:
            return Hand.ONEPAIR

    def calc_point(self):
        match self._hand.get_type():
            case Hand.ZITCH | Hand.STRAIGHT | Hand.FLUSH | Hand.STRAIGHTFLUSH:
                return self._zitch_point * 100 / 7937
            case Hand.ONEPAIR:
                for i in range(4):
                    if self._hand.get_cards()[i].get_rank() == self._hand.get_cards()[i+1].get_rank():
                        zitch = self._zitch_point - self._hand.get_cards()[i].get_rank_point() * 2
                        return self._hand.get_cards()[i].get_rank_value()
            case Hand.TWOPAIR:
                zitch = sum(
                    c.get_rank_value() if c.get_rank() not in (self._hand.get_cards()[1].get_rank(), self._hand.get_cards()[3].get_rank())
                    else 0
                    for c in self._hand.get_cards()
                )
                _point = self._hand.get_cards()[1].get_rank_point() + self._hand.get_cards()[3].get_rank_point()
                return _point * 100 / 7937
            case Hand.THREEKIND | Hand.FULLHOUSE | Hand.FOURKIND:
                return self._hand.get_cards()[2].get_rank_value() * 100 / 13
