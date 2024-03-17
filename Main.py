from Deck import Card, Deck
import random
from itertools import combinations
import unittest

#deck = Deck()
#deck.shuffle()
#card = deck.deal()
#print(card)

#requires updating for asynchronous programming
# The Player class represents a player in the game.ch
class Player:
    # Each player has a name and a number of chips.
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.current_bet = 0  # The current bet is initially set to 0.
        #self.sBlind = sBlind
        #self.bBlind = bBlind

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
        self.showdown_agreed = False  # The showdown agreed flag is initially set to False.
        self.acted_players = set()  # The set of players who have acted this round is initially empty.

    # The play_round method allows each player to take an action.
    def play_round(self):
        # Initialize a list to keep track of players who need to act this round.
        players_to_act = self.players.copy()

        # While there are players who still haven't acted or need to react to a bet/raise...
        while len(players_to_act) > 0:
            player = players_to_act.pop(0)  # Get the first player in the list

            # Print the current bet and the player's chips
            print(f'Pot: {self.pot}')
            print(f'Current bet: {self.current_bet}')
            print(f'{player.name} has {player.chips} chips left.')

            # Determine the player's action
            action = input(f'{player.name}, enter your action (check, bet, call, raise, or fold): ').lower()

            # Handle the player's action
            bet_amount = raise_amount = 0
            if action == 'bet' or action == 'raise':
                bet_amount = raise_amount = int(input(f'{player.name}, enter the amount: '))

            if action == 'check':
                self.handle_check(player)
            elif action == 'bet':
                if self.handle_bet(player, bet_amount):
                    players_to_act = self.players.copy()  # All players need to react to the bet
                    players_to_act.remove(player)  # Except for the player who has just acted
            elif action == 'call':
                self.handle_call(player)
            elif action == 'raise':
                if self.handle_raise(player, raise_amount):
                    players_to_act = self.players.copy()  # All players need to react to the raise
                    players_to_act.remove(player)  # Except for the player who has just acted
            elif action == 'fold':
                self.handle_fold(player)
            else:
                print(f'Invalid action: {action}')
                players_to_act.insert(0, player)  # Give player another chance for a valid action.

        print('End of betting round.')

   # The handle_check method handles a player checking.
    def handle_check(self, player):
        if self.current_bet == 0:  # Check if there are no other bets on the table
            print(f'{player.name} checks.')
        else:
            print(f'{player.name} cannot check because there is a bet on the table.')
            return False
        return True

    # The handle_bet method handles a player betting a certain amount.
    def handle_bet(self, player, amount):
        if self.current_bet == 0:  # Check if there are no other bets on the table
            if amount <= player.chips:  # Check if the player has enough chips.
                player.bet(amount)
                self.pot += amount
                self.current_bet = amount
                print(f'{player.name} bets {amount}.')
            else:
                print(f'{player.name} does not have enough chips to bet.')
                return False
        else:
            print(f'{player.name} cannot bet because there is already a bet on the table.')
            return False
        return True

    # The handle_call method handles a player calling the current bet.
    def handle_call(self, player):
        if player.chips >= self.current_bet:  # Check if the player has enough chips to call
            player.call(self.current_bet)
            self.pot += self.current_bet
            print(f'{player.name} calls.')
        else:
            print(f'{player.name} does not have enough chips to call. {player.name} folds')
            self.handle_fold(player)
        return True

    # The handle_raise method handles a player raising the current bet.
    def handle_raise(self, player, amount):
        if player.chips >= (self.current_bet + amount):
            player.current_bet = self.current_bet
            player.raise_bet(amount)
            self.pot += player.current_bet
            self.current_bet = player.current_bet
            print(f'{player.name} raises to {player.current_bet}.')
        else:
            print(f'{player.name} does not have enough chips to raise. {player.name} folds')
            self.handle_fold(player)
        return True

    # The handle_fold method handles a player folding.
    def handle_fold(self, player):
        player.fold()
        print(f'{player.name} folds.')


    # The end_round method ends the current betting round.
    def end_round(self, community_cards):
        # Reset the current bet to 0.
        self.current_bet = 0
        # Store the current pot in a variable.
        pot_to_distribute = self.pot
        # Reset the pot to 0.
        self.pot = 0

        # Collect all player hands, including community cards
        all_hands = [player.cards + community_cards for player in self.players]

        # Find the best hand using the rank_hand method as the key for max
        best_hand = max(all_hands, key=PokerHandEvaluator.rank_hand)

        # Check for tie and compare kickers if needed
        winners = [player for player in self.players if PokerHandEvaluator.rank_hand(player.cards + community_cards) == PokerHandEvaluator.rank_hand(best_hand)]

        if len(winners) > 1:
            # It's a tie, compare kickers
            tie_winner = max(winners, key=lambda player: PokerHandEvaluator.compare_kickers(player.cards + community_cards, best_hand))
            winners = [tie_winner]

        # Ensure the method always returns the list of winners
        return winners
    
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

    
    def deal_flop(self, deck):
        # Burn one card
        deck.pop()

        # Deal three cards for the flop
        flop = [deck.pop() for _ in range(3)]

        return flop

    def deal_turn(self, deck):
        # Burn one card
        deck.pop()

        # Deal one card for the turn
        turn = deck.pop()

        return turn

    def deal_river(self, deck):
        # Burn one card
        deck.pop()

        # Deal one card for the river
        river = deck.pop()

        return river
    
    def play_round(self, dealer_index):
        # Start with the player to the left of the dealer and go clockwise
        current_player_index = (dealer_index + 1) % len(self.players)

        # Deal initial cards
        deck = Deck()
        random.shuffle(deck)
        for player in self.players:
            player.cards = [deck.pop(), deck.pop()]

        # Deal the flop
        flop = self.deal_flop(deck)
        print("Flop:", flop)
        self.community_cards.extend(flop)

        # Allow each player to take actions
        while True:
            player = self.players[current_player_index]
            print("\n{}'s Turn:".format(player.name))

            # Let the player take an action (check, bet, fold, etc.)
            # For simplicity, let's assume players always choose to check in this implementation
            self.handle_check(player)

            # Move to the next player
            current_player_index = (current_player_index + 1) % len(self.players)

            # If all players have checked, move to the next round or end the round
            if current_player_index == dealer_index:
                print("End of pre-flop betting round.")
                break

        # End of pre-flop betting round
        print("End of pre-flop betting round.")


class PokerHandEvaluator:
    # Define possible card ranks and hand rankings
    ranks = [None, None] + [str(n) for n in range(2, 11)] + list('JQKA')
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
        # Combine player's and community's cards
        all_cards = player_cards + community_cards
        # Generate all possible combinations of 5 cards
        possible_hands = list(combinations(all_cards, 5))
        # Find the best hand using the rank_hand method as the key for max
        best_hand = max(possible_hands, key=PokerHandEvaluator.rank_hand)
        return PokerHandEvaluator.rank_hand(best_hand)

    @staticmethod
    def rank_hand(hand):
        # Extract values and suits from the hand
        values = sorted([PokerHandEvaluator.ranks.index(str(card.rank)) if not isinstance(card.rank, int) else card.rank for card in hand])
        suits = [card.suit for card in hand]
        # Check for flush (all cards have the same suit)
        is_flush = len(set(suits)) == 1

        # Check if the ranks form a sequence (straight)
        is_straight = values == list(range(min(values), max(values) + 1))

        # Check for Ace-low straight (wheel)
        is_wheel = values == [2, 3, 4, 5, 14]

        # Check for 5 high straight
        is_five_high_straight = values == [14, 2, 3, 4, 5]

        # Update is_straight to include the wheel case
        is_straight = is_straight or is_wheel or is_five_high_straight

        # Check for straight flush and royal flush
        if is_flush and is_straight:
            if values[-1] == 14 and values[0] == 10:
                # Royal Flush
                return PokerHandEvaluator.hand_rankings.index(('Royal Flush', 9))
            else:
                # Straight Flush
                return PokerHandEvaluator.hand_rankings.index(('Straight Flush', 8))

        # Check for other hand rankings
        value_counts = {value: values.count(value) for value in set(values)}
        sorted_counts = sorted(value_counts.values(), reverse=True)

        if 4 in sorted_counts:
            # Four of a Kind
            return PokerHandEvaluator.hand_rankings.index(('Four of a Kind', 7))
        elif sorted_counts == [3, 2]:
            # Full House
            return PokerHandEvaluator.hand_rankings.index(('Full House', 6))
        elif is_flush:
            # Flush
            return PokerHandEvaluator.hand_rankings.index(('Flush', 5))
        elif is_straight:
            # Straight
            return PokerHandEvaluator.hand_rankings.index(('Straight', 4))
        elif 3 in sorted_counts:
            # Three of a Kind
            return PokerHandEvaluator.hand_rankings.index(('Three of a Kind', 3))
        elif sorted_counts == [2, 2, 1]:
            # Two Pair
            return PokerHandEvaluator.hand_rankings.index(('Two Pair', 2))
        elif 2 in sorted_counts:
            # One Pair
            return PokerHandEvaluator.hand_rankings.index(('One Pair', 1))
        else:
            # High Card
            return PokerHandEvaluator.hand_rankings.index(('High Card', 0))

    @staticmethod
    def compare_kickers(hand1, hand2):
        """
        Compare kickers of two hands to determine the winner in case of a tie.

        Args:
            hand1 (List[Card]): First hand to compare.
            hand2 (List[Card]): Second hand to compare.

        Returns:
            int: 1 if hand1 wins, -1 if hand2 wins, 0 if it's a tie.
        """
        values1 = sorted([PokerHandEvaluator.ranks.index(str(card.rank)) if not isinstance(card.rank, int) else card.rank for card in hand1])
        values2 = sorted([PokerHandEvaluator.ranks.index(str(card.rank)) if not isinstance(card.rank, int) else card.rank for card in hand2])

        # Compare kickers starting from the highest
        for kicker1, kicker2 in zip(reversed(values1), reversed(values2)):
            if kicker1 > kicker2:
                return 1
            elif kicker1 < kicker2:
                return -1

        return 0


if __name__ == '__main__':
    players = [Player('Alice', 100), Player('Bob', 100), Player('Charlie', 100)]
    betting_round = BettingRound(players)
    betting_round.play_round()