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
        # Print a message indicating the player's action.
        print(f'{player.name} checks.')
        # Print the current state of the pot and the player's chips.
        print(f'Pot is now {self.pot}. {player.name} has {player.chips} chips left.')

    # The handle_bet method handles a player betting a certain amount.
    def handle_bet(self, player, amount):
        # If the player can make the bet...
        if player.bet(amount):
            # Add the bet amount to the pot and set the current bet to the bet amount.
            self.pot += amount
            self.current_bet = amount
            # Print a message indicating the player's action.
            print(f'{player.name} bets {amount}.')
            # Print the current state of the pot and the player's chips.
            print(f'Pot is now {self.pot}. {player.name} has {player.chips} chips left.')
            return True
        else:
            # If the player cannot make the bet, print a message indicating the invalid action.
            print(f'{player.name} tried to bet {amount}, but the bet was invalid.')
            # Print the player's remaining chips.
            print(f'{player.name} has {player.chips} chips left.')
            return False

    # The handle_call method handles a player calling the current bet.
    def handle_call(self, player):
        # If the player can make the call...
        if player.call(self.current_bet):
            # Add the current bet to the pot.
            self.pot += self.current_bet
            # Print a message indicating the player's action.
            print(f'{player.name} calls.')
            # Print the current state of the pot and the player's chips.
            print(f'Pot is now {self.pot}. {player.name} has {player.chips} chips left.')
            return True
        else:
            # If the player cannot make the call, print a message indicating the invalid action.
            print(f'{player.name} tried to call, but the call was invalid.')
            # Print the player's remaining chips.
            print(f'{player.name} has {player.chips} chips left.')
            return False

    # The handle_raise method handles a player raising the current bet.
    def handle_raise(self, player, amount):
        # If the player can make the raise...
        if player.raise_bet(amount):
            # Add the player's current bet to the pot and set the current bet to the player's current bet.
            self.pot += player.current_bet
            self.current_bet = player.current_bet
            # Print a message indicating the player's action.
            print(f'{player.name} raises to {player.current_bet}.')
            # Print the current state of the pot and the player's chips.
            print(f'Pot is now {self.pot}. {player.name} has {player.chips} chips left.')
            return True
        else:
            # If the player cannot make the raise, print a message indicating the invalid action.
            print(f'{player.name} tried to raise to {player.current_bet + amount}, but the raise was invalid.')
            # Print the player's remaining chips.
            print(f'{player.name} has {player.chips} chips left.')
            return False

    # The handle_fold method handles a player folding.
    def handle_fold(self, player):
        # The player folds.
        player.fold()
        # Print a message indicating the player's action.
        print(f'{player.name} folds.')
        # Print the current state of the pot and the player's chips.
        print(f'Pot is now {self.pot}. {player.name} has {player.chips} chips left.')

    # The end_round method ends the current betting round.
    def end_round(self):
        # Reset the current bet to 0.
        self.current_bet = 0
        # Store the current pot in a variable.
        pot_to_distribute = self.pot
        # Reset the pot to 0.
        self.pot = 0
        # Return the pot to be distributed to the winning player(s).
        return pot_to_distribute
        round.distribute_pot(winners, pot_to_distribute)
    
    def distribute_pot(self, winners, pot_to_distribute):
        # Divide the pot evenly among the winners
        share = pot_to_distribute // len(winners)
        for player in winners:
            # Add the share to each winner's chips
            player.chips += share

def bettingAlgorithmTests():
    # Create some players
    alice = Player('Alice', 100)
    bob = Player('Bob', 100)

    # Create a betting round with those players
    round = BettingRound([alice, bob])

    # Alice tries to bet 110 chips, which is more than she has
    round.handle_bet(alice, 110)

    # Alice bets 10 chips, which is a valid bet
    round.handle_bet(alice, 10)

    # Bob tries to raise to 110, which is more than he has
    round.handle_raise(bob, 110)

    # Bob calls, which should match Alice's bet of 10 chips
    round.handle_call(bob)

    # Alice checks, which should be a valid action since the bets are even
    round.handle_check(alice)

    # Bob folds, which should end his participation in the round
    round.handle_fold(bob)

      # End the round and store the pot to distribute in a variable
    pot_to_distribute = round.end_round()
    print(f'The round has ended. The pot to distribute is {pot_to_distribute}')

    # Assume Alice is the winner and distribute the pot to her
    round.distribute_pot([alice], pot_to_distribute)

    # Print Alice's chips to verify that she received the pot
    print(f'Alice now has {alice.chips} chips')

bettingAlgorithmTests()