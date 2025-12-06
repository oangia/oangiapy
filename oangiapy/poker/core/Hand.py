class Hand:
    ZITCH = 0
    ONEPAIR = 1
    TWOPAIR = 2
    THREEKIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULLHOUSE = 6
    FOURKIND = 7
    STRAIGHTFLUSH = 8
    
    def __init__(self, cards):
        self._cards = cards
        self._typeDetector = HandTypeDetector(self)
        self._pointCalcilator = HandPointCalculator(self)

    def get_cards(self):
        return self._cards
        
    def get_type(self):
        return self._typeDetector.get_type()

    def get_point(self):
        return self._pointCalcilator.get_point()

    def check_dup(self, other):
        return any(c1.get_name() == c2.get_name() for c1 in self.get_cards() for c2 in other.get_cards())

    def compare(self, other, zitch=False):
        if self.get_type() < other.get_type():
            return -1
        if self.get_type() > other.get_type():
            return 1
        # same level → compare point
        if self.get_point() > other.get_point():
            return 1
        if self.get_point() < other.get_point():
            return -1
            
        return 0
        
    def __lt__(self, other):
        return self.compare(other) == -1

    def __gt__(self, other):
        return self.compare(other) == 1

    def __repr__(self):
        return ",".join(c.get_name() for c in self._cards) + " " + str(self.get_type()) + " " + str(self.get_point())    

class HandTypeDetector:
    def __init__(self, hand):
        self._type = Hand.ZITCH

        self.zitch_point = sum(card.get_rank_point() for card in hand.get_cards())
        self.suit_str = ''.join(card.get_suit() for card in hand.get_cards())
        if self._hasDup():
            self._type = self._detectPair()
        else:
            self._type = self._detectZitch()
        
    def get_type(self):
        return self._type

    def _hasDup(self):
        return any(hand.get_cards()[i].get_rank() == hand.get_cards()[i+1].get_rank() for i in range(len(hand.get_cards()) - 1))

    def _detectZitch(self):
        self.straight = self.zitch_point in [
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
        ranks = [card.get_rank() for card in hand.get_cards()]
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
            #return (HandType.TWOPAIR, point + zitch / 7937)
        if counts[0] == 2:
            return Hand.ONEPAIR
            #return (HandType.ONEPAIR, point + zitch / 7937)

class HandPointCalculator:
    def __init__(self, hand):
        self._point = 0
        self._zitch_point = sum(card.get_rank_point() for card in hand.get_cards())
        hand.get_cards()
        match hand.get_type():
            case Hand.ZITCH | Hand.STRAIGHT | Hand.FLUSH | Hand.STRAIGHTFLUSH:
                self._point = self._zitch_point * 100 / 7937
            case Hand.ONEPAIR:
                for i in range(4):
                    if hand.get_cards()[i].get_rank() == hand.get_cards()[i+1].get_rank():
                        self._point = hand.get_cards()[i].get_rank_value()
                        zitch = self.zitch_point - hand.get_cards()[i].get_rank_point() * 2
                        break
            case Hand.TWOPAIR:
                self._point = hand.get_cards()[1].get_rank_point() + hand.get_cards()[3].get_rank_point()
                self._point = self._point * 100 / 7937
                zitch = sum(
                    c.get_rank_value() if c.get_rank() not in (hand.get_cards()[1].get_rank(), hand.get_cards()[3].get_rank())
                    else 0
                    for c in hand.get_cards()
                )
            case Hand.THREEKIND | Hand.FULLHOUSE | Hand.FOURKIND:
                self._point = hand.get_cards()[2].get_rank_value() * 100 / 13

    def get_point(self):
        return self._point
            
