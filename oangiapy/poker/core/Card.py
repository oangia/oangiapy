class BaseCard:
    def __init__(self, name):
        self._name = name
        self._rank = int(name[:-1])
        self._suit = name[-1]

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def get_name(self):
        return self._name

    def __eq__(self, other):
        return self._name == other.get_name()

    def __lt__(self, other):
        return self._rank < other.get_rank()

    def __repr__(self):
        return self._name

class Card(BaseCard):
    def __init__(self, name):
        super().__init__(name)
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point
