class Card:
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

    def __repr__(self):
        return self._name
      
