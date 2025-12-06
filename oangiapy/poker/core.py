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

    def get_type(self):
        return Hand.ZITCH

    def get_type_str(self):
        names = ["Zitch", "One Pair", "Two Pairs", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
        return names[self.get_type()] 

    def get_point(self):
        return 0

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
        return ",".join(c.get_name() for c in self._cards) + " " + self.get_type_str() + " " + str(self.get_point())    

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

    def compare_point(self, other):
        if self.get_point() == other.get_point():
            return 0
        if self.get_point() > other.get_point():
            return 1
        return -1

    def compare_dominance(self, other):
        _back, _middle, _front = self.compare(other)
        if _back == 0 and _middle ==0 and _front == 0:
            return 0

        if _back >=0 and _middle >= 0 and _front >= 0:
            return 1

        if _back <=0 and _middle <= 0 and _front <= 0:
            return -1

        return 0
    
    def compare(self, other):
        _back = self._back.compare(other.get_back())
        _middle = self._middle.compare(other.get_middle())
        _front = self._front.compare(other.get_front())
        return (_back, _middle, _front)

    def __lt__(self, other):
        _back, _middle, _front = self.compare(other)
        if _back == 0:
            if _middle == 0:
                return _front == -1
            return _middle == -1
        return _back == -1

    def __gt__(self, other):
        return self._point > other._point
        
    def __repr__(self):
        return f"Back: {self._back}\nMiddle: {self._middle}\nFront: {self._front}"
