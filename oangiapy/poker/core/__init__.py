from itertools import combinations
import random

class Card:
    def __init__(self, name):
        self._name = name
        self._rank = int(name[:-1])
        self._suit = name[-1]

    def get_name(self):
        return self._name
        
    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def __eq__(self, other):
        return self._name == other.get_name()

    def __lt__(self, other):
        return self._rank < other.get_rank()

    def __repr__(self):
        return self._name

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

    def get_cards(self):
        return self._cards

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

class Hands:
    def __init__(self, back, middle, front):
        self._back = back
        self._middle = middle
        self._front = front
        self._point = 0

    def get_back(self):
        return self._back

    def get_middle(self):
        return self._middle

    def get_front(self):
        return self._front    

    def get_point(self):
        return self._point

    def __lt__(self, other):
        _back = self._back.compare(other._back)
        if _back == 0:
            _middle = self._middle.compare(other._middle)
            if _middle == 0:
                _front = self._front.compare(other._front)
                return _front == -1
            return _middle == -1
        return _back == -1

    def __gt__(self, other):
        return self._point > other._point

    def compare(self, other, detailed=False):
        front  = self._front.compare(other._front)
        middle = self._middle.compare(other._middle)
        back   = self._back.compare(other._back)
        if detailed:
            return [front, middle, back]

        if front == 0 and middle == 0 and back == 0:
            return 0

        if front <= 0 and middle <= 0 and back <= 0:
            return -1

        if front >= 0 and middle >= 0 and back >= 0:
            return 1

        return 0
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"

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
      
class Player:
    def __init__(self, cards, Algo: Algorithm):
        self._algo = Algo(cards)

    def get_best_hands(self):
        return self._algo.get_best_hands()

class Deck:
    suit_order = {"s": 0, "c": 1, "d": 2, "h": 3}
    def __init__(self):
        self.reset()

    def reset(self):
        self._cards = [f"{r}{s}" for r in range(1, 14) for s in "scdh"]
        random.shuffle(self._cards)

    def draw(self, n):
        if n > len(self._cards):
            raise ValueError("not enough cards")
        return ",".join(sorted(
            [self._cards.pop() for _ in range(n)],
            key=lambda x: (int(x[:-1]), self.suit_order[x[-1]])
        ))

    def __len__(self):
        return len(self._cards)
