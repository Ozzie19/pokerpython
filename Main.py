from Deck import Card, Deck

#deck = Deck()
#deck.shuffle()
#card = deck.deal()
#print(card)

#requires updating for asynchronous programming
# The Player class represents a player in the game.
class Player:
    # Each player has a name, a number of chips, and a current bet.
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.current_bet = 0

    # The check method represents the action of checking in poker.
    def check(self):
        pass 

    # The bet method allows a player to bet a certain amount of chips.
    def bet(self, amount):
        self.chips -= amount
        self.current_bet = amount

    # The call method allows a player to call the current bet.
    def call(self, amount):
        self.chips -= amount
        self.current_bet = amount

    # The raise_bet method allows a player to raise the current bet.
    def raise_bet(self, amount):
        self.chips -= amount
        self.current_bet += amount

    # The fold method allows a player to fold their hand.
    def fold(self):
        self.current_bet = 0

# The BettingRound class represents a round of betting in the game.
class BettingRound: 
    # Each betting round has a pot, a current bet, and a list of players.
    def __init__(self, players):
        self.pot = 0
        self.current_bet = 0
        self.players = players

    # The play_round method allows each player to take an action.
    def play_round(self):
        for player in self.players:
            # Here I will add logic to decide the player's action - to be incorporated into future module
            pass

    # The handle_check method handles a player checking.
    def handle_check(self, player):
        pass

    # The handle_bet method handles a player betting a certain amount.
    def handle_bet(self, player, amount):
        player.bet(amount)
        self.pot += amount
        self.current_bet = amount

    # The handle_call method handles a player calling the current bet.
    def handle_call(self, player):
        player.call(self.current_bet)
        self.pot += self.current_bet

    # The handle_raise method handles a player raising the current bet.
    def handle_raise(self, player, amount):
        player.raise_bet(amount)
        self.pot += player.current_bet
        self.current_bet = player.current_bet

    # The handle_fold method handles a player folding their hand.
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
    print (f'Alice has {alice.chips} chips left')

    # Bob raises to 20
    round.handle_raise(bob, 110)
    print(f'Bob raises to 20, pot is now {round.pot}')

    # Alice calls
    round.handle_call(alice)
    print(f'Alice calls, pot is now {round.pot}')
    print (f'Alice has {alice.chips} chips left')
    print (f'Bob has {bob.chips} chips left')
    
    # Bob checks
    bob.check()
    print(f'Bob checks')
    print (f'Bob has {bob.chips} chips left')

    # Alice folds
    alice.fold()
    print(f'Alice folds, current bet is {alice.current_bet}')
    print (f'Alice has {alice.chips} chips left')

    # End of betting round
    print(f'End of betting round, pot is {round.pot}')

bettingAlgorithmTests()