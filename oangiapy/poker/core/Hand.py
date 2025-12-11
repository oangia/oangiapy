from oangiapy.poker.core.HandDetector import HandDetector

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
        self._detector = HandDetector

    def get_cards(self):
        return self._cards

    def get_type(self):
        return self._detector.get_type()

    def get_point(self):
        return self._detector.get_point()

    def get_type_str(self):
        names = ["Zitch", "One Pair", "Two Pairs", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
        return names[self.get_type()] 

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
