""" Cribbage scorer unit tests """
import unittest
import cribbage_hand_scorer as chs

class TestCribbageHandScorer(unittest.TestCase):
  """ Test the cribbage scorer """

  def _test_one_score(self, cards, top_of_deck_card, expected_score):
    """
    Helper function to score one set of cards
    """
    scored_list, _ = chs.score(cards, top_of_deck_card)
    my_score, my_hand = scored_list[0]
    self.assertEqual(my_score, expected_score,
                     'The score was not ' + str(expected_score) +
                     ' and was ' + str(my_score) + ' for ' +
                     str(my_hand) + ', ' + str(top_of_deck_card))
    return my_score

  def _test_for_exception(self, cards, top_of_deck_card):
    self.assertRaises(Exception, chs.score,
                      cards, top_of_deck_card)

  def test_big_scores(self):
    """
    Tests for randomly selected large hand totals
    """
    hand, top_of_deck_card = ([(5, 's'), (5, 'h'), (5, 'd'), (11, 'c')],
                              (5, 'c'))
    # 6 pairs, 8 15's, his nibs
    expected_score = chs.PAIR_SCORE * 6 + chs.SPECIAL_TOTAL_SCORE * 8 + \
                     chs.HIS_NIBS_SCORE
    self._test_one_score(hand, top_of_deck_card, expected_score)

    hand, top_of_deck_card = ([(5, 's'), (5, 'h'), (5, 'd'), (5, 'c')],
                              (11, 'c'))
    # 6 pairs, 8 15's
    expected_score = chs.PAIR_SCORE * 6 + chs.SPECIAL_TOTAL_SCORE * 8
    self._test_one_score(hand, top_of_deck_card, expected_score)

    for hand, top_of_deck_card in [
            ([(7, 's'), (7, 'h'), (7, 'd'), (7, 'c')], (1, 'c')),
            ([(3, 's'), (3, 'h'), (3, 'd'), (3, 'c')], (9, 'c')),
            ([(3, 's'), (6, 'h'), (6, 'd'), (6, 'c')], (6, 's')),
            ([(4, 's'), (4, 'h'), (4, 'd'), (4, 'c')], (7, 'c'))]:
      # 6 pairs, 6 15's
      expected_score = chs.PAIR_SCORE * 6 + chs.SPECIAL_TOTAL_SCORE * 6
      self._test_one_score(hand, top_of_deck_card, expected_score)

    for hand, top_of_deck_card in [
            ([(4, 's'), (4, 'h'), (5, 'd'), (5, 'c')], (6, 'c')),
            ([(4, 's'), (4, 'h'), (5, 'd'), (6, 'c')], (6, 's')),
            ([(4, 's'), (5, 'h'), (5, 'd'), (6, 'c')], (6, 's')),
            ([(6, 's'), (7, 'h'), (7, 'd'), (8, 'c')], (8, 's')),
            ([(7, 's'), (7, 'h'), (8, 'd'), (8, 'c')], (9, 's'))]:
      # 2 pairs, 4 15's, 4 3-card sequences
      expected_score = chs.PAIR_SCORE * 2 + chs.SPECIAL_TOTAL_SCORE * 4 + \
                       chs.SINGLE_CARD_SCORE * 3 * 4
      self._test_one_score(hand, top_of_deck_card, expected_score)

    hand, top_of_deck_card = ([(2, 's'), (2, 'h'), (2, 'd'), (2, 'c')],
                              (9, 's'))
    # 6 pairs, 4 15's
    expected_score = chs.PAIR_SCORE * 6 + chs.SPECIAL_TOTAL_SCORE * 4
    self._test_one_score(hand, top_of_deck_card, expected_score)

    hand, top_of_deck_card = ([(2, 'h'), (6, 'h'), (7, 'h'), (8, 'h')],
                              (7, 'd'))
    # 1 pair, 4 15's, 2 3-card sequences, 1 4-card flush
    expected_score = chs.PAIR_SCORE + chs.SPECIAL_TOTAL_SCORE * 4 + \
                     chs.SINGLE_CARD_SCORE * 3 * 2 + chs.SINGLE_CARD_SCORE * 4
    self._test_one_score(hand, top_of_deck_card, expected_score)

  def test_his_nibs(self):
    """
    Tests for his nibs
    """
    # No his nibs but J in hand
    hand, top_of_deck_card = ([(2, 's'), (4, 'h'), (6, 's'), (11, 's')],
                              (10, 'c'))
    self._test_one_score(hand, top_of_deck_card, 0)
    # His nibs with J in hand
    hand, top_of_deck_card = ([(2, 's'), (4, 'h'), (6, 's'), (11, 's')],
                              (10, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.HIS_NIBS_SCORE)

  def test_flushes(self):
    """
    Tests for flushes
    """
    # No flush even though top-of-deck card matches to make 4-hand flush
    hand, top_of_deck_card = ([(2, 's'), (4, 'h'), (6, 's'), (8, 's')],
                              (10, 's'))
    self._test_one_score(hand, top_of_deck_card, 0)
    # 4-card flush in hand with no top-of-deck card match
    hand, top_of_deck_card = ([(2, 's'), (4, 's'), (6, 's'), (8, 's')],
                              (10, 'c'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 4)
    # 5-card flush with top-of-deck card match
    hand, top_of_deck_card = ([(2, 's'), (4, 's'), (6, 's'), (8, 's')],
                              (10, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 5)

  def test_sequences(self):
    """
    Test for sequences
    """
    # 3-card sequence with no top-of-deck card match
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (7, 'd')],
                              (1, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3)
    # 3-card sequence with top-of-deck card match
    hand, top_of_deck_card = ([(1, 's'), (10, 'h'), (11, 'c'), (7, 'd')],
                              (9, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3)
    # 4-card sequence with no top-of-deck card match
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (12, 'd')],
                              (1, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 4)
    # 4-card sequence with top-of-deck card match
    hand, top_of_deck_card = ([(1, 's'), (10, 'h'), (11, 'c'), (12, 'd')],
                              (9, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 4)
    # 5-card sequence with top-of-deck card match
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (12, 'd')],
                              (13, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 5)
    # Double 3-card sequence with no top-of-deck card match (1 pair total)
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (1, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3 * 2 + chs.PAIR_SCORE)
    # Double 3-card sequence with top-of-deck card match (1 pair total)
    hand, top_of_deck_card = ([(1, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (9, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3 * 2 + chs.PAIR_SCORE)
    # Double 4-card sequence with no top-of-deck pair (1 pair total)
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (12, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 4 * 2 + chs.PAIR_SCORE)
    # Double 4-card sequence with top-of-deck card pair (1 pair total)
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (12, 'd')],
                              (9, 'd'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 4 * 2 + chs.PAIR_SCORE)
    # Double double 3-card sequence with no top-of-deck card pair
    # (2 pairs total)
    hand, top_of_deck_card = ([(10, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (9, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3 * 4 + chs.PAIR_SCORE * 2)
    # Double double 3-card sequence with top-of-deck card pair (2 pairs total)
    hand, top_of_deck_card = ([(9, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (10, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3 * 4 + chs.PAIR_SCORE * 2)
    # Triple 3-card sequence with top-of-deck card pair (3 pairs total)
    hand, top_of_deck_card = ([(1, 's'), (2, 'h'), (3, 'c'), (3, 'd')],
                              (3, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.SINGLE_CARD_SCORE * 3 * 3 + chs.PAIR_SCORE * 3)

  def test_pairs(self):
    """
    Test pairs
    """
    # No pairs
    hand, top_of_deck_card = ([(6, 's'), (10, 'h'), (11, 'c'), (7, 'd')],
                              (1, 's'))
    self._test_one_score(hand, top_of_deck_card, 0)
    # One pair with no top-of-deck pair
    hand, top_of_deck_card = ([(6, 's'), (10, 'h'), (11, 'c'), (11, 'd')],
                              (1, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE)
    # One pair with top-of-deck pair
    hand, top_of_deck_card = ([(6, 's'), (10, 'h'), (11, 'c'), (1, 'd')],
                              (11, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE)
    # Two pairs with no top-of-deck pair
    hand, top_of_deck_card = ([(6, 's'), (10, 'h'), (10, 'c'), (6, 'd')],
                              (11, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 2)

    # Two pairs with top-of-deck pair
    hand, top_of_deck_card = ([(11, 'h'), (10, 'h'), (10, 'c'), (6, 'd')],
                              (6, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 2)
    # Three pairs (same card) with no top-of-deck pair
    hand, top_of_deck_card = ([(10, 'h'), (10, 's'), (10, 'c'), (6, 'd')],
                              (7, 's'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 3)
    # Three pairs (same card) with top-of-deck pair
    hand, top_of_deck_card = ([(10, 'h'), (10, 's'), (7, 'c'), (6, 'd')],
                              (10, 'd'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 3)
    # Six pairs (same card) with no top-of-deck pair
    hand, top_of_deck_card = ([(10, 'h'), (10, 's'), (10, 'c'), (10, 'd')],
                              (1, 'd'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 6)
    # Six pairs (same card) with top-of-deck pair
    hand, top_of_deck_card = ([(1, 'h'), (10, 's'), (10, 'c'), (10, 'd')],
                              (10, 'h'))
    self._test_one_score(hand, top_of_deck_card,
                         chs.PAIR_SCORE * 6)

  def test_special_totals(self):
    """
    Test special totals
    """
    # One special total with 2-card 10/5 (with testing for 10, J, Q, K)
    for hand, top_of_deck_card in [
            ([(3, 's'), (8, 'h'), (6, 'd'), (5, 'c')], (10, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (10, 'c')], (5, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (5, 'c')], (11, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (11, 'c')], (5, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (5, 'c')], (12, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (12, 'c')], (5, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (5, 'c')], (13, 's')),
            ([(3, 's'), (8, 'h'), (6, 'd'), (13, 'c')], (5, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE)

    # One special total with 2-card 6/9
    for hand, top_of_deck_card in [
            ([(1, 's'), (2, 'h'), (12, 'd'), (6, 'c')], (9, 's')),
            ([(1, 's'), (2, 'h'), (12, 'd'), (9, 'c')], (6, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE)

    # One special total with 2-card 7/8
    for hand, top_of_deck_card in [
            ([(1, 's'), (3, 'h'), (12, 'd'), (7, 'c')], (8, 's')),
            ([(1, 's'), (3, 'h'), (12, 'd'), (8, 'c')], (7, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE)

    # Can add tests for one special total with 3-card 10/5
    # (1+4/10,2+3/10,1+9/5,2+8/5,3+7/5,4+6/5)

    # Can add tests for one special total with 3-card 6/9
    # (1+5/9,2+4/9,3+3/9,1+8/6,2+7/6,3+6/6,4+5/6)

    # Can add tests for one special total with 3-card 7/8
    # (1+6/8,2+5/8,3+4/8,1+7/7,2+6/7,3+5/7,4+4/7)

    # Other tests can be added for one special total with 4- and 5-card
    # 10/5's, 6/9's, and 7/8's

    # Will only test one case here for 2 special totals
    for hand, top_of_deck_card in [
            ([(1, 's'), (4, 'h'), (12, 'd'), (7, 'c')], (8, 's')),
            ([(1, 's'), (4, 'h'), (12, 'd'), (8, 'c')], (7, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 2)

    # Will only test two cases here for 3 special totals
    for hand, top_of_deck_card in [
            ([(3, 's'), (5, 'h'), (7, 'd'), (8, 'c')], (10, 's')),
            ([(10, 's'), (5, 'h'), (7, 'd'), (8, 'c')], (3, 's')),
            ([(1, 's'), (5, 'h'), (13, 'd'), (11, 'c')], (10, 's')),
            ([(1, 's'), (10, 'h'), (13, 'd'), (11, 'c')], (5, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 3)

    # Cannot think of a way to test for 4 special totals without
    # scoring some other way as well
    # The test case below has a pair of 10's (so we score that too)
    for hand, top_of_deck_card in [
            ([(5, 's'), (10, 'h'), (10, 'd'), (11, 'c')], (13, 's')),
            ([(5, 's'), (13, 'h'), (10, 'd'), (11, 'c')], (10, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 4 +
                           chs.PAIR_SCORE)

    # Cannot think of a way to test for 5 special totals without
    # scoring some other way as well
    # The test case below has 2 pairs
    for hand, top_of_deck_card in [
            ([(3, 's'), (6, 'h'), (6, 'd'), (9, 'c')], (9, 's')),
            ([(9, 's'), (6, 'h'), (6, 'd'), (9, 'c')], (3, 's')),
            ([(1, 's'), (7, 'h'), (7, 'd'), (8, 'c')], (8, 's')),
            ([(8, 's'), (7, 'h'), (7, 'd'), (8, 'c')], (1, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 5 +
                           chs.PAIR_SCORE * 2)

    # Cannot think of a way to test for 6 special totals without
    # scoring some other way as well
    # The test case below has a pair of 5's (so we score that too)
    for hand, top_of_deck_card in [
            ([(5, 's'), (5, 'h'), (10, 'd'), (11, 'c')], (13, 's')),
            ([(13, 's'), (5, 'h'), (10, 'd'), (11, 'c')], (5, 's'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 6 +
                           chs.PAIR_SCORE)

    # Cannot think of a way to test for 7 special totals without
    # scoring some other way as well
    # The test case below has 3 pairs of 5's (so we score that too)
    for hand, top_of_deck_card in [
            ([(5, 's'), (5, 'h'), (5, 'd'), (11, 'c')], (13, 's')),
            ([(5, 's'), (5, 'h'), (13, 'd'), (11, 'c')], (5, 'd'))]:
      self._test_one_score(hand, top_of_deck_card,
                           chs.SPECIAL_TOTAL_SCORE * 7 +
                           chs.PAIR_SCORE * 3)

  def test_invalid_hands(self):
    """
    Tests for cards that are invalid, too few cards, duplicate cards
    """
    for hand, top_of_deck_card in [
            # Insufficient hands
            ([], (None, None)),
            ([], (1, 's')),
            ([(1, 's')], (None, None)),
            ([(1, 's')], (1, 's')),
            ([(1, 's'), (2, 's'), (3, 's'), (4, 's')], (None, None)),
            ([(1, 's'), (2, 's'), (3, 's')], (4, 's')),
            # Invalid cards
            ([(1, 's'), (2, 's'), (3, 's'), (4, 'a')], (None, None)),
            ([(1, 's'), (2, 's'), (3, 's'), (16, 's')], (4, 's')),
            # Duplicated cards
            ([(1, 's'), (2, 's'), (3, 's'), (4, 's')], (4, 's')),
            ([(1, 's'), (1, 's'), (3, 's'), (4, 's')], (2, 's'))]:
      self._test_for_exception(hand, top_of_deck_card)

if __name__ == '__main__':
  unittest.main()
