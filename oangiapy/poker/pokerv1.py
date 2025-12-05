from oangiapy.poker.core import Card as BaseCard
from oangiapy.poker.core import HandDetector as BaseHandDetector
from oangiapy.poker.core import Hands as BaseHands
from oangiapy.poker.core import Hand as BaseHand
from oangiapy.poker.core import HandType, Algorithm, Player

class Hand(BaseHand):
    def __init__(self, cards, Detector = HandDetector):
        super().__init__(cards, Detector = Detector)
        
class Card(BaseCard):
    def __init__(self, name):
        super().__init__(name)
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point

class HandDetector(BaseHandDetector):
    def __init__(self, cards):
        self.cards = cards

        self.zitch_point = sum(card.get_rank_point() for card in self.cards)
        self.suit_str = ''.join(card.get_suit() for card in self.cards)
        if self._hasDup():
            detect = self._detectPair()
        else:
            detect = self._detectZitch()

        self._type, self._point = detect
        
    def get_type(self):
        return self._type

    def get_point(self):
        return self._point

    def _hasDup(self):
        return any(self.cards[i].get_rank() == self.cards[i+1].get_rank() for i in range(len(self.cards) - 1))

    def _detectZitch(self):
        self.straight = self.zitch_point in [
            4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936
        ]
        self.flush = self.suit_str in ['sssss', 'ccccc', 'ddddd', 'hhhhh']

        if self.straight and self.flush:
            return (HandType.STRAIGHTFLUSH, self.zitch_point)
        if self.straight:
            return (HandType.STRAIGHT, self.zitch_point)
        if self.flush:
            return (HandType.FLUSH, self.zitch_point)

        return (HandType.ZITCH, self.zitch_point)

    def _detectPair(self):
        ranks = [card.get_rank() for card in self.cards]
        freqs = {}
        for r in ranks:
            freqs[r] = freqs.get(r, 0) + 1

        counts = sorted(freqs.values(), reverse=True)

        if counts[0] == 4:
            return (HandType.FOURKIND, self.cards[2].get_rank_value())

        if counts[0] == 3 and counts[1] == 2:
            return (HandType.FULLHOUSE, self.cards[2].get_rank_value())

        if counts[0] == 3:
            return (HandType.THREEKIND, self.cards[2].get_rank_value())

        if counts[0] == 2 and counts[1] == 2:
            point = self.cards[1].get_rank_point() + self.cards[3].get_rank_point()
            zitch = sum(
                c.get_rank_value() if c.get_rank() not in (self.cards[1].get_rank(), self.cards[3].get_rank())
                else 0
                for c in self.cards
            )
            return (HandType.TWOPAIR, point + zitch / 7937)

        if counts[0] == 2:
            for i in range(4):
                if self.cards[i].get_rank() == self.cards[i+1].get_rank():
                    point = self.cards[i].get_rank_value()
                    zitch = self.zitch_point - self.cards[i].get_rank_point() * 2
                    break
            return (HandType.ONEPAIR, point + zitch / 7937)
            
class Hands(BaseHands):
    def __init__(self, back, middle, front):
        super().__init__(back, middle, front)
        self._bonus = 0
        self.point_calc()
        
    def point_calc(self):
        system = {
            'StraightFlush': {'m': 6200, 'b': 4000},
            'FourKind': {'m': 5300, 'b': 3500},
            'FullHouse': {'m': 2500, 'b': 1600},
            'Flush': {'m': 1500, 'b': 1200},
            'Straight': {'m': 1400, 'b': 800},
            'ThreeKind': {'f': 3000, 'm': 1100, 'b': 600},
            'TwoPair': {'m': 900, 'b': 500},
            'OnePair': {'f': 1300, 'm': {'ak': 700, 'qj': 300}, 'b': 200},
            'Zitch': {'f': {'ak': 1000, 'qj': 400}, 'm': 100, 'b': 0}
        }

        front, middle, back = self._front, self._middle, self._back
        f_level, f_point = front.get_type(), front.get_point()
        m_level, m_point = middle.get_type(), middle.get_point()
        b_level, b_point = back.get_type(), back.get_point()

        # Front
        if f_level == HandType.THREEKIND:
            self._point += system['ThreeKind']['f'] + f_point
        elif f_level == HandType.ONEPAIR:
            self._point += system['OnePair']['f'] + f_point
        elif f_level == HandType.ZITCH:
            if f_point >= 50:
                self._point += system['Zitch']['f']['ak'] + f_point
            else:
                self._point += system['Zitch']['f']['qj'] + f_point

        # Middle
        if m_level == HandType.ZITCH:
            self._point += system['Zitch']['m'] + m_point
        elif m_level == HandType.ONEPAIR:
            if f_point >= 50:
                self._point += system['OnePair']['m']['ak'] + m_point
            else:
                self._point += system['OnePair']['m']['qj'] + m_point
        elif m_level == HandType.TWOPAIR:
            self._point += system['TwoPair']['m'] + m_point
            self._bonus += m_point
        elif m_level == HandType.THREEKIND:
            self._point += system['ThreeKind']['m'] + m_point
        elif m_level == HandType.STRAIGHT:
            self._point += system['Straight']['m'] + m_point
        elif m_level == HandType.FLUSH:
            self._point += system['Flush']['m'] + m_point
        elif m_level == HandType.FULLHOUSE:
            self._point += system['FullHouse']['m'] + m_point
            self._bonus += m_point
        elif m_level == HandType.FOURKIND:
            self._point += system['FourKind']['m'] + m_point
            self._bonus += m_point
        elif m_level == HandType.STRAIGHTFLUSH:
            self._point += system['StraightFlush']['m'] + m_point
            self._bonus += m_point

        # Back
        if b_level == HandType.ZITCH:
            self._point += system['Zitch']['b'] + b_point
        elif b_level == HandType.ONEPAIR:
            self._point += system['OnePair']['b'] + b_point
        elif b_level == HandType.TWOPAIR:
            self._point += system['TwoPair']['b'] + b_point
        elif b_level == HandType.THREEKIND:
            self._point += system['ThreeKind']['b'] + b_point
        elif b_level == HandType.STRAIGHT:
            self._point += system['Straight']['b'] + b_point
        elif b_level == HandType.FLUSH:
            self._point += system['Flush']['b'] + b_point
        elif b_level == HandType.FULLHOUSE:
            self._point += system['FullHouse']['b'] + b_point
            self._bonus += b_point * 2
        elif b_level == HandType.FOURKIND:
            self._point += system['FourKind']['b'] + b_point
            self._bonus += b_point * 2
        elif b_level == HandType.STRAIGHTFLUSH:
            self._point += system['StraightFlush']['b'] + b_point
            self._bonus += b_point * 2

        self._point = round(self._point, 2)
        self._bonus = round(self._bonus, 2)
            
          
