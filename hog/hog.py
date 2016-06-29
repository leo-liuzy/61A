"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    dice_sum = 0
    have_one = False
    while num_rolls > 0:
        dice_num = dice()
        if dice_num == 1:
            have_one = True
        else:
            dice_sum += dice_num
        num_rolls -= 1
    if have_one:
        dice_sum = 1
    return dice_sum
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    units = opponent_score % 10
    tens = (opponent_score - units)//10
    if is_prime(max(units,tens)+1):
        return next_prime(max(units,tens)+1)
    else:
        return max(units,tens)+1
    # END PROBLEM 2

# Write your prime functions here!
def is_prime(x):
    input_num = x
    if input_num == 1 or input_num == 0:
        return False
    if input_num == 2:
        return True
    for num in range(2,x):
        if input_num % num == 0:
            return False
    return True

def next_prime(x):
    x += 1
    while not is_prime(x):
        x += 1
    return x


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        current_score = roll_dice(num_rolls,dice)
        if is_prime(current_score):
            # print('is_prime == ',next_prime(current_score))
            return next_prime(current_score)
        else:
            # print('not_prime == ',current_score)
            return current_score
    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

def max_dice(score, opponent_score):
    """Return the maximum number of dice the current player can roll. The
    current player can roll at most 10 dice unless the sum of SCORE and
    OPPONENT_SCORE ends in a 7, in which case the player can roll at most 1.
    """
    # BEGIN PROBLEM 3
    if (score + opponent_score) % 10 == 7:
        return 1
    else:
        return 10
    
    # END PROBLEM 3


def is_swap(score):
    """Returns whether the SCORE contains only one unique digit, such as 22.
    """
    # BEGIN PROBLEM 4
    units = score % 10
    tens = ((score - units)//10) % 10
    hundreds = (score - 10 * tens - units)//100

    # print(units,tens,hundreds)

    zzn = (not hundreds)and(not tens)
    znn = (not hundreds)and(tens and units)and(tens==units)
    nnn = (hundreds and tens and units)and(hundreds==tens)and(tens==units)

    if zzn or znn or nnn:
        return True
    else:
        return False 


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def one_turn(player,strategy,score_current,score_opposite):
    num_rolls = strategy(score_current,score_opposite)
    max_num_roll = max_dice(score_current, score_opposite)
    num_rolls = min(max_num_roll,num_rolls)
    # print('num_rolls:',num_rolls)
    dice = select_dice(score_current,score_opposite)
    # print('before_add_this_turn',score_current)
    score_current = score_current + take_turn(num_rolls,score_opposite,dice)
    # print('after_add_this_turn',score_current)
    if is_swap(score_current):
        temp = score_current
        score_current = score_opposite
        score_opposite = temp
    player = other(player)
    return score_current,score_opposite,player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if not player:
            score0,score1,player = one_turn(player,strategy0,score0,score1)
            # print('score0:',score0,'score1:',score1)
        else:
            score1,score0,player = one_turn(player,strategy1,score1,score0)
            # print('score0:',score0,'score1:',score1)
    # END PROBLEM 5
    return score0, score1

if __name__ == '__main__':
    import hog
    hog.four_sided = hog.make_test_dice(1)
    hog.six_sided = hog.make_test_dice(3)
    always = hog.always_roll
    s0, s1 = hog.play(always(0), always(0),score0=98,score1=1)
    print(s0,s1)

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    @check_strategy
    def strategy(score, opponent_score):
        return n

    return strategy

def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid strategy
    output. All strategy outputs must be non-negative integers less than or
    equal to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'

def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the 
    strategy returns a valid input. Use `check_strategy_roll` to raise 
    an error with a helpful message if the strategy retuns an invalid 
    output.

    >>> always_roll_5 = always_roll(5)
    >>> always_roll_5 == check_strategy(always_roll_5)
    True
    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> fail_15_20 == check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (invalid number of rolls)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> fail_102_115 == check_strategy(fail_102_115)
    True
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    # END PROBLEM 6
    for score in range(0,goal+1):
        for opponent_score in range(0,goal+1):
            num_rolls = strategy(score,opponent_score)
            check_strategy_roll(score,opponent_score,num_rolls)
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def inside(*args):
        dice_sum = 0
        for index in range(0,num_samples):
            dice_sum += fn(*args)
        return dice_sum/num_samples
    return inside
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    # make_averaged roll_dice
    max_scoring = 0
    max_scoring_num = 0
    for num_rolls in range(1,11):
        current_scoring = make_averaged(roll_dice,num_samples)(num_rolls,dice)
        if current_scoring > max_scoring:
            max_scoring = current_scoring
            max_scoring_num = num_rolls
    return max_scoring_num
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

@check_strategy
def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    if free_bacon(opponent_score) > margin-1:
        return 0
    else:
        return num_rolls
    # END PROBLEM 9


@check_strategy
def swap_strategy(score, opponent_score, margin=5, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and doesn't trigger a
    swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    
    if is_swap(score + free_bacon(opponent_score)) and score < 92 and opponent_score > score + free_bacon(opponent_score):
        return 0
    elif not is_swap(score + free_bacon(opponent_score)) and free_bacon(opponent_score) > margin-1:
        return 0
    if max_dice(score+1,opponent_score) == 1:
        return num_rolls
    if select_dice(score+1,opponent_score) == 1:
        return num_rolls
    
    else:
        return num_rolls
    # END PROBLEM 10



@check_strategy
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    default: swap_strategy
    *** YOUR DESCRIPTION HERE ***
    """
    roll_nums = swap_strategy(score,opponent_score)
    return roll_nums

    # END PROBLEM 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()