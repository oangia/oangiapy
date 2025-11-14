import random
class Card:
    def __init__(self, name):
        self.name = name
        self.rank = int(name[:-1])
        self.suit = name[-1]

        self.rank_value = 12 if self.rank == 1 else self.rank - 2
        self.rank_point = pow(2, self.rank_value)

    def __repr__(self):
        return self.name

class Hand:
  def __init__(self, cards):
    self.ranks = {
        'Zitch': 0,
        'One Pair': 1,
        'Two Pair': 2,
        'Three of a Kind': 3,
        'Straight': 4,
        'Flush': 5,
        'Full House': 6,
        'Four of a Kind': 7,
        'Straight Flush': 8
    }
    self.cards = cards
    self.zitch_point = sum(card.rank_point for card in self.cards)
    self.suit_str = ''.join(card.suit for card in self.cards)
    if self.hasDup():
      detect = self.detectPair()
    else:
      detect = self.detectZitch()
    self.detect = detect

  def hasDup(self):
    return any(self.cards[i].rank == self.cards[i+1].rank for i in range(4))

  def detectZitch(self):
    
    self.straight = self.zitch_point in [4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936]
    self.flush = self.suit_str in ['sssss', 'ccccc', 'ddddd', 'hhhhh']
    
    if self.straight and self.flush:
      return ("Straight Flush", self.zitch_point)
    if self.straight:
      return ("Straight", self.zitch_point)
    if self.flush:
      return ("Flush", self.zitch_point)
    return ("Zitch", self.zitch_point)

  def detectPair(self):
    self.ranks = [card.rank for card in self.cards]
    freqs = {}
    for r in self.ranks:
        if r in freqs:
            freqs[r] += 1
        else:
            freqs[r] = 1
    # Get counts in descending order
    counts = sorted(freqs.values(), reverse=True)
    if counts[0] == 4:
        return ("Four of a Kind", self.cards[2].rank_value)
    elif counts[0] == 3 and counts[1] == 2:
        return ("Full House", self.cards[2].rank_value)
    elif counts[0] == 3:
        return ("Three of a Kind", self.cards[2].rank_value)
    elif counts[0] == 2 and counts[1] == 2:
        point = self.cards[1].rank_point + self.cards[3].rank_point
        zitch = sum(card.rank_value if card.rank != self.cards[1].rank and card.rank != self.cards[3].rank else 0 for card in self.cards)
        return ("Two Pair", point + zitch / 7937)
    elif counts[0] == 2:
        for i in range(4):
          if self.cards[i].rank == self.cards[i+1].rank:
            point = self.cards[i].rank_value
            zitch = self.zitch_point - self.cards[i].rank_point * 2
            break
        return ("One Pair", point + zitch / 7937)

class Deck:
    def __init__(self):
        ranks = list(range(1, 14))  # 1 to 13
        suits = ['s', 'c', 'd', 'h']
        self.cards = [f"{r}{s}" for r in ranks for s in suits]

    def deal(self, n=5):
        hand = random.sample(self.cards, n)
        # sort by rank first, then by suit order s < c < d < h
        suit_order = {'s': 0, 'c': 1, 'd': 2, 'h': 3}
        hand.sort(key=lambda x: (int(x[:-1]), suit_order[x[-1]]))
        return hand

deck = Deck()
   # deal 5 random cards
hands = ["Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "Zitch"]
for handName in hands:
    cards = deck.deal()
    hand = Hand([Card(cards[0]), Card(cards[1]), Card(cards[2]), Card(cards[3]), Card(cards[4])])
    while handName != hand.detect[0]:
        cards = deck.deal()
        hand = Hand([Card(cards[0]), Card(cards[1]), Card(cards[2]), Card(cards[3]), Card(cards[4])])
    print(hand.detect, cards)
hand = Hand([Card("1s"), Card("2s"), Card("2c"), Card("12s"), Card("13s")])
print(hand.detect)
