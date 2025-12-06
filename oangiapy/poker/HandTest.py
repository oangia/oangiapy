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
        
            print(",".join(c.get_name() for c in hand.get_cards()), hand.get_type())
