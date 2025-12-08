from itertools import combinations

class Algorithm:
    def __init__(self, cards):
        self._cards = cards.split(",")

    def split_5_5_3_index(self):
        index = range(13)
        res = []
        for back in combinations(index, 5):
            back_set = set(back)
            remain1 = [c for c in index if c not in back_set]
            for middle in combinations(remain1, 5):
                middle_set = set(middle)
                front = [c for c in remain1 if c not in middle_set]
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
