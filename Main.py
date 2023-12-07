from Deck import Card, Deck

#deck = Deck()
#deck.shuffle()
#card = deck.deal()
#print(card)

#requires updating for asynchronous programming
# The Player class represents a player in the game.
class Player:
    # Each player has a name and a number of chips.
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.current_bet = 0  # The current bet is initially set to 0.

    # The check method represents the action of checking in poker.
    def check(self):
        pass 

    # The bet method allows a player to bet a certain amount of chips.
    # It checks if the player has enough chips to make the bet.
    # If the player does not have enough chips, it returns False.
    def bet(self, amount):
        if self.chips >= amount:  # Check if the player has enough chips.
            self.chips -= amount  # Deduct the bet amount from the player's chips.
            self.current_bet = amount  # Set the current bet to the bet amount.
            return True  # The bet was successful.
        else:
            return False  # The bet was not successful.

    # The call method allows a player to call the current bet.
    # It checks if the player has enough chips to make the call.
    # If the player does not have enough chips, it returns False.
    def call(self, amount):
        if self.chips >= amount:  # Check if the player has enough chips.
            self.chips -= amount  # Deduct the call amount from the player's chips.
            self.current_bet = amount  # Set the current bet to the call amount.
            return True  # The call was successful.
        else:
            return False  # The call was not successful.

    # The raise_bet method allows a player to raise the current bet.
    # It checks if the player has enough chips to make the raise.
    # If the player does not have enough chips, it returns False.
    def raise_bet(self, amount):
        if self.chips >= self.current_bet + amount:  # Check if the player has enough chips.
            self.chips -= amount  # Deduct the raise amount from the player's chips.
            self.current_bet += amount  # Add the raise amount to the current bet.
            return True  # The raise was successful.
        else:
            return False  # The raise was not successful.

    # The fold method allows a player to fold their hand.
    # It sets the player's current bet to 0.
    def fold(self):
        self.current_bet = 0

# The BettingRound class represents a round of betting in a poker game.
class BettingRound: 
    # Each betting round has a pot, a current bet, and a list of players.
    def __init__(self, players):
        self.pot = 0  # The pot is initially set to 0.
        self.current_bet = 0  # The current bet is initially set to 0.
        self.players = players  # The players participating in the betting round.

    # The play_round method allows each player to take an action.
    def play_round(self):
        for player in self.players:  # For each player in the list of players...
            pass  # (This method is not yet implemented.)

    # The handle_check method handles a player checking.
    def handle_check(self, player):
        pass  # (This method is not yet implemented.)

    # The handle_bet method handles a player betting a certain amount.
    # It checks if the player has enough chips to make the bet.
    # If the player does not have enough chips, it returns False.
    def handle_bet(self, player, amount):
        if player.bet(amount):  # If the player can make the bet...
            self.pot += amount  # Add the bet amount to the pot.
            self.current_bet = amount  # Set the current bet to the bet amount.
            return True  # The bet was successful.
        else:
            return False  # The bet was not successful.

    # The handle_call method handles a player calling the current bet.
    # It checks if the player has enough chips to make the call.
    # If the player does not have enough chips, it returns False.
    def handle_call(self, player):
        if player.call(self.current_bet):  # If the player can make the call...
            self.pot += self.current_bet  # Add the current bet to the pot.
            return True  # The call was successful.
        else:
            return False  # The call was not successful.

    # The handle_raise method handles a player raising the current bet.
    # It checks if the player has enough chips to make the raise.
    # If the player does not have enough chips, it returns False.
    def handle_raise(self, player, amount):
        if player.raise_bet(amount):  # If the player can make the raise...
            self.pot += player.current_bet  # Add the player's current bet to the pot.
            self.current_bet = player.current_bet  # Set the current bet to the player's current bet.
            return True  # The raise was successful.
        else:
            return False  # The raise was not successful.
        
    # The handle_fold method handles a player folding their hand.
    def handle_fold(self, player):
        player.fold()

def bettingAlgorithmTests():    
    # Create some players
    alice = Player('Alice', 100)
    bob = Player('Bob', 100)

    # Create a betting round with those players
    round = BettingRound([alice, bob])

    # Alice tries to bet 110 chips, which is more than she has
    if not round.handle_bet(alice, 110):
        print('Alice tried to bet 110 chips, but the bet was invalid.')
    print(f'Alice has {alice.chips} chips left')

    # Alice bets 10 chips, which is a valid bet
    if round.handle_bet(alice, 10):
        print('Alice successfully bet 10 chips.')
    print(f'Alice has {alice.chips} chips left')

    # Bob tries to raise to 110, which is more than he has
    if not round.handle_raise(bob, 110):
        print('Bob tried to raise to 110, but the raise was invalid.')
    print(f'Bob has {bob.chips} chips left')

    # Bob raises to 20, which is a valid raise
    if round.handle_raise(bob, 20):
        print('Bob successfully raised to 20.')
    print(f'Bob has {bob.chips} chips left')

    # Alice calls
    round.handle_call(alice)
    print(f'Alice calls, pot is now {round.pot}')
    print(f'Alice has {alice.chips} chips left')

    # Bob checks
    bob.check()
    print('Bob checks')

bettingAlgorithmTests()