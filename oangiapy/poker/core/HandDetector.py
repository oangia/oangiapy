class HandDetector:
    def __init__(self, cards):
        self.cards = cards
        self._type = HandType.ZITCH
        self._point = 0
        
    def get_type(self):
        return self._type

    def get_point(self):
        return self._point
