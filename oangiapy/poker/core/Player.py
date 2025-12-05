from oangiapy.poker.core.Algorithm import Algorithm

class Player:
    def __init__(self, cards, Algo: Algorithm):
        self._algo = Algo(cards)

    def get_best_hands(self):
        return self._algo.get_best_hands()
