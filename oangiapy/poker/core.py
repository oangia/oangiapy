class Card:
    def __init__(self, name):
        self._name = name
        self._rank = int(name[:-1])
        self._suit = name[-1]
        # my take
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank(self):
        return self._rank

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point

    def get_suit(self):
        return self._suit

    def get_name(self):
        return self._name

    def __repr__(self):
        return self._name

class HandType:
    ZITCH = 1
    ONEPAIR = 2
    TWOPAIR = 3
    THREEKIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULLHOUSE = 7
    FOURKIND = 8
    STRAIGHTFLUSH = 9

class MyHandDetector:
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

class Hand:
    def __init__(self, cards):
        self._cards = cards
        self._detector = MyHandDetector(self._cards)
        self._type = self._detector.get_type()

    def get_type(self):
        return self._type

    def compare(self, other, zitch=False):
        if self.get_type() < other.get_type():
            return -1
        if self.get_type() > other.get_type():
            return 1

        # same level → compare point
        #if self.get_point() > other.get_point():
        #    return 1
        #if self.get_point() < other.get_point():
        #    return -1

        # same point → compare zitch point (optional)
        #if self.get_point() == other.get_point():
        #    return self.compare_zitch_point(other) if zitch else 0

    def compare_zitch_point(self, other):
        if self.get_zitch_point() > other.get_zitch_point():
            return 1
        if self.get_zitch_point() < other.get_zitch_point():
            return -1
        return 0

    def __repr__(self):
        return ",".join(c.get_name() for c in self._cards)

class Hands:
    def __init__(self, back, middle, front):
        self._back = back
        self._middle = middle
        self._front = front

    def get_back(self):
        return self._back

    def compare(self, other, detailed=False):
        front  = self._front.compare(other._front)
        middle = self._middle.compare(other._middle)
        back   = self._back.compare(other._back)
        if detailed:
            return [front, middle, back]

        if front == 0 and middle == 0 and back == 0:
            return 1 if self._front.compareZitchPoint(other._front) == 1 else -1

        if front <= 0 and middle <= 0 and back <= 0:
            return -1

        if front >= 0 and middle >= 0 and back >= 0:
            return 1

        return 0
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"

class PokerAlgo:
    def __init__(self):
        self._CardClass = Card
        self._HandClass = Hand
        self._HandsClass = Hands

    def get_card_class(self):
        return self._CardClass

    def get_hand_class(self):
        return self._HandClass

    def get_hands_class(self):
        return self._HandsClass

class Player:
    def __init__(self, cards, Algo: PokerAlgo):
        self._algo = Algo()
        self._cards = self._parse(cards)

    def _parse(self, s: str):
        arr = [self._algo.get_card_class()(x) for x in s.split(",")]
        arr.sort(key=lambda c: (c.get_rank(), c.get_suit()))
        return arr

    def get_best_hands(self):
        return self._algo.calc(self._cards)
      
