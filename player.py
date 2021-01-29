from game import BlackJack
from deck import Card

class Player:
    def __init__(self, cutoff, decks, starting_cash, hitsoft17, hands, custom_deck=None):
        self.hand_count = hands
        self.game = BlackJack(cutoff, decks, starting_cash, hitsoft17, False, custom_deck)

    def basicStrat(self, bet):
        for i in range(self.hand_count):
            self.game.newHand(bet)
            while self.game.active:
                score, soft = self.game.playerScore()
                upcard = self.game.dealer_cards[0].rank
                if upcard > 10: upcard = 10
                move = self.basic_strategy(score, upcard, soft)
                if move == 'hit': self.game.hit()
                elif move == 'stand': self.game.stand()
                elif move == 'double': self.game.double()
                elif move == 'surrender': self.game.surrender()
        print(self.game.money)

    # Source: https://github.com/v/blackjack
    def basic_strategy(self, player_total, dealer_value, soft):
        """ This is a simple implementation of Blackjack's
            basic strategy. It is used to recommend actions
            for the player. """
        if ((player_total in [15, 16] and dealer_value in [1, 10]) or \
        (player_total == 16 and dealer_value == 9) or \
        (player_total == 17 and dealer_value == 1)) and not soft:
            return 'surrender'

        if 4 <= player_total <= 8:
            return 'hit'
        if player_total == 9:
            if dealer_value in [1,2,7,8,9,10]:
                return 'hit'
            return 'double'
        if player_total == 10:
            if dealer_value in [1, 10]:
                return 'hit'
            return 'double'
        if player_total == 11:
            if dealer_value == 1:
                return 'hit'
            return 'double'
        if soft:
            #we only double soft 12 because there's no splitting
            if player_total in [12, 13, 14]:
                if dealer_value in [5, 6]:
                    return 'double'
                return 'hit'
            if player_total in [15, 16]:
                if dealer_value in [4, 5, 6]:
                    return 'double'
                return 'hit'
            if player_total == 17:
                if dealer_value in [3, 4, 5, 6]:
                    return 'double'
                return 'hit'
            if player_total == 18:
                if dealer_value in [3, 4, 5, 6]:
                    return 'double'
                if dealer_value in [2, 7, 8]:
                    return 'stand'
                return 'hit'
            if player_total >= 19:
                return 'stand'

        else:
            if player_total == 12:
                if dealer_value in [1, 2, 3, 7, 8, 9, 10]:
                    return 'hit'
                return 'stand'
            if player_total in [13, 14, 15, 16]:
                if dealer_value in [2, 3, 4, 5, 6]:
                    return 'stand'
                return 'hit'

            if player_total >= 17:
                return 'stand'




custom = [Card(1, 1), Card(1, 2), Card(1, 3), Card(1, 4), \
Card(4, 1), Card(4, 2), Card(4, 3), Card(4, 4), \
Card(5, 1), Card(5, 2), Card(5, 3), Card(5, 4)]
player = Player(104, 6, 0, True, 100000)
player.basicStrat(10)
