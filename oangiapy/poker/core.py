class Card:
    def __init__(self, name):
        self._name = name
        self._rank = int(name[:-1])
        self._suit = name[-1]

    def get_rank(self):
        return self._rank

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

class Hand:
    def __init__(self, cards, Detector = HandDetector):
        self._cards = cards
        self._detector = Detector(self._cards)

    def get_cards(self):
        return self._cards
        
    def get_type(self):
        return self.self._detector.get_type()

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

class HandDetector:
    def __init__(self, cards):
        self.cards = cards
        self._type = HandType.ZITCH
        self._point = 0
        
    def get_type(self):
        return self._type

    def get_point(self):
        return self._point

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

    def fast_scan(self, cards):
        self._cards = cards

        return (False, None)
 
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
      
