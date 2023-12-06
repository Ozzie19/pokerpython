from Deck import Card, Deck

#deck = Deck()
#deck.shuffle()
#card = deck.deal()
#print(card)

#requires updating for asynchronous programming
class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.current_bet = 0

    def check(self):
        pass #improve - use a check boolean to check if the player has "check"ed for the game management algorithm

    def bet(self, amount):
        self.chips -= amount
        self.current_bet = amount

    def call(self, amount):
        self.chips -= amount
        self.current_bet = amount

    def raise_bet(self, amount):
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.current_bet = 0

class BettingRound: #needs method to end betting round 
        def __init__(self, players):
            self.pot = 0
            self.current_bet = 0
            self.players = players

        def play_round(self):
            for player in self.players:
                # Here I will add logic to decide the player's action - to be incorporated into future module
                pass

        def handle_check(self, player):
            pass

        def handle_bet(self, player, amount):
            player.bet(amount)
            self.pot += amount
            self.current_bet = amount

        def handle_call(self, player):
            player.call(self.current_bet)
            self.pot += self.current_bet

        def handle_raise(self, player, amount):
            player.raise_bet(amount)
            self.pot += player.current_bet
            self.current_bet = player.current_bet

        def handle_fold(self, player):
            player.fold()

def bettingAlgorithmTests():    
    # Create some players
    alice = Player('Alice', 100)
    bob = Player('Bob', 100)

    # Create a betting round with those players
    round = BettingRound([alice, bob])

    # Alice bets 10 chips
    round.handle_bet(alice, 10)
    print(f'Alice bets 10, pot is now {round.pot}')

    # Bob raises to 20
    round.handle_raise(bob, 10)
    print(f'Bob raises to 20, pot is now {round.pot}')

    # Alice calls
    round.handle_call(alice)
    print(f'Alice calls, pot is now {round.pot}')

    # Bob checks
    bob.check()
    print(f'Bob checks')

    # Alice folds
    alice.fold()
    print(f'Alice folds, current bet is {alice.current_bet}')

    # End of betting round
    print(f'End of betting round, pot is {round.pot}')