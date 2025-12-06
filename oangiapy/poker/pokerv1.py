from oangiapy.poker.core import Hands as BaseHands
from oangiapy.poker.core import Card as BaseCard
from oangiapy.poker.core import Hand as BaseHand
from oangiapy.poker.core import Hand, Algorithm, Player
        
class Card(BaseCard):
    def __init__(self, name):
        super().__init__(name)
        self._rank_value = 12 if self.get_rank() == 1 else self.get_rank() - 2
        self._rank_point = pow(2, self._rank_value)

    def get_rank_value(self):
        return self._rank_value

    def get_rank_point(self):
        return self._rank_point

class Hand(BaseHand):
    def __init__(self, cards):
        super().__init__(cards);
        self._typeDetector = HandTypeDetector(self)
        self._pointCalcilator = HandPointCalculator(self)
        
    def get_type(self):
        return self._typeDetector.get_type()

    def get_point(self):
        return self._pointCalcilator.get_point()
        
class HandTypeDetector:
    def __init__(self, hand):
        self._hand = hand
        self._type = Hand.ZITCH

        self.zitch_point = sum(card.get_rank_point() for card in hand.get_cards())
        self.suit_str = ''.join(card.get_suit() for card in hand.get_cards())
        if self._hasDup():
            self._type = self._detectPair()
        else:
            self._type = self._detectZitch()
        
    def get_type(self):
        return self._type

    def _hasDup(self):
        return any(self._hand.get_cards()[i].get_rank() == self._hand.get_cards()[i+1].get_rank() for i in range(len(self._hand.get_cards()) - 1))

    def _detectZitch(self):
        self.straight = self.zitch_point in [
            4111, 31, 62, 124, 248, 496, 992, 1984, 3968, 7936
        ]
        self.flush = self.suit_str in ['sssss', 'ccccc', 'ddddd', 'hhhhh']

        if self.straight and self.flush:
            return Hand.STRAIGHTFLUSH
        if self.straight:
            return Hand.STRAIGHT
        if self.flush:
            return Hand.FLUSH
        return Hand.ZITCH

    def _detectPair(self):
        ranks = [card.get_rank() for card in self._hand.get_cards()]
        freqs = {}
        for r in ranks:
            freqs[r] = freqs.get(r, 0) + 1

        counts = sorted(freqs.values(), reverse=True)

        if counts[0] == 4:
            return Hand.FOURKIND
        if counts[0] == 3 and counts[1] == 2:
            return Hand.FULLHOUSE
        if counts[0] == 3:
            return Hand.THREEKIND
            
        if counts[0] == 2 and counts[1] == 2:
            return Hand.TWOPAIR
        if counts[0] == 2:
            return Hand.ONEPAIR

class HandPointCalculator:
    def __init__(self, hand):
        self._hand = hand
        self._point = 0
        self._zitch_point = sum(card.get_rank_point() for card in self._hand.get_cards())
        match self._hand.get_type():
            case Hand.ZITCH | Hand.STRAIGHT | Hand.FLUSH | Hand.STRAIGHTFLUSH:
                self._point = self._zitch_point * 100 / 7937
            case Hand.ONEPAIR:
                for i in range(4):
                    if self._hand.get_cards()[i].get_rank() == self._hand.get_cards()[i+1].get_rank():
                        self._point = self._hand.get_cards()[i].get_rank_value()
                        zitch = self.zitch_point - self._hand.get_cards()[i].get_rank_point() * 2
                        break
            case Hand.TWOPAIR:
                self._point = self._hand.get_cards()[1].get_rank_point() + self._hand.get_cards()[3].get_rank_point()
                self._point = self._point * 100 / 7937
                zitch = sum(
                    c.get_rank_value() if c.get_rank() not in (self._hand.get_cards()[1].get_rank(), self._hand.get_cards()[3].get_rank())
                    else 0
                    for c in self._hand.get_cards()
                )
            case Hand.THREEKIND | Hand.FULLHOUSE | Hand.FOURKIND:
                self._point = self._hand.get_cards()[2].get_rank_value() * 100 / 13

    def get_point(self):
        return self._point
            
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
        if f_level == Hand.THREEKIND:
            self._point += system['ThreeKind']['f'] + f_point
        elif f_level == Hand.ONEPAIR:
            self._point += system['OnePair']['f'] + f_point
        elif f_level == Hand.ZITCH:
            if f_point >= 50:
                self._point += system['Zitch']['f']['ak'] + f_point
            else:
                self._point += system['Zitch']['f']['qj'] + f_point

        # Middle
        if m_level == Hand.ZITCH:
            self._point += system['Zitch']['m'] + m_point
        elif m_level == Hand.ONEPAIR:
            if f_point >= 50:
                self._point += system['OnePair']['m']['ak'] + m_point
            else:
                self._point += system['OnePair']['m']['qj'] + m_point
        elif m_level == Hand.TWOPAIR:
            self._point += system['TwoPair']['m'] + m_point
            self._bonus += m_point
        elif m_level == Hand.THREEKIND:
            self._point += system['ThreeKind']['m'] + m_point
        elif m_level == Hand.STRAIGHT:
            self._point += system['Straight']['m'] + m_point
        elif m_level == Hand.FLUSH:
            self._point += system['Flush']['m'] + m_point
        elif m_level == Hand.FULLHOUSE:
            self._point += system['FullHouse']['m'] + m_point
            self._bonus += m_point
        elif m_level == Hand.FOURKIND:
            self._point += system['FourKind']['m'] + m_point
            self._bonus += m_point
        elif m_level == Hand.STRAIGHTFLUSH:
            self._point += system['StraightFlush']['m'] + m_point
            self._bonus += m_point

        # Back
        if b_level == Hand.ZITCH:
            self._point += system['Zitch']['b'] + b_point
        elif b_level == Hand.ONEPAIR:
            self._point += system['OnePair']['b'] + b_point
        elif b_level == Hand.TWOPAIR:
            self._point += system['TwoPair']['b'] + b_point
        elif b_level == Hand.THREEKIND:
            self._point += system['ThreeKind']['b'] + b_point
        elif b_level == Hand.STRAIGHT:
            self._point += system['Straight']['b'] + b_point
        elif b_level == Hand.FLUSH:
            self._point += system['Flush']['b'] + b_point
        elif b_level == Hand.FULLHOUSE:
            self._point += system['FullHouse']['b'] + b_point
            self._bonus += b_point * 2
        elif b_level == Hand.FOURKIND:
            self._point += system['FourKind']['b'] + b_point
            self._bonus += b_point * 2
        elif b_level == Hand.STRAIGHTFLUSH:
            self._point += system['StraightFlush']['b'] + b_point
            self._bonus += b_point * 2

        self._point = round(self._point, 2)
        self._bonus = round(self._bonus, 2)
            
          
