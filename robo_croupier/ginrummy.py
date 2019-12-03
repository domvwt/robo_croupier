import logging
from dataclasses import dataclass
from itertools import groupby
from typing import List
from typing import Set

from robo_croupier.common import Card
from robo_croupier.common import Deck
from robo_croupier.common import Hand
from robo_croupier.common import Player
from robo_croupier.common import value_lookup
from robo_croupier.userinput import get_valid_input
from robo_croupier.userinput import select_menu

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.info("testing the logger")


class Meld(Set):
    def __init__(self, cards):
        super().__init__(cards)

    def __hash__(self):
        return hash(repr(self))


@dataclass
class MeldScore:
    meld: Meld
    score: int


def make_runs(cards: List[Card], min_run: int) -> List[Meld]:
    """
    Check for runs in suited and sorted sets of cards.

    :param min_run:
    :param cards:
    :return:
    """
    last_card = Card(-1, -1)
    this_run = []
    all_runs = []

    for card in cards:
        if card.value == last_card.value + 1:
            if len(this_run) >= min_run:
                all_runs.append(Meld(this_run))
            this_run.append(card)
        else:
            if len(this_run) >= min_run:
                all_runs.append(Meld(this_run))
            this_run = [card]
        last_card = card

    return all_runs


def make_melds(hand: Hand, min_run, min_set) -> List[Meld]:
    # Sort by value
    hand.cards.sort(key=lambda card: card.value)
    # Sort by suit
    hand.cards.sort(key=lambda card: card.suit)

    suit_sets = groupby(hand.cards, key=lambda card: card.suit)
    run_melds = [
        make_runs(list(suit_group), min_run=min_run)
        for _, suit_group in suit_sets
        if len(list(suit_group)) >= min_run
    ]

    # Unpack the list of lists into one list
    run_melds = [*run_melds]

    value_sets = groupby(hand.cards, key=lambda card: card.value)
    value_melds = [
        Meld(value_set)
        for _, value_set in value_sets
        if len(list(value_set)) >= min_set
    ]

    return run_melds + value_melds


score_lookup = {x: min(x + 1, 10) for x in value_lookup.keys()}


def score_meld(meld: Meld) -> int:
    return sum([score_lookup.get(card.value) for card in meld])


def score_meld_list(melds: List[Meld]) -> List[MeldScore]:
    meld_scores = [MeldScore(meld, score_meld(meld)) for meld in melds]
    return meld_scores


def valid_meld_combos(meld_list: List[Meld]) -> List[List[Meld]]:
    """
    Recursively generate all valid combinations of melds.

    :param meld_list:
    :return:
    """

    def recurse_combos(prime: Meld, remaining: List[Meld], acc: List[Meld]):
        remaining = remaining.copy()
        remaining.remove(prime)
        if len(remaining) == 1:
            if prime.isdisjoint(acc):
                acc.append(prime)
            combos.append(acc)
        else:
            if prime.isdisjoint(acc):
                acc.append(prime)
                remaining.remove(prime)
            for meld_b in remaining:
                recurse_combos(meld_b, remaining, acc)

    combos = []
    for meld_a in meld_list:
        recurse_combos(prime=meld_a, remaining=meld_list, acc=[])

    return combos


class GinRummy:
    def __init__(self, score_limit=500):
        self.game_name = "Gin Rummy"
        self.deck = Deck()
        self.discard_pile = List[Card]
        self.score_limit = score_limit
        self.players = []

    def setup_actions(self):
        # how many players
        # TODO: Define max number of players
        player_count = get_valid_input(
            prompt="How many players are there?: ",
            valid_class=int,
            invalid_msg="Please enter a valid number",
        )

        # create players
        for i in range(1, player_count + 1):
            player_name = input(f"Enter {i} player name: ")
            self.players.append(
                Player(name=player_name, hand=Hand(self.deck.deal(num_cards=7)))
            )

        self.discard_pile = self.deck.deal(1)

    def round_actions(self):
        knocked = False
        round_end_conds = len(self.deck.cards_remaining) <= 2 or knocked
        game_end_conds = self.max_player_score() >= self.score_limit
        round_number = 0
        game_number = 0
        while not game_end_conds:
            game_number += 1
            knocked = False
            while not round_end_conds:
                round_number += 1
                for p in self.players:
                    # TODO: Print player name
                    # TODO: Print current score
                    # TODO: Press any key to continue or press 's' to see the scoreboard
                    print(f"Player: {p.name}")
                    print(p.hand)

                    # TODO: Pick discard or from deck
                    last_discard = self.discard_pile[-1]
                    print(f"Discard pile: {last_discard}")

                    card_options = ["Deck", "Discard Pile"]
                    card_choice = select_menu(
                        "Choose where to draw from: ", select_from=card_options
                    )
                    if card_choice == "Deck":
                        new_card = self.deck.deal(1)
                    else:
                        new_card = last_discard

                    p.hand += new_card
                    discard_options = p.hand[:-1]
                    discard_selection = select_menu(
                        "Choose which to discard", select_from=discard_options
                    )

                    p.hand.remove(discard_selection)
                    self.discard_pile += discard_selection

                    # TODO: Calculate score

                    # TODO: If hand value 10 or less: Knock or continue?
                    knock_response = select_menu(
                        "Do you want to knock?", select_from=["Yes", "No"]
                    )
                    if knock_response == "Yes":
                        break

    def player_scores(self):
        return {player.name: player.game_score for player in self.players}

    def max_player_score(self):
        return max(self.player_scores().values())

    def play(self):
        self.setup_actions()
        self.round_actions()
        while len(self.deck.cards_remaining) > 0:
            pass
