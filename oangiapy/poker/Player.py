class Algorithm:
    def __init__(self, cards):
        self._cards = cards.split(",")

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

    def fast_scan(self):
        return (False, None)
      
class Player:
    def __init__(self, cards, Algo: Algorithm):
        self._algo = Algo(cards)

    def get_best_hands(self):
        return self._algo.get_best_hands()
