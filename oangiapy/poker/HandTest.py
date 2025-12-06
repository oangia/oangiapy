from oangiapy.poker.Deck import Deck
from oangiapy.poker.pokerv1 import Card, Hand

class HandTest:
    def __init__(self):
        pass
    def test(self):
        deck = Deck()
        
        for i in range(0, 9):
            cards = deck.draw(5)
            hand = Hand([Card(c) for c in cards.split(",")])
            while hand.get_type() != i:
                deck.reset()
                cards = deck.draw(5)
                hand = Hand([Card(c) for c in cards.split(",")])
        
            print(",".join(c.get_name() for c in hand.get_cards()), hand.get_type_str())

    def test2(self):
        cases = [

            # -------------------
            # STRAIGHT FLUSH (9)
            # -------------------
            ("1s,2s,3s,4s,5s", Hand.STRAIGHTFLUSH, 5),
            ("1s,10s,11s,12s,13s", Hand.STRAIGHTFLUSH, 14),
        
            # -------------------
            # FOUR OF A KIND (8)
            # -------------------
            ("9c,9d,9h,9s,2d", Hand.FOURKIND, 9),
            ("5h,5d,5s,5c,13d", Hand.FOURKIND, 5),
        
            # -------------------
            # FULL HOUSE (7)
            # -------------------
            ("3s,3d,3h,8c,8d", Hand.FULLHOUSE, 3),
            ("12s,12d,13h,13c,13s", Hand.FULLHOUSE, 13),
        
            # -------------------
            # FLUSH (6)
            # -------------------
            ("2s,5s,7s,8s,13s", Hand.FLUSH, 13),
            ("3c,6c,9c,11c,12c", Hand.FLUSH, 12),
        
            # -------------------
            # STRAIGHT (5)
            # -------------------
            ("4d,5h,6s,7c,8d", Hand.STRAIGHT, 8),
            ("1h,10h,11s,12c,13d", Hand.STRAIGHT, 14),
            ("1s,2d,3h,4c,5s", Hand.STRAIGHT, 5),   # wheel (A2345)
        
            # -------------------
            # THREE OF A KIND (4)
            # -------------------
            ("7s,7c,7d,2h,9c", Hand.THREEKIND, 7),
            ("11h,11d,11c,4s,6d", Hand.THREEKIND, 11),
        
            # -------------------
            # TWO PAIR (3)
            # -------------------
            ("9s,9c,4h,4d,2s", Hand.TWOPAIR, 9),
            ("13s,13d,3h,3s,8c", Hand.TWOPAIR, 13),
        
            # -------------------
            # ONE PAIR (2)
            # -------------------
            ("5s,5d,9c,11h,12s", Hand.ONEPAIR, 5),
            ("1s,1d,7h,4c,2s", Hand.ONEPAIR, 14),
        
            # -------------------
            # ZITCH (HIGH CARD) (1)
            # -------------------
            ("2s,5d,7c,9h,13d", Hand.ZITCH, 13),
            ("3c,6s,8d,11h,12c", Hand.ZITCH, 12),
        ]
        results = []
        for cards_str, expect_type, expect_point in cases:
            cards = [Card(x) for x in cards_str.split(",")]
            hand = Hand(cards)
        
            t = hand.get_type()
            p = hand.get_point()
        
            ok_type = (t == expect_type)
            ok_point = (p == expect_point)
            ok = ok_type and ok_point
        
            print(f"{cards_str}")
            print(f"  type:  {t}  ({'OK' if ok_type else f'FAIL expect {expect_type}'})")
            print(f"  point: {p}  ({'OK' if ok_point else f'FAIL expect {expect_point}'})")
            print()
        
            results.append(ok)
        
        print(f"Passed {sum(results)}/{len(results)}")
