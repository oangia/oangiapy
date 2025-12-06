import random

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self._cards = [f"{r}{s}" for r in range(1, 14) for s in "scdh"]
        random.shuffle(self._cards)

    def draw(self, n):
        if n > len(self._cards):
            raise ValueError("not enough cards")
        return ",".join([self._cards.pop() for _ in range(n)])

    def __len__(self):
        return len(self._cards)
