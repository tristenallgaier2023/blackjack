import random

class Card:
    def __init__(self, ranking, card_suit):
        self.rank = ranking
        self.suit = card_suit

class Deck:
    # ranks: 1 == ace, 2-10, 11 == jack, 12 == queen, 13 == king
    # suits: 1 == spades, 2 == clubs, 3 == hearts, 4 == diamonds
    def __init__(self, decks, rigged_deck=None):
        self.deck_count = decks
        if not rigged_deck:
            self.master_deck = []
            for rank in range(1, 14):
                for suit in range(1, 5):
                    self.master_deck.append(Card(rank, suit))
        else:
            self.master_deck = rigged_deck
        self.deck = []

    # resets and shuffles the decks
    def shuffle(self):
        remaining = []
        for i in range(len(self.master_deck)):
            remaining.append([self.deck_count, i])
        self.deck = []
        i = 0
        while i < len(self.master_deck) * self.deck_count:
            n = random.randint(0, len(remaining) - 1)
            card = self.master_deck[remaining[n][1]]
            self.deck.append(Card(card.rank, card.suit))
            remaining[n][0] -= 1
            if remaining[n][0] < 1:
                remaining.pop(n)
            i += 1

    # removes a card from the deck and returns it
    def draw(self):
        if not self.deck:
            print("Deck is empty")
            return None
        n = random.randint(0, len(self.deck) - 1)
        card = self.deck[n]
        self.deck.pop(n)
        return card
