from Deck import Card, Deck
import random
from itertools import combinations

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

class Game:
    def __init__(self):
        self.players = []
        self.current_round = None

    def add_player(self, name, chips):
        player = Player(name, chips)
        self.players.append(player)

    def start_game(self):
        num_players = int(input("Enter the number of players: "))
        chips = int(input("Enter the initial chips for each player: "))
        for i in range(num_players):
            name = input(f"Enter the name of player {i+1}: ")
            self.add_player(name, chips)

    def deal_initial_cards(self):
        # Create a deck of cards
        deck = Deck() # assuming 1-52 represents a standard deck of cards

        # Shuffle the deck
        random.shuffle(deck)

        # Deal two cards to each player
        for player in self.players:
            player.cards = [deck.pop(), deck.pop()]


class PokerHandEvaluator:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    hand_rankings = [
        ('High Card', 0),
        ('One Pair', 1),
        ('Two Pair', 2),
        ('Three of a Kind', 3),
        ('Straight', 4),
        ('Flush', 5),
        ('Full House', 6),
        ('Four of a Kind', 7),
        ('Straight Flush', 8),
        ('Royal Flush', 9)
    ]

    @staticmethod
    def evaluate_hand(player_cards, community_cards):
        all_cards = player_cards + community_cards
        possible_hands = list(combinations(all_cards, 5))
        best_hand = max(possible_hands, key=PokerHandEvaluator.rank_hand)
        return best_hand

    @staticmethod
    def rank_hand(hand):
        # Extract values and suits from the hand
        values = sorted([PokerHandEvaluator.ranks.index(str(card.rank)) if not isinstance(card.rank, int) else card.rank for card in hand])
        suits = [card.suit for card in hand]

        # Check for flush
        is_flush = len(set(suits)) == 1

        # Check for straight
        is_straight = values == list(range(min(values), max(values) + 1))

        # Check for straight flush and royal flush
        if is_flush and is_straight:
            if values[-1] == 'A' and values[0] == 10:
                return PokerHandEvaluator.hand_rankings.index(('Royal Flush', 9))
            else:
                return PokerHandEvaluator.hand_rankings.index(('Straight Flush', 8))

        # Check for other hand rankings
        value_counts = {value: values.count(value) for value in set(values)}
        sorted_counts = sorted(value_counts.values(), reverse=True)

        if 4 in sorted_counts:
            return PokerHandEvaluator.hand_rankings.index(('Four of a Kind', 7))
        elif sorted_counts == [3, 2]:
            return PokerHandEvaluator.hand_rankings.index(('Full House', 6))
        elif is_flush:
            return PokerHandEvaluator.hand_rankings.index(('Flush', 5))
        elif is_straight:
            return PokerHandEvaluator.hand_rankings.index(('Straight', 4))
        elif 3 in sorted_counts:
            return PokerHandEvaluator.hand_rankings.index(('Three of a Kind', 3))
        elif sorted_counts == [2, 2]:
            return PokerHandEvaluator.hand_rankings.index(('Two Pair', 2))
        elif 2 in sorted_counts:
            return PokerHandEvaluator.hand_rankings.index(('One Pair', 1))
        else:
            return PokerHandEvaluator.hand_rankings.index(('High Card', 0))



def test_PokerHandEvaluator():
    evaluator = PokerHandEvaluator()

    # Test case 1: Royal Flush
    player_cards = [Card(10, 'hearts'), Card('J', 'hearts')]
    community_cards = [Card('Q', 'hearts'), Card('K', 'hearts'), Card('A', 'hearts'), Card(2, 'spades'), Card(3, 'spades')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print the Royal Flush

    # Test case 2: Four of a Kind
    player_cards = [Card(10, 'hearts'), Card(10, 'diamonds')]
    community_cards = [Card(10, 'clubs'), Card(10, 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Four of a Kind

    # Test case 3: Full House
    player_cards = [Card('A', 'hearts'), Card('A', 'diamonds')]
    community_cards = [Card(10, 'clubs'), Card('A', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Full House

    # Test case 4: Flush
    player_cards = [Card(10, 'hearts'), Card('Q', 'hearts')]
    community_cards = [Card(2, 'hearts'), Card('K', 'hearts'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Flush

    # Test case 5: Straight
    player_cards = [Card(10, 'hearts'), Card('J', 'diamonds')]
    community_cards = [Card('Q', 'clubs'), Card('K', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Straight

    # Test case 6: Three of a Kind
    player_cards = [Card(10, 'hearts'), Card(10, 'diamonds')]
    community_cards = [Card(10, 'clubs'), Card('Q', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Three of a Kind

    # Test case 7: Two Pair
    player_cards = [Card(10, 'hearts'), Card(10, 'diamonds')]
    community_cards = [Card('Q', 'clubs'), Card('Q', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print Two Pair

    # Test case 8: One Pair
    player_cards = [Card(10, 'hearts'), Card(10, 'diamonds')]
    community_cards = [Card('Q', 'clubs'), Card('K', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print One Pair

    # Test case 9: High Card
    player_cards = [Card(10, 'hearts'), Card('Q', 'diamonds')]
    community_cards = [Card('A', 'clubs'), Card('K', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    best_hand = evaluator.evaluate_hand(player_cards, community_cards)
    print("Best Hand:", best_hand)  # Should print High Card

# Run the test
test_PokerHandEvaluator()


# Run the test
test_PokerHandEvaluator()



