from Deck import Card, Deck
import random
from itertools import combinations
import tkinter as tk # required for GUI
from tkinter import messagebox
import os
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL module
import time

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
        #self.showdown_agreed = False  # The showdown agreed flag is initially set to False.
        self.acted_players = set()  # The set of players who have acted this round is initially empty.

        # Set active flag for all players to True initially
        for player in self.players:
            player.active = True

    def play_round(self):

        # Reset the current bet to 0 at the start of the round
        self.current_bet = 0

        # Initialize a list to keep track of players who need to act this round.
        players_to_act = [player for player in self.players if player.active]

        # Initialize a list to keep track of active players. 
        # When a player folds, they are removed from active_players and won't be considered in subsequent rounds.
        active_players = players_to_act.copy()

        # While there are active players who still haven't acted or need to react to a bet/raise...
        while len(players_to_act) > 0:
            player = players_to_act.pop(0)  # Get the first active player in the list

            # Print the current bet and the player's chips
            print(f'Pot: {self.pot}')
            print(f'Current bet: {self.current_bet}')
            print(f'{player.name} has {player.chips} chips left.')

            # Determine the player's action
            MainScreen.update_current_player(player.name) #update current player on GUI
            action = input(f'{player.name}, enter your action (check, bet, call, raise, or fold): ').lower()

            # Handle the player's action
            bet_amount = raise_amount = 0
            if action == 'bet' or action == 'raise':
                bet_amount = raise_amount = int(input(f'{player.name}, enter the amount: '))

            if action == 'check':
                self.handle_check(player)
            elif action == 'bet':
                if self.handle_bet(player, bet_amount):
                    players_to_act = active_players.copy()  # All active players need to react to the bet
                    players_to_act.remove(player)  # Except for the player who has just acted
            elif action == 'call':
                self.handle_call(player)
            elif action == 'raise':
                if self.handle_raise(player, raise_amount):
                    players_to_act = active_players.copy()  # All active players need to react to the raise
                    players_to_act.remove(player)  # Except for the player who has just acted
            elif action == 'fold':
                self.handle_fold(player)
                active_players.remove(player)  # Remove this player from active players
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
        player.active = False  # Set active flag to False for the folded player
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
        # Find the maximum hand rank
        max_rank = PokerHandEvaluator.rank_hand(max(all_hands, key=PokerHandEvaluator.rank_hand))

        # Find all hands with the maximum rank
        max_hands = [hand for hand in all_hands if PokerHandEvaluator.rank_hand(hand) == max_rank]

        # If there's only one hand with the maximum rank, it's the best hand
        if len(max_hands) == 1:
            best_hand = max_hands[0]
        else:
            # If there are multiple hands with the maximum rank, use compare_kickers to find the best hand
            best_hand = PokerHandEvaluator.find_best_hand(max_hands)

        #Winners
        winners = [player for player in self.players if (player.cards + community_cards) == best_hand]

        # Print the winners
        #for winner in winners:
            #print(f'{winner.name} is a winner!')

        if len(winners) > 1:
            # It's a tie, compare kickers
            tie_winner = max(winners, key=lambda player: PokerHandEvaluator.compare_kickers(player.cards + community_cards, best_hand))
            winners = [tie_winner]

        # Ensure the method always returns the list of winners
        return winners, pot_to_distribute
    
    
    def distribute_pot(self, winners, pot_to_distribute):
        # Divide the pot evenly among the winners
        share = pot_to_distribute // len(winners)
        for player in winners:
            # Add the share to each winner's chips
            player.chips += share
            # Print the winner's name and their new chip count
            print(f'{player.name} now has {player.chips} chips.')

class Game:
    def __init__(self):
        self.players = []  # The players in the game
        self.dealer_index = 0  # Set the dealer to be the first player initially
        self.deck = Deck()     # Initialize a new deck of cards
        self.community_cards = []  # Initialize community cards
        self.betting_round = None  # There is no betting round happening initially


    def add_player(self, name, chips):
        player = Player(name, chips)
        self.players.append(player)

    def start_game(self, num_players, starting_chips, player_names):
        for i in range(num_players):
            self.add_player(player_names[i], starting_chips)

        root = tk.Tk()
        MainScreen(root, num_players, player_names)
        root.mainloop()
        
        while True:
            # play a round
            self.play_round()

            # Ask the players if they'd like to play another round
            play_again = input('Would you like to play another round? (yes/no):')
            if play_again.lower() != 'yes':
                break

    def deal_initial_cards(self):
        deck = self.deck

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
    
    def play_round(self):
        # Determine the dealer (it rotates every round)
        dealer = self.players[self.dealer_index]
        print(f'Dealer is {dealer.name}')

        # Initialize a new deck of cards and shuffle it
        self.deck = Deck()
        self.deck.shuffle()

        # Deal two hidden cards to each player
        for player in self.players:
            player.cards = [self.deck.deal() for _ in range(2)]
            print(f'{player.name} has been dealt their cards: {player.cards}')
            # TODO: Remove this print statement when a GUI is added

        # Initialize a single instance of BettingRound for the entire hand
        self.betting_round = BettingRound(self.players)

        # The pre-flop betting round. Afterward, a round of betting takes place.
        self.betting_round.play_round()

        # The flop is dealt. Then, display the community cards to the players.
        self.community_cards = [self.deck.deal() for _ in range(3)]
        print('The flop: ', self.community_cards)

        # Another round of betting takes place.
        self.betting_round.play_round()

        # The turn card is dealt. Show the community cards to the players.
        self.community_cards.append(self.deck.deal()) 
        print('The board after the turn: ', self.community_cards)

        # Another round of betting takes place.
        self.betting_round.play_round()

        # The river card is dealt. Show the community cards to the players.
        self.community_cards.append(self.deck.deal()) 
        print('The board after the river: ', self.community_cards)

        # The final round of betting takes place.
        self.betting_round.play_round()

        # The end-round method is then used to end the round of poker
        winners, pot_to_distribute = self.betting_round.end_round(self.community_cards)
        
        # Distribute pot to the determined winner
        self.betting_round.distribute_pot(winners, pot_to_distribute)

        # Move the dealer button to the next player
        self.dealer_index = (self.dealer_index + 1) % len(self.players)



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

    def find_best_hand(hands):
        best_hand = hands[0]
        for hand in hands[1:]:
            if PokerHandEvaluator.compare_kickers(best_hand, hand) < 0:
                best_hand = hand
        return best_hand


class GameSetupScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game Setup")

        # Set the background color
        self.root.configure(bg="#108F33")

        # Make the window fullscreen
        self.root.attributes("-fullscreen", True)

        # Frame for "Number of Players" label and entry on the left
        self.num_players_frame = tk.Frame(root, bg="#D9D9D9", width=341, height=59)
        self.num_players_frame.place(x=50, y=100)

        # Label for "Number of Players"
        self.num_players_label = tk.Label(self.num_players_frame, text="Number of Players:", bg="#D9D9D9", font=("Arial", 16))
        self.num_players_label.pack(padx=10, pady=10, side=tk.LEFT)

        # Entry for "Number of Players"
        self.num_players_entry = tk.Entry(self.num_players_frame, font=("Arial", 16), bg="#D9D9D9", width=20)
        self.num_players_entry.pack(padx=10, pady=10, side=tk.RIGHT)

        # Frame for "Starting Chips" label and entry on the left
        self.starting_chips_frame = tk.Frame(root, bg="#D9D9D9", width=341, height=59)
        self.starting_chips_frame.place(x=50, y=200)

        # Label for "Starting Chips"
        self.starting_chips_label = tk.Label(self.starting_chips_frame, text="Starting Chips:", bg="#D9D9D9", font=("Arial", 16))
        self.starting_chips_label.pack(padx=10, pady=10, side=tk.LEFT)

        # Entry for "Starting Chips"
        self.starting_chips_entry = tk.Entry(self.starting_chips_frame, font=("Arial", 16), bg="#D9D9D9", width=20)
        self.starting_chips_entry.pack(padx=10, pady=10, side=tk.RIGHT)

        # Button to start the game on the left
        self.start_game_button = tk.Button(root, text="Start Game", command=self.start_game, bg="#FFD700", fg="#108F33", font=("Arial", 16))
        self.start_game_button.place(x=50, y=300)

        # Frame for "Enter Player Names" label and entries on the right
        self.players_info_frame = tk.Frame(root, bg="#D9D9D9", width=341, height=59)
        self.players_info_frame.place(x=1063, y=100)

        # Label for "Enter Player Names"
        self.players_info_label = tk.Label(self.players_info_frame, text="Enter Player Names:", bg="#D9D9D9", font=("Arial", 16))
        self.players_info_label.pack(padx=10, pady=10, side=tk.LEFT)

        # Labels and entries for entering player names on the right
        self.player_name_entries = []
        for i in range(1, 11):  # Assuming a maximum of 10 players
            player_frame = tk.Frame(root, bg="#D9D9D9", width=341, height=59)
            player_frame.place(x=1063, y=100 + 80*i)
            
            player_label = tk.Label(player_frame, text=f"Player {i}:", bg="#D9D9D9", font=("Arial", 16))
            player_label.pack(padx=10, pady=10, side=tk.LEFT)
            
            player_entry = tk.Entry(player_frame, font=("Arial", 16), bg="#D9D9D9", width=20)
            player_entry.pack(padx=10, pady=10, side=tk.RIGHT)
            
            self.player_name_entries.append(player_entry)

    def start_game(self):
        num_players_str = self.num_players_entry.get()
        if not num_players_str.isdigit():
            messagebox.showerror("Error", "Number of players must be a positive integer.")
            return
        num_players = int(num_players_str)
        if num_players < 2 or num_players > 10:
            messagebox.showerror("Error", "Number of players must be between 2 and 10.")
            return
        
        player_names = []
        for entry in self.player_name_entries[:num_players]:
            name = entry.get().strip()
            if name:
                player_names.append(name)

        if len(player_names) != num_players:
            messagebox.showerror("Error", "Number of non-empty player names does not match the specified number of players.")
            return
        
        starting_chips_str = self.starting_chips_entry.get()
        if not starting_chips_str.isdigit():
            messagebox.showerror("Error", "Starting chips must be a positive integer.")
            return

        starting_chips = int(starting_chips_str)
        if starting_chips < 1:
            messagebox.showerror("Error", "Starting chips must be a positive integer.")
            return

        self.root.destroy()
        game = Game()
        game.start_game(num_players, starting_chips, player_names)


class MainScreen:
    def __init__(self, root, num_players, player_names):
        self.root = root
        self.root.title("Poker Game")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#108F33")  # Set background color to the green from the setup screen

        # Load card images
        self.load_card_images()

        # Create a canvas for the card holder box
        self.card_holder_canvas = tk.Canvas(root, bg="#108F33", bd=2, highlightthickness=0)
        self.card_holder_canvas.place(relx=1, rely=0, anchor="ne", width=940, height=240)  # Adjust dimensions
        self.card_holder_canvas.create_rectangle(10, 30, 920, 230, outline="#D9D9D9")  # Adjust dimensions and padding

        # Create the label for displaying pot
        self.pot_label = tk.Label(root, text="Pot:", font=("Arial", 18), bg="#D9D9D9")
        self.pot_label.place(relx=0, rely=1, anchor="sw", x=980, y=-800)  # Adjust position

        # Initialize pot value
        self.pot_value = 0
        self.update_pot(self.pot_value)

        # Create a big box at the bottom right half of the screen for player actions
        self.action_box = tk.Canvas(root, bg="#A0DDFF")
        self.action_box.place(relx=1, rely=1, anchor="se", width=root.winfo_screenwidth() / 2, height=root.winfo_screenheight() / 2)

        # Create a small box with the current player's name at the top left of the big box
        self.current_player_box = tk.Canvas(root, bg="#D9D9D9")
        self.current_player_box.place(relx=1, rely=1, anchor="se", width=root.winfo_screenwidth() / 2, height=50, x=0, y=-root.winfo_screenheight() / 2)

        # Create a label to display the current player's name
        self.current_player_name = "Player 1"  # You can change this dynamically based on the current player
        self.player_name_label = tk.Label(root, text=self.current_player_name, font=("Arial", 12), bg="#D9D9D9")
        self.player_name_label.place(relx=1, rely=1, anchor="se", width=root.winfo_screenwidth() / 2, height=50, x=0, y=-root.winfo_screenheight() / 2)

        # Create a dropdown menu for player actions
        self.action_options = ["Check", "Bet", "Call", "Raise", "Fold"]
        self.selected_action = tk.StringVar(root)
        self.selected_action.set(self.action_options[0])  # Default action is Check
        self.action_menu = tk.OptionMenu(root, self.selected_action, *self.action_options)
        self.action_menu.config(width=10, font=("Arial", 12))
        self.action_menu.place(relx=1, rely=1, anchor="se", width=root.winfo_screenwidth() / 2, height=50)

        # Bind the action_menu to update the selected action
        self.selected_action.trace("w", self.update_selected_action)

        # Create a canvas for displaying player hands, chips, and current bet
        self.players_canvas = tk.Canvas(root, bg="#D9D9D9")
        self.players_canvas.place(relx=0, rely=0, anchor="nw", width=root.winfo_screenwidth() / 2, height=root.winfo_screenheight())

        # Calculate the height of each player's box
        player_box_height = root.winfo_screenheight() / num_players

        # Create boxes for each player
        for i in range(num_players):
            player_box = tk.Frame(root, bg="#FFFFFF", highlightbackground="#000000", highlightthickness=1)
            player_box.place(relx=0, rely=i / num_players, relwidth=0.5, relheight=1 / num_players)

            # Example: Add labels for chip balance, current bet (stake), and card images for each player
            chip_balance_label = tk.Label(player_box, text="Chips: 1000", font=("Arial", 10), bg="#FFFFFF")
            chip_balance_label.pack(side="left")

            stake_label = tk.Label(player_box, text="Stake: 50", font=("Arial", 10), bg="#FFFFFF")
            stake_label.pack()

            player_name_label = tk.Label(player_box, text=f"Player Name: {player_names[i]}", font=("Arial", 10), bg="#FFFFFF")
            player_name_label.pack(side="right")

            # Add images of cards
            card_image1 = tk.Label(player_box, image=self.card_images['default'], bg="#FFFFFF")
            card_image1.pack(side="left")
            card_image2 = tk.Label(player_box, image=self.card_images['default'], bg="#FFFFFF")
            card_image2.pack(side="left")
    
    def update_current_player(self, new_player_name):
        self.current_player_name = new_player_name
        self.player_name_label.config(text=f"Player Name: {self.current_player_name}")

    def update_selected_action(self, *args):
        # This method will be called whenever the selected action is changed
        print("Selected action:", self.selected_action.get())  

    def update_pot(self, pot_value):
        self.pot_value = pot_value
        # Update the label text with the new pot value
        self.pot_label.config(text=f"Pot: {self.pot_value}")

    def update_selected_action(self, *args):
        # This method will be called whenever the selected action is changed
        print("Selected action:", self.selected_action.get())  # For testing, you can replace print with any other action

    def load_card_images(self):
        # Dictionary to store the paths to card images
        self.card_images = {}

        # Directory containing the card images
        cards_directory = r'pokerpython\cards'

        # List files in the directory
        files = os.listdir(cards_directory)

        # Loop through the files
        for file_name in files:
            # Extract card name from file name
            if file_name.endswith('.png'):
                card_name = os.path.splitext(file_name)[0].lower()

                # Convert card name
                card_name = self.convert_card_name(card_name)

                # Open the image file using PIL
                image = Image.open(os.path.join(cards_directory, file_name))
                
                # Resize the image to a smaller size
                resized_image = image.resize((50, 100), Image.LANCZOS)
                
                # Convert the resized image to PhotoImage
                photo_image = ImageTk.PhotoImage(resized_image)

                # Add the card image to the dictionary
                self.card_images[card_name] = photo_image

    def convert_card_name(self, card_name):
        # Dictionary mapping long names to their corresponding short names
        name_mapping = {
            "ace": "A",
            "king": "K",
            "queen": "Q",
            "jack": "J",
            "ten": "10",
            "nine": "9",
            "eight": "8",
            "seven": "7",
            "six": "6",
            "five": "5",
            "four": "4",
            "three": "3",
            "two": "2"
        }

        # Split the card name into individual words
        words = card_name.split(" ")

        # Convert each word to the desired format
        converted_words = [name_mapping[word] if word in name_mapping else word.lower() for word in words]

        # Join the converted words back into a single string
        converted_card_name = " ".join(converted_words)


        return converted_card_name

    #def display_card_images(self):
        # Display card images along with their names
        #row = 0
        #for converted_card_name, image in self.card_images.items():
            #label = tk.Label(self.root, text=converted_card_name, image=image, compound=tk.TOP)
            #label.grid(row=row // 10, column=row % 10, padx=0, pady=0)
            #row += 1
    
# Define a new class called ResultsScreen, which inherits from tk.Toplevel
class ResultsScreen(tk.Toplevel):
    # The __init__ method is called when an instance of the class is created
    def __init__(self, winners):
        # Call the __init__ method of the parent class (tk.Toplevel)
        super().__init__()
        # Store the list of winners
        self.winners = winners
        # Set the title of the window
        self.title("Results")
        # Set the size of the window
        self.geometry("300x200")
        # Call the display_results method to display the results
        self.display_results()

    # Define a method to display the results
    def display_results(self):
        # Create a label with the text "Winners:"
        result_label = tk.Label(self, text="Winners:")
        # Add the label to the window
        result_label.pack()

        # Loop over the list of winners
        for winner in self.winners:
            # For each winner, create a label with their name and remaining chips
            winner_label = tk.Label(self, text=f"{winner.name} wins with a new balance of {winner.chips} chips remaining.", wraplength=200)
            # Add the label to the window
            winner_label.pack()

        # Ask the user if they want to play again
        play_again = messagebox.askyesno("Play Again", "Would you like to play another round?")
        # If the user wants to play again
        if play_again:
            # Create a new root window
            root = tk.Tk()
            # Create a new game setup screen in the root window
            game_setup_screen = GameSetupScreen(root)
            # Start the main event loop
            root.mainloop()
            # Destroy the results screen
            self.destroy()
def main():
    player1 = Player("Player 1", 1000)
    player2 = Player("Player 2", 100)
    results_screen = ResultsScreen([player2])

#used to test main screen
#def main():
    #root = tk.Tk()
    #player_names = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8", "Player 9", "Player 10"]
    #main_screen = MainScreen(root, 10, player_names)
    #root.mainloop()


 #used to test setup screen
#def main():
    #root = tk.Tk()
    #game_setup_screen = GameSetupScreen(root)
    #root.mainloop()
    
if __name__ == "__main__":
    main()