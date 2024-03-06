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


def test_PokerHandEvaluator():
    evaluator = PokerHandEvaluator()

    # Test case 1: Royal Flush
    player_cards = [Card(10, 'hearts'), Card('J', 'hearts')]
    community_cards = [Card('Q', 'hearts'), Card('K', 'hearts'), Card('A', 'hearts'), Card(2, 'spades'), Card(3, 'spades')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 9

    # Test case 2: High Card
    player_cards = [Card(2, 'hearts'), Card(3, 'diamonds')]
    community_cards = [Card(5, 'clubs'), Card(7, 'spades'), Card(8, 'hearts'), Card(10, 'clubs'), Card('K', 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 0

    # Test case 3: One Pair
    player_cards = [Card(2, 'hearts'), Card(2, 'diamonds')]
    community_cards = [Card(5, 'clubs'), Card(7, 'spades'), Card(8, 'hearts'), Card(10, 'clubs'), Card('K', 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 1

    # Test case 4: Two Pair
    player_cards = [Card(2, 'hearts'), Card(2, 'diamonds')]
    community_cards = [Card(5, 'clubs'), Card(5, 'spades'), Card(8, 'hearts'), Card(10, 'clubs'), Card('K', 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 2

    # Test case 5: Three of a Kind
    player_cards = [Card(2, 'hearts'), Card(2, 'diamonds')]
    community_cards = [Card(2, 'clubs'), Card(7, 'spades'), Card(8, 'hearts'), Card(10, 'clubs'), Card('K', 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 3

    # Test case 6: Straight
    player_cards = [Card(10, 'hearts'), Card('J', 'diamonds')]
    community_cards = [Card('Q', 'clubs'), Card('K', 'spades'), Card('A', 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 4

    # Test case 7: Flush
    player_cards = [Card(10, 'hearts'), Card('Q', 'hearts')]
    community_cards = [Card(2, 'hearts'), Card('K', 'hearts'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 5

    # Test case 8: Full House
    player_cards = [Card('A', 'hearts'), Card('A', 'diamonds')]
    community_cards = [Card(10, 'clubs'), Card('A', 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(10, 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 6

    # Test case 9: Four of a Kind
    player_cards = [Card(10, 'hearts'), Card(10, 'diamonds')]
    community_cards = [Card(10, 'clubs'), Card(10, 'spades'), Card(5, 'hearts'), Card(6, 'clubs'), Card(7, 'diamonds')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 7

    # Test case 10: Straight Flush
    player_cards = [Card(8, 'hearts'), Card('9', 'hearts')]
    community_cards = [Card(10, 'hearts'), Card('J', 'hearts'), Card('Q', 'hearts'), Card('K', 'spades'), Card(3, 'spades')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 8

    # Test case 11: Random Hand
    player_cards = [Card(2, 'hearts'), Card('7', 'diamonds')]
    community_cards = [Card(10, 'hearts'), Card('J', 'hearts'), Card('Q', 'hearts'), Card('K', 'spades'), Card(3, 'spades')]
    # Adjust the expected result based on the specific hand
    assert evaluator.evaluate_hand(player_cards, community_cards) == 0

    # Test case 12: Ace-low Straight Flush
    player_cards = [Card('A', 'hearts'), Card('2', 'hearts')]
    community_cards = [Card('3', 'hearts'), Card('4', 'hearts'), Card('5', 'hearts'), Card('6', 'spades'), Card('7', 'spades')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 8

    # Test case 13: 5 high straight flush
    player_cards = [Card('A', 'hearts'), Card('2', 'hearts')]
    community_cards = [Card('3', 'hearts'), Card('4', 'hearts'), Card('5', 'hearts'), Card('6', 'spades'), Card('7', 'spades')]
    assert evaluator.evaluate_hand(player_cards, community_cards) == 8

def test_compare_kickers():
    # Test Case 1: Same pair, different kickers
    hand1 = [Card('2', 'hearts'), Card('2', 'spades'), Card('5', 'diamonds')]
    hand2 = [Card('2', 'clubs'), Card('2', 'diamonds'), Card('7', 'hearts')]
    result1 = PokerHandEvaluator.compare_kickers(hand1, hand2)
    assert result1 == -1, f"Test Case 1 failed: Expected -1, got {result1}"

    # Test Case 2: Same pair, same kickers, higher pair wins
    hand3 = [Card('3', 'hearts'), Card('3', 'spades'), Card('5', 'diamonds')]
    hand4 = [Card('2', 'clubs'), Card('2', 'diamonds'), Card('5', 'hearts')]
    result2 = PokerHandEvaluator.compare_kickers(hand3, hand4)
    assert result2 == 1, f"Test Case 2 failed: Expected 1, got {result2}"

    # Test Case 3: Same pair, same kickers, tie
    hand5 = [Card('3', 'hearts'), Card('3', 'spades'), Card('5', 'diamonds')]
    hand6 = [Card('3', 'clubs'), Card('3', 'diamonds'), Card('5', 'hearts')]
    result3 = PokerHandEvaluator.compare_kickers(hand5, hand6)
    assert result3 == 0, f"Test Case 3 failed: Expected 0, got {result3}"

    print("All tests passed!")

def test_end_round():
    # Test Case 1: One player wins with a high card
    round1 = BettingRound([Player("Player1", 100), Player("Player2", 100)])
    round1.players[0].cards = [Card('A', 'hearts'), Card('8', 'diamonds')]
    round1.players[1].cards = [Card('K', 'spades'), Card('2', 'clubs')]
    community_cards = [Card('10', 'hearts'), Card('7', 'spades'), Card('5', 'diamonds')]
    result1 = round1.end_round(community_cards)
    assert result1 == [round1.players[0]], f"Test Case 1 failed: Expected [Player1], got {result1}"

    # Test Case 2: Player 2 wins with a pair
    round2 = BettingRound([Player("Player1", 100), Player("Player2", 100)])
    round2.players[0].cards = [Card('K', 'hearts'), Card('J', 'diamonds')]
    round2.players[1].cards = [Card('Q', 'spades'), Card('10', 'clubs')]
    community_cards = [Card('10', 'hearts'), Card('9', 'spades'), Card('8', 'diamonds')]
    result2 = round2.end_round(community_cards)
    assert result2 == [round2.players[1]], f"Test Case 2 failed: Expected [Player2], got {result2}"

    # Test Case 3: Three players tie with the same hand, resolved by kicker
    round3 = BettingRound([Player("Player1", 100), Player("Player2", 100), Player("Player3", 100)])
    round3.players[0].cards = [Card('9', 'hearts'), Card('9', 'diamonds')]
    round3.players[1].cards = [Card('9', 'spades'), Card('9', 'clubs')]
    round3.players[2].cards = [Card('10', 'spades'), Card('10', 'clubs')]
    community_cards = [Card('8', 'hearts'), Card('7', 'spades'), Card('6', 'diamonds')]
    result3 = round3.end_round(community_cards)
    assert result3 == [round3.players[2]], f"Test Case 3 failed: Expected [Player3], got {result3}"

    # Test Case 4: Both players tie with equal hands
    round4 = BettingRound([Player("Player1", 100), Player("Player2", 100)])
    round4.players[0].cards = [Card('Q', 'hearts'), Card('J', 'diamonds')]
    round4.players[1].cards = [Card('Q', 'spades'), Card('J', 'clubs')]
    community_cards = [Card('10', 'hearts'), Card('9', 'spades'), Card('8', 'diamonds')]
    result4 = round4.end_round(community_cards)
    assert result4 == [round4.players[1]], f"Test Case 4 failed: Expected [Player1, Player2], got {result4}"
