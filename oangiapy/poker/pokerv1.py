from oangiapy.poker.core import HandDetector as BaseHandDetector
from oangiapy.poker.core import Hands as BaseHands
from oangiapy.poker.core import Card, Hand, Algorithm, Player
        
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
            
          
