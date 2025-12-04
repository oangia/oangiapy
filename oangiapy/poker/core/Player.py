class Player:
    def __init__(self, cards, Algo: Algorithm):
        self._algo = Algo()
        self._cards = self._parse(cards)

    def _parse(self, s: str):
        arr = [self._algo.get_card_class()(x) for x in s.split(",")]
        arr.sort(key=lambda c: (c.get_rank(), c.get_suit()))
        return arr

    def get_best_hands(self):
        return self._algo.calc(self._cards)
