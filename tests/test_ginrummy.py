import pytest

from robo_croupier.common import Card
from robo_croupier.common import Hand
from robo_croupier.ginrummy import GinRummy
from robo_croupier.ginrummy import make_runs
from robo_croupier.ginrummy import Meld
from robo_croupier.ginrummy import score_meld_list
from robo_croupier.ginrummy import valid_meld_combos


@pytest.fixture
def hand_mock_a():
    cards = [
        Card(0, 3),
        Card(1, 5),
        Card(2, 6),
        Card(3, 7),
        Card(0, 4),
        Card(0, 5),
    ]
    h = Hand(cards)
    return h


@pytest.fixture
def melds_mock_a():
    melds = [
        Meld([Card(0, 1), Card(0, 2), Card(0, 3)]),
        Meld([Card(1, 11), Card(2, 11), Card(3, 11)]),
    ]
    return melds


def test_make_runs(hand_mock_a):
    h = hand_mock_a
    runs = make_runs(h.cards, min_run=3)
    print(runs)


def test_score_meld_list(melds_mock_a):
    m = melds_mock_a
    scores = score_meld_list(m)
    print()
    for i in scores:
        print(i)


def test_valid_meld_combos(melds_mock_a):
    m = melds_mock_a
    result = valid_meld_combos(m)
    print(result)
    print("Done!")


def test_sort_hand(hand_mock_a):
    print()
    h = hand_mock_a.cards
    print(h)
    print(h.sort())
    print(h)
    print(h[0] < h[1])
