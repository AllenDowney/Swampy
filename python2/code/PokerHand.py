"""

This module contains code from
Think Python: an Introduction to Software Design
Allen B. Downey

"""

from Card import *

class PokerHand(Hand):
    def suit_hist(self):
        """build a histogram of the suits that appear in the hand"""
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def has_flush(self):
        """return True if the hand has a flush, False otherwise"""
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()

    # deal the cards and classify the hands
    for i in range(7):
        hand = PokerHand()
        deck.move_cards(hand, 7)
        hand.sort()
        print hand
        print hand.has_flush()
        print ''




