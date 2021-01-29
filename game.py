from deck import Deck

class BlackJack:
    def __init__(self, cutoff, decks, starting_cash, hitsoft17, takes_input, custom_deck=None):
        self.deck = Deck(decks, custom_deck)
        self.hidden_card = None
        self.dealer_cards = []
        self.player_cards = []
        self.cut = cutoff
        self.bet = None
        self.money = starting_cash
        self.soft17 = hitsoft17
        self.active = False
        self.responsive = takes_input
        self.insurance = False

    def newHand(self, bet_size):
        self.active = True
        self.bet = bet_size
        if len(self.deck.deck) < self.cut:
            self.deck.shuffle()
            if self.responsive: print("Deck shuffled")
        self.hidden_card = self.deck.draw()
        self.dealer_cards = [self.deck.draw()]
        self.player_cards = [self.deck.draw(), self.deck.draw()]
        if self.responsive: self.showTable(False)
        self.insurance = False
        if self.responsive and self.dealer_cards[0].rank == 1:
            ans = input("Buy insurance? ").lower()
            if ans == "y" or ans == "yes":
                self.buyInsurance()
        if self.dealerBJ() and self.playerBJ():
            if self.insurance: self.winInsurance()
            self.gameOver("push")
        elif self.dealerBJ():
            if self.insurance: self.winInsurance()
            self.gameOver("dealer", "L", 21)
        elif self.playerBJ():
            if self.insurance: self.loseInsurance()
            self.gameOver("blackjack", 21, "L")
        if self.insurance: self.loseInsurance()
        if self.responsive:
            self.askMove()

    def askMove(self):
        moved = False
        while self.active:
            move = input("What's your move? ").lower()
            if move == "hit" or move == "h":
                self.hit()
            elif move == "stand" or move == "stay" or move == "s":
                self.stand()
            elif move == "double" or move == "d" or move == "double down":
                if moved:
                    print("You can't double down after making a move")
                    continue
                else:
                    self.double()
            elif move == "surrender":
                if moved:
                    print("You can't surrender after making a move")
                    continue
                else:
                    self.surrender()
            elif move == "split":
                if moved or self.player_cards[0].rank != self.player_cards[1].rank:
                    print("Can't split that buddy")
                    continue
                else:
                    self.split()
            else:
                print("That's not a valid move!")
                continue
            moved = True
            self.showTable(False)

    def hit(self):
        self.player_cards.append(self.deck.draw())
        pscore, soft = self.playerScore()
        if pscore > 21:
            dscore0, ace0 = self.dealerCardScore(self.hidden_card)
            dscore1, ace1 = self.dealerCardScore(self.dealer_cards[0])
            if dscore0 + dscore1 == 22: dscore1 = 1
            if self.responsive: self.showTable(True)
            self.gameOver("dealer", pscore, dscore0 + dscore1)
        else:
            # For chekcing if player score is under 21 when doubling
            return True

    def stand(self):
        dealer_score = self.dealerScore()
        player_score, soft = self.playerScore()
        if self.responsive: self.showTable(True)
        if player_score > dealer_score or dealer_score > 21:
            self.gameOver("player", player_score, dealer_score)
        elif dealer_score > player_score:
            self.gameOver("dealer", player_score, dealer_score)
        else:
            self.gameOver("push", player_score, dealer_score)

    def double(self):
        self.bet *= 2
        if self.responsive: print("New bet: ", self.bet)
        if self.hit(): self.stand()

    def surrender(self):
        self.bet /= 2
        if self.responsive: self.showTable(True)
        self.gameOver("dealer")

    # Aces can only be hit once after split. One split allowed. No doubling split
    def split(self):
        secCard = self.player_cards.pop(-1)
        if self.player_cards[0].rank == 1:
            self.player_cards.append(self.deck.draw())
            score1, soft = self.playerScore()
            temp = self.player_cards.pop(-1)
            self.player_cards.append(self.deck.draw())
            score2, soft = self.playerScore()
            self.player_cards += [secCard, temp]
        if self.responsive:
            if self.player_cards[0].rank == 1:
                self.splitStand(False, score1, score2)
            else:
                score1 = self.splitAct("first")
                self.splitStand(True)
                self.player_cards = [secCard]
                score2 = self.splitAct("second")
                self.splitStand(False, score1, score2)

    def splitAct(self, time):
        while self.playerScore()[0] <= 21:
            move = input("Hit " + time + " hand? ").lower()
            if move == "yes" or move == "y":
                self.splitHit()
            else: break
            self.showTable(False)
        return self.playerScore()[0]

    def splitScoreCalc(self, time, pscore, dscore):
        if pscore > 21:
            self.money -= self.bet
            if self.responsive: print(time + " hand bust")
        elif dscore > 21 or pscore > dscore:
            self.money += self.bet
            if self.responsive: print(time + " hand won")
        elif dscore > pscore:
            self.money -= self.bet
            if self.responsive: print(time + " hand lost")
        else:
            if self.responsive: print(time + " hand push")

    def splitHit(self):
        self.player_cards.append(self.deck.draw())

    def splitStand(self, first, score1=0, score2=0):
        if not first:
            dealer_score = self.dealerScore()
            self.splitScoreCalc("First", score1, dealer_score)
            self.splitScoreCalc("Second", score2, dealer_score)
            if self.responsive: self.showTable(True)
            self.gameOver("N/A", str(score1) + " " + str(score2), dealer_score)

    def buyInsurance(self):
        self.insurance = True

    def winInsurance(self):
        self.money += self.bet
        if self.responsive: print("You won the insurance bet!")

    def loseInsurance(self):
        self.money -= (self.bet / 2)
        if self.responsive: print("You lost the insurance bet")

    def dealerCardScore(self, card):
        if 2 <= card.rank <= 10: return card.rank, 0
        elif card.rank > 10: return 10, 0
        else: return 11, 1

    def dealerScore(self):
        dealer_score, aces = self.dealerCardScore(self.hidden_card)
        dscore1, ace1 = self.dealerCardScore(self.dealer_cards[0])
        dealer_score += dscore1
        aces += ace1
        while dealer_score < 17:
            self.dealer_cards.append(self.deck.draw())
            score, ace = self.dealerCardScore(self.dealer_cards[-1])
            dealer_score += score
            aces += ace
            if dealer_score > 21 and aces > 0:
                dealer_score -= 10
                aces -= 1
            if dealer_score == 17 and (not self.soft17 or aces == 0): break
        while dealer_score > 21 and aces > 0:
            dealer_score -= 10
            aces -= 1
        return dealer_score

    def playerScore(self):
        score = 0
        ace_count = 0
        for card in self.player_cards:
            if 2 <= card.rank <= 10: score += card.rank
            elif card.rank > 10: score += 10
            else:
                ace_count += 1
                score += 11
        while ace_count > 0 and score > 21:
            score -= 10
            ace_count -= 1
        return score, ace_count > 0

    def dealerBJ(self):
        return (self.hidden_card.rank == 1 and self.dealer_cards[0].rank >= 10) \
        or (self.hidden_card.rank >= 10 and self.dealer_cards[0].rank == 1)

    def playerBJ(self):
        return (self.player_cards[0].rank == 1 and self.player_cards[1].rank >= 10) \
        or (self.player_cards[0].rank >= 10 and self.player_cards[1].rank == 1)

    def gameOver(self, res, pscore="N/A", dscore="N/A"):
        self.active = False
        if res == "dealer":
            self.money -= self.bet
            if self.responsive: print("You lose")
        elif res == "player":
            self.money += self.bet
            if self.responsive: print("You won. Nice one bud")
        elif res == "blackjack":
            self.money += 1.5 * self.bet
            if self.responsive: print("BlackJack. You lucky dog!")
        elif res == "push":
            if self.responsive: print("Push")
        if self.responsive:
            print("Player score: ", pscore, "Dealer score: ", dscore)
            print("Bet size: ", self.bet, "Player money: ", self.money)
            again = input("Play again? ").lower()
            if again == "yes" or again == "yeah" or again == "y":
                bet = input("How much do you want to bet? ")
                self.newHand(int(bet))
            else:
                print("See ya later alligator!")
                print("Money: ", self.money)

    def translateRank(self, card):
        if 2 <= card.rank <= 10:
            return card.rank
        elif card.rank == 1:
            return "A"
        elif card.rank == 11:
            return "J"
        elif card.rank == 12:
            return "Q"
        else:
            return "K"

    def translateSuit(self, card):
        if card.suit == 1: return "spades"
        if card.suit == 2: return "clubs"
        if card.suit == 3: return "hearts"
        if card.suit == 4: return "diamonds"

    def showTable(self, show_hidden):
        if self.active:
            print(" ")
            if show_hidden:
                print("Hidden card")
                print("Rank: ", self.translateRank(self.hidden_card), \
                "Suit: ", self.translateSuit(self.hidden_card))
                print("Dealer cards")
            else:
                print("Dealer card")
            for card in self.dealer_cards:
                print("Rank: ", self.translateRank(card), \
                "Suit: ", self.translateSuit(card))
            print("Player cards")
            for card in self.player_cards:
                print("Rank: ", self.translateRank(card), \
                "Suit: ", self.translateSuit(card))
