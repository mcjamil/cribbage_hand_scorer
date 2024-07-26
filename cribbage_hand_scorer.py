"""
This is a cribbage scorer. It is meant to be used as a module to score
a cribbage hand. The most relevant function is score(); all other functions
are utilized by score() to generate the score for a given hand. The caller
can specify a top-of-deck card as an option; if specified, his nibs will
also be scored.

Key values (e.g., how many cards constitute a minimum-sized hand) are
defined as constants so the rules of cribbage can be
easily manipulated if necessary.
"""
from itertools import product, combinations, chain

_CARD_NUMBER_SMALLEST = 1
_CARD_NUMBER_LARGEST = 13
_CARD_NUMBERS = range(_CARD_NUMBER_SMALLEST, _CARD_NUMBER_LARGEST + 1)
_SUITS = ['s', 'h', 'd', 'c']
_ALL_CARDS = list(product(_CARD_NUMBERS, _SUITS))

SINGLE_CARD_SCORE = 1
HIS_NIBS_SCORE = SINGLE_CARD_SCORE * 1
PAIR_SCORE = SINGLE_CARD_SCORE * 2
SPECIAL_TOTAL_SCORE = SINGLE_CARD_SCORE * 2
SPECIAL_TOTAL = 15
MIN_HAND_SIZE = 4
MIN_SEQUENCE_SIZE = 3
MIN_FLUSH_SIZE = 4
MAX_CARD_NUMBER = 10

def score_his_nibs(cards):
  """
  Score his nibs (if present)
  This assumes the last element in the parameter provided is the
  top-of-deck card

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: his nibs score
  :rtype: int
  """
  # Split the incoming cards into the top-of-deck card and
  # the rest of the cards
  top_of_deck_card = cards[-1]
  other_cards = cards[:-1]

  # Find his nibs
  his_nibs_count = len([card for card in other_cards if
                        card[0] == 11 and card[1] == top_of_deck_card[1]])
  his_nibs_score = his_nibs_count * HIS_NIBS_SCORE

  return his_nibs_score

def score_flush(cards):
  """
  Score flush (if present)
  This assumes the last element in the parameter provided is the
  top-of-deck card

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: flush score
  :rtype: int
  """
  flush_score = 0
  # Split the incoming cards into the top-of-deck card and
  # the rest of the cards
  top_of_deck_card = cards[-1]
  other_cards = cards[:-1]

  # Check to see that at least MIN_FLUSH_SIZE cards are present;
  # if not, return immediately
  if len(other_cards) < MIN_FLUSH_SIZE:
    return flush_score
  # Use set comprehension to make a set of the second element
  # for each card (that's the suit)
  # If the set has only one element, then all cards have the same suit
  suits = {card[1] for card in other_cards}
  if len(suits) == 1:
    flush_score = len(other_cards) * SINGLE_CARD_SCORE
    # Add in an extra point for the top-of-deck card if it also matches suit
    if suits == set(top_of_deck_card[1]):
      flush_score += SINGLE_CARD_SCORE
  return flush_score

def score_sequence(cards):
  """
  Score a sequence (if present)

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: sequence score
  :rtype: int
  """
  sequence_score = 0
  # Check to see that at least MIN_SEQUENCE_SIZE cards are present;
  # if not, return immediately
  if len(cards) < MIN_SEQUENCE_SIZE:
    return sequence_score
  # Use list comprehension to make a list of the first element
  # for each card (that's the card number)
  card_numbers = [card[0] for card in cards]
  # Sort the list before checking the sequence is valid
  card_numbers.sort()
  # Use set comprehension to make a set of the integer difference
  # between successive elements
  # If it's a sequence, all the set differences will be 1, so the
  # set will contain only one element with the value 1
  card_number_differences = {card_numbers[i + 1] - card_numbers[i]
                             for i in range(len(card_numbers) - 1)}
  if len(card_number_differences) == 1 and \
    next(iter(card_number_differences)) == 1:
    sequence_score += len(cards) * SINGLE_CARD_SCORE
  return sequence_score

def score_sequences(cards):
  """
  This function generates scores of any sequences present in valid
  subsets of the parameter provided. It then sums the max scores
  (since each max score represents the score for the longest unique sequence)

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: sum of max sequence scores (if sequences exist)
  :rtype: int
  """
  # Generate all the sublists of the cards that contain
  # MIN_SEQUENCE_SIZE or more cards
  card_sublists = []
  for i in range(MIN_SEQUENCE_SIZE, len(cards) + 1):
    card_sublists.append(list(combinations(cards, i)))
  # This generates a nested list so use some itertools magic
  # to flatten the list to one dimension
  card_sublists = list(chain.from_iterable(card_sublists))

  # Score each sublist and score by score total
  card_sublist_scores = [score_sequence(card_sublist)
                         for card_sublist in card_sublists]

  # Now count the highest scores (duplicates are expected
  # for multiple runs with different suits)
  max_sublist_score = max(card_sublist_scores)
  count_max_scores = sum(1 for i in card_sublist_scores
                         if i == max_sublist_score)

  # Finally return the total of the max scores
  sequences_score = max_sublist_score * count_max_scores

  return sequences_score

def score_pairs(cards):
  """
  Score pairs

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: sum of pairs
  :rtype: int
  """
  # Generate all the pair sublists of the cards
  card_pairs = list(combinations(cards, 2))

  # Now count and score each pair
  count_pairs = sum(1 for card1, card2 in card_pairs if card1[0] == card2[0])
  card_pairs_score = count_pairs * PAIR_SCORE
  return card_pairs_score

def score_special_totals(cards):
  """
  Score special totals (which is 15 in usual cribbage).
  This ensures a given card can only have a max numeric value of
  MAX_CARD_NUMBER.

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :returns: sum of special totals score
  :rtype: int
  """
  # Generate all the sublists of the cards
  card_sublists = []
  for i in range(1, len(cards) + 1):
    card_sublists.append(list(combinations(cards, i)))
  # This generates a nested list so use some itertools magic
  # to flatten the list to one dimension
  card_sublists = list(chain.from_iterable(card_sublists))

  # METHOD 1: Non-pythonic
  #special_totals_score = 0
  # Now score each sublist and increment the total score by
  # the score for each SPECIAL_TOTAL (SPECIAL_TOTAL_SCORE)
  #for card_sublist in card_sublists:
  #  subtotal = 0
  #  for card_number, _ in card_sublist:
      # If the card number is greater than MAX_CARD_NUMBER,
      # then treat its score as MAX_CARD_NUMBER
  #    if card_number > MAX_CARD_NUMBER:
  #      card_number = MAX_CARD_NUMBER
  #    subtotal += card_number
  #  if subtotal == SPECIAL_TOTAL:
  #    special_totals_score += SPECIAL_TOTAL_SCORE

  # METHOD 2: Pythonic (i.e., comprehensions instead of for loops)
  # Convert list of card sublists into a list of card number totals for each
  # card sublist (with each card number being MAX_CARD_NUMBER or lower)
  # Example: [[(2, 'h'), (11, 'd')], [(3, 'd')]] -> [[12], [3]]
  card_total_sublists = [sum([MAX_CARD_NUMBER if
                              card_number >= (MAX_CARD_NUMBER)
                              else card_number
                              for card_number, _ in card_sublist])
                          for card_sublist in card_sublists]
  # Only consider the sublist totals that match SPECIAL_TOTAL
  special_total_sublists = [total for total in card_total_sublists
                            if total == SPECIAL_TOTAL]
  special_totals_score = len(special_total_sublists) * SPECIAL_TOTAL_SCORE

  return special_totals_score

def score_min_card_combo(cards, top_of_deck_card):
  """
  Score a hand

  :param cards: tuple of card tuples (e.g., ((5, 'h'), (3, 'c')) )
  :type cards: tuple(tuple(int, str), ...)
  :param top_of_deck_card: card tuple (e.g., (4, 'c') )
  :type top_of_deck_card: tuple(int, str) or None
  :returns: hand score
  :rtype: int
  """
  combo_score = 0

  # Ensure the top-of-deck card is included in the consideration when scoring
  if top_of_deck_card is not None:
    cards += (top_of_deck_card,)
    # Score "his nibs"
    combo_score += score_his_nibs(cards)

  # Score a flush (if present)
  combo_score += score_flush(cards)

  # Score a sequence or sequences (if present)
  combo_score += score_sequences(cards)

  # Score pairs (if present)
  combo_score += score_pairs(cards)

  # Score special totals (if present)
  combo_score += score_special_totals(cards)

  # Finally return the cumulative score
  return combo_score

def score(cards, top_of_deck_card=None):
  """
  This generates a cribbage score for an arbitrary sized list of cards.
  It will create a list of combinations of MIN_HAND_SIZE and score each.

  :param cards: list of card tuples (e.g., [(5, 'h'), (3, 'c')] )
  :type cards: list[tuple(int, str)]
  :param top_of_deck_card: card tuple (e.g., (4, 'c') )
  :type top_of_deck_card: tuple(int, str) or None
  :returns: tuple of scored hands and top-of-deck card where scored hands is
            a list of tuples of the format (score for a given card combination,
            the given card combination) and top-of-deck card is a card tuple
            e.g., ([(20, ((2, 'h'), (6, 'h'), (7, 'h'), (8, 'h')))], (7, 'd'))
  :rtype: tuple(list[tuple(int, tuple(tuple(int, str), ...))],
          tuple(int, str) or None)
  :raises Exception: if the hand or the top-of-deck card is invalid
  """
  # Check to see that the hand contains valid cards by comparing against
  # elements in _ALL_CARDS, ensuring there are enough cards, and
  # ensuring there are no duplicate cards
  if not set(cards).issubset(_ALL_CARDS):
    raise Exception("Invalid hand provided: Contains cards that are invalid")
  if len(cards) < MIN_HAND_SIZE:
    raise Exception("Invalid hand provided: Contains not enough cards")
  if len(cards) != len(set(cards)):
    raise Exception("Invalid hand provided: Contains duplicate cards")

  # Also check that the top-of-deck card contains a valid card by comparing
  # against elements in _ALL_CARDS and the hand
  if top_of_deck_card is not None:
    if not set([top_of_deck_card]).issubset(_ALL_CARDS):
      raise Exception("Invalid top-of-deck card provided: Card is invalid")
    if set([top_of_deck_card]).issubset(cards):
      raise Exception("Invalid top-of-deck card provided: Card is duplicated")

  # Find all min-card combinations
  min_card_combos = list(combinations(cards, MIN_HAND_SIZE))

  # Score each min-card combination and
  # create a list with a two-member tuple (score, hand)
  min_card_combos_plus_scores = [(score_min_card_combo(hand, top_of_deck_card),
                                  hand)
                                 for hand in min_card_combos]

  # This will automatically sort by the first element in the list
  # (which is the score)
  min_card_combos_plus_scores.sort()

  return (min_card_combos_plus_scores, top_of_deck_card)

def print_score(scored_hands_with_topper):
  """
  For each scored hand provided as input, print each combination of
  hand and top-of-deck card, and its associated score

  :param scored_hands_with_topper: tuple of scored hands and top-of-deck card
                                   where scored hands is a list of tuples of
                                   the format
                                   (score for a given card combination,
                                   the given card combination)
                                   and top-of-deck card is a card tuple
                                   e.g., ([(20,
                                            ((2, 'h'), (6, 'h'),
                                             (7, 'h'), (8, 'h')))],
                                          (7, 'd'))
  :type scored_hands_with_topper: tuple(
                                    list[tuple(int,
                                                tuple(tuple(int, str), ...))],
                                    tuple(int, str) or None)
  """
  scored_hands, top_of_deck_card = scored_hands_with_topper
  for hand_score, hand in scored_hands:
    print("Hand: " + str(hand) + " + top-of-deck: " +
          str(top_of_deck_card) + ", score: " + str(hand_score))

if __name__ == '__main__':
  # Test for 29
  print_score(score([(5, 's'), (5, 'h'), (5, 'd'), (11, 'c')], (5, 'c')))

  # Test for 28
  print_score(score([(5, 's'), (5, 'h'), (5, 'd'), (5, 'c')], (11, 'c')))

  # Tests for 24
  print_score(score([(7, 's'), (7, 'h'), (7, 'd'), (7, 'c')], (1, 'c')))
  print_score(score([(3, 's'), (3, 'h'), (3, 'd'), (3, 'c')], (9, 'c')))
  print_score(score([(3, 's'), (6, 'h'), (6, 'd'), (6, 'c')], (6, 's')))
  print_score(score([(4, 's'), (4, 'h'), (4, 'd'), (4, 'c')], (7, 'c')))
  print_score(score([(4, 's'), (4, 'h'), (5, 'd'), (5, 'c')], (6, 'c')))
  print_score(score([(4, 's'), (4, 'h'), (5, 'd'), (6, 'c')], (6, 's')))
  print_score(score([(4, 's'), (5, 'h'), (5, 'd'), (6, 'c')], (6, 's')))
  print_score(score([(6, 's'), (7, 'h'), (7, 'd'), (8, 'c')], (8, 's')))
  print_score(score([(7, 's'), (7, 'h'), (8, 'd'), (8, 'c')], (9, 's')))

  # Tests for max score (20) with a 2
  print_score(score([(2, 's'), (2, 'h'), (2, 'd'), (2, 'c')], (9, 's')))
  print_score(score([(2, 'h'), (6, 'h'), (7, 'h'), (8, 'h')], (7, 'd')))

  # Tests for a larger list
  print_score(score([(2, 's'), (2, 'h'), (2, 'd'), (2, 'c'), (1, 'c')],
                    (9, 's')))
