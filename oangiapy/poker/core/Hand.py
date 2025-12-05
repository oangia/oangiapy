from oangiapy.poker.core.HandDetector import HandDetector

class Hand:
    def __init__(self, cards, Detector = HandDetector):
        self._cards = cards
        self._detector = Detector(self._cards)

    def get_cards(self):
        return self._cards
        
    def get_type(self):
        return self._detector.get_type()

    def get_point(self):
        return self._detector.get_point()

    def check_dup(self, other):
        return any(c1.name == c2.name for c1 in self._cards for c2 in other.get_cards())

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
        return self.compare(other) < 0

    def __repr__(self):
        return ",".join(c.get_name() for c in self._cards) + " " + str(self.get_type())
      
