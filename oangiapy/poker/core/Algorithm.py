class Algorithm:
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
