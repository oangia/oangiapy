from oangiapy.poker.core.HandDetector import HandDetector

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
      
