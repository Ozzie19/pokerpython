import random

# Define a class to represent a playing card
class Card:
    # Initialize a card with a rank and a suit
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # Return a string representation of the card
    def __repr__(self):
        return f'{self.rank} of {self.suit}'

# Define a class to represent a deck of cards
class Deck:
    # Initialize an empty deck of cards and build it
    def __init__(self):
        self.cards = []
        self.build()

    # Build a standard deck of 52 cards
    def build(self):
        ranks = [str(n) for n in range(2, 11)] + list('JQKA')
        suits = ['spades', 'clubs', 'diamonds', 'hearts']
        # Create a card for each combination of rank and suit
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    # Shuffle the deck of cards
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal (remove and return) the top card from the deck
    def deal(self):
        return self.cards.pop()