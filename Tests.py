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