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