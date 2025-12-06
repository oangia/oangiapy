import random

class Deck:
    suit_order = {"s": 0, "c": 1, "d": 2, "h": 3}
    def __init__(self):
        self.reset()

    def reset(self):
        self._cards = [f"{r}{s}" for r in range(1, 14) for s in "scdh"]
        random.shuffle(self._cards)

    def draw(self, n):
        if n > len(self._cards):
            raise ValueError("not enough cards")
        return ",".join(sorted(
            [self._cards.pop() for _ in range(n)],
            key=lambda x: (int(x[:-1]), self.suit_order[x[-1]])
        ))

    def __len__(self):
        return len(self._cards)
