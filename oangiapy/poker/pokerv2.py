import time

start = time.time()
from oangiapy.poker.pokerv1 import Card, Hand, Hands
from oangiapy.poker.Player import Algorithm, Player
from itertools import combinations

class BruteForce(Algorithm):
    def __init__(self, cards):
        self._cards = [Card(card) for card in cards.split(",")]
        self._cards.sort(key=lambda card: (card.get_rank(), card.get_suit()))

    def get_best_hands(self):
        handses_index = self.split_5_5_3_index()
        print("index:", time.time() - start)
        handses = self._get_handses_from_index(handses_index)
        print("pre-sort:", time.time() - start)
        #handses.sort(reverse=True)
        #new_handses = self._remove_weak_handses(handses)
        print("after-sort:", time.time() - start)
        print(len(handses))
        print(handses[-1])
        return handses[0]

    def _remove_weak_handses(self, handses):
        new_handses = []
        length = len(self._handses)
        for i in range(length):
            for j in range(i + 1, length):
                if handses[i].compare(handses[j]) == 1:
                    new_handses.append(handses[i])
                    break
                if handses[i].compare(handses[j]) == -1:
                    new_handses.append(handses[j])
                    break

        return self.new_handses

    def _get_handses_from_index(self, handses_index):
        handses = [
            Hands(Hand([self._cards[i] for i in hands[0]]), Hand([self._cards[i] for i in hands[1]]), Hand([self._cards[i] for i in hands[2]])) for hands in handses_index
        ]
        return handses

    def _check_weak_hands(self, check):
        for hands in self.new_handses:
            if hands.compare(check) == 1:
                return True
        return False


cards = "1s,2s,3s,4s,5s,6s,7s,8s,9s,10s,11s,12s,13s"
player = Player(cards, Algo = BruteForce)
results = player.get_best_hands()
print(results)
# your code
print("elapsed:", time.time() - start)

import time

start = time.time()
import numpy as np
from itertools import combinations
#from oangiapy.poker.Deck import Deck

cards = "1h,2h,3h,4h,5h,6h,7h,8h,9h,10h,11h,12h,13h".split(',')

def vectorize_cards(cards):
    # 1) Base card values
    smap = {'s':0, 'c':1, 'h':7, 'd':37}
    mat = np.zeros((13, 4), dtype=int)
    for i, c in enumerate(cards):
        rank = int(c[:-1])
        suit = smap[c[-1]]
        value = 12 if rank == 1 else rank - 2
        power = 1 << value
        mat[i] = (rank, suit, value, power)

    return mat

def get_idx():
    # 2) Generate 5-5-3 combinations (indices)
    arr = np.zeros((72072, 13), dtype=int)
    row = 0
    for back in combinations(range(13), 5):
        remain1 = [x for x in range(13) if x not in back]
        for middle in combinations(remain1, 5):
            front = [x for x in remain1 if x not in middle]
            arr[row, :5] = back
            arr[row, 5:10] = middle
            arr[row, 10:13] = front
            row += 1

    return arr

def get_idx5():
    # 2) Generate 5-5-3 combinations (indices)
    arr = np.zeros((72072, 5), dtype=int)
    row = 0
    for back in combinations(range(13), 5):
        arr[row, :5] = back
        row += 1

    return arr

cards_vectorized = vectorize_cards(cards)
print("vector", cards_vectorized.shape)
print(time.time() - start)
idx = get_idx()
handses = cards_vectorized[idx]
print("handses", handses.shape)
print(time.time() - start)
def get_info(idx):
    n = idx.shape[1]
    ranks = idx[:, :, 0]
    suits = idx[:, :, 1]
    values = idx[:, :, 2]
    points = idx[:, :, 3]

    point_sum = points.sum(axis=1)
    suit_sum = suits.sum(axis=1)

    if n == 5:
        straight_targets = np.array([4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936])
        straight_flags = np.isin(point_sum, straight_targets).astype(int)
        flush_flags = np.array(suit_sum % n == 0).astype(int)
        straight_flush_flags = straight_flags * flush_flags
    elif n == 3:
        straight_targets = np.array([4099, 7, 14, 28, 56, 112, 224, 448, 896, 1792, 3584, 7168])
        straight_flags = np.zeros((72072, ), dtype=int)
        flush_flags = np.zeros((72072, ), dtype=int)
        straight_flush_flags = np.zeros((72072, ), dtype=int)

    cmp = (ranks[:, :-1] == ranks[:, 1:]).astype(int)
    pos = cmp.argmax(axis=1)        # gives *some* index even if none is True
    mask = cmp.any(axis=1)          # row has an equal pair?

    pos[~mask] = -1

    weights = (10 ** np.arange(n - 1))[::-1]
    weighted_sum = (cmp * weights).sum(axis=1)  # shape (N,)

    middle = values[:, 2]

    if n == 5:
        two = points[:, 1] + points[:, 3]
        zitch_two = point_sum - two * 2
    elif n == 3:
        two = np.zeros(72072, dtype=int)
        zitch_two = np.zeros(72072, dtype=int)
          # (N, M)
    pos_safe = pos.copy()

    # temporarily fix -1 so indexing won’t break
    pos_safe[pos_safe == -1] = 0

    # gather values
    one = points[np.arange(len(pos)), pos_safe]

    # replace entries that came from -1 with 0
    one[pos == -1] = 0
    zitch_one = point_sum - one * 2
    return np.stack([straight_flags, flush_flags, straight_flush_flags, point_sum, weighted_sum, middle, two, zitch_two, one, zitch_one], axis=1)

def get_point(idx):
    back_info = get_info(idx)

    out = np.zeros((72072, 9))

    zitch = back_info[:, 3]   # (72072,)
    middle_val = back_info[:, 5]
    two = back_info[:, 6]
    one = back_info[:, 8]
    out[:, [0, 4, 5, 8]] = zitch[:, None] * 100 / 7937
    out[:, [3, 6, 7]] = middle_val[:, None] * 100 / 13
    out[:, [1]] = one[:, None] * 100 / 4097
    out[:, [2]] = two[:, None] * 100 / 6145

    #middle = cal(handses[:, 5:10])
    #front = cal(handses[:, 10:13])
    maps = {111: 7, 1110: 7, 1101: 6, 1011: 6, 1100: 3, 110: 3, 11: 3, 1010:2, 101: 2, 1001: 2, 1000: 1, 100: 1, 10: 1, 1: 1, 0: 0}
    #col_front = front[:, 0] * 4 + front[:, 1] * 5 - front[:, 2] + np.array([maps[k] for k in front[:,4]])
    #col_middle = middle[:, 0] * 4 + middle[:, 1] * 5 - middle[:, 2] + np.array([maps[k] for k in middle[:,4]])
    col_back = back_info[:, 0] * 4 + back_info[:, 1] * 5 - back_info[:, 2] + np.array([maps[k] for k in back_info[:,4]])

    one_hot = np.eye(9)[col_back]

    result = col_back * 100 + (one_hot * out).sum(axis=1)
    return result

back_point = get_point(handses[:, :5])
middle_point = get_point(handses[:, 5:10])
front_point = get_point(handses[:, 10:13])

points = np.stack([back_point, middle_point, front_point], axis=1)
print("points", points.shape)
print(time.time() - start)
mask = (points[:, 1] > points[:, 0]) | (points[:, 2] > points[:, 1])
points[mask] = 0
count_zero = np.sum(np.all(points == 0, axis=1))
print(count_zero)

def sort_points(points):
    idx = np.lexsort((-points[:, 2], -points[:, 1], -points[:, 0]))
    return idx



idx = sort_points(points)
handses = handses[idx]
points = (points[idx] * 100).astype(int)
def remove_weak(filtered):
    for i in range(len(filtered) - 1):
        if filtered[i][1] >= filtered[i + 1][1] and filtered[i][2] >= filtered[i + 1][2]:
            filtered[i + 1] = 0
    return filtered

strong = remove_weak(points)
idx = sort_points(points)
handses = handses[idx]
points = (points[idx] * 100).astype(int)

count_zero = np.sum(np.all(strong == 0, axis=1))
print(count_zero)
print(strong)
# Columns not in cols_to_set remain unchanged

print(time.time() - start)


import numpy as np
from sklearn.neural_network import MLPRegressor

# Example length
n = 5

# Training data: deterministic shuffle
# Rule: [a,b,c,d,e] -> [c,d,e,a,b]
X = np.array([
    [1, 2, 3, 4, 5],
    [10, 20, 30, 40, 50],
    [2, 4, 6, 8, 10],
])

y = np.array([
    [3, 4, 5, 1, 2],
    [30, 40, 50, 10, 20],
    [6, 8, 10, 2, 4],
])

# Basic neural network
model = MLPRegressor(
    hidden_layer_sizes=(32,),
    activation='relu',
    solver='adam',
    max_iter=100000
)

model.fit(X, y)

# Test
test_in = np.array([[100, 200, 300, 400, 500]])
pred = model.predict(test_in)

print(pred)


import random

# Build deck
ranks = list(range(1, 13+1))
suits = ['s', 'c', 'd', 'h']
DECK = [f"{r}{s}" for r in ranks for s in suits]

# Order by rank then suit priority
suit_order = {'s':0, 'c':1, 'd':2, 'h':3}
def sort_cards(cards):
    return sorted(cards, key=lambda x: (int(x[:-1]), suit_order[x[-1]]))

def pick_two_hands():
    cards = random.sample(DECK, 10)
    h1 = sort_cards(cards[:5])
    h2 = sort_cards(cards[5:])
    return h1, h2

def save_result(h1, h2, label, path="data.txt"):
    with open(path, "a") as f:
        f.write(f"{','.join(h1)} | {','.join(h2)} | {label}\n")

# Example run loop
while True:
    h1, h2 = pick_two_hands()
    print("Hand 1:", h1)
    print("Hand 2:", h2)
    label = input("Enter -1, 0, or 1 (or q to quit): ")
    if label.lower() == "q":
        break
    if label in ["-1","0","1"]:
        save_result(h1, h2, label)
        print("Saved.\n")
    else:
        print("Invalid input.\n")
