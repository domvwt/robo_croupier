# -*- coding: utf-8 -*-
"""Main module."""
import random
from dataclasses import dataclass
from dataclasses import field
from functools import total_ordering
from typing import List

suit_lookup = {0: "Clubs", 1: "Diamonds", 2: "Hearts", 3: "Spades"}

value_lookup = {
    0: "Ace",
    1: "Two",
    2: "Three",
    3: "Four",
    4: "Five",
    5: "Six",
    6: "Seven",
    7: "Eight",
    8: "Nine",
    9: "Ten",
    10: "Jack",
    11: "Queen",
    12: "King",
}


@dataclass
@total_ordering
class Card:
    """
    A playing card with a suit and a value.
    """

    suit: int
    value: int

    def __str__(self):
        return f"{value_lookup.get(self.value)} of {suit_lookup.get(self.suit)}"

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "suit") and hasattr(other, "value")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.suit, self.value) == (other.suit, other.value)

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        if self.value == other.value:
            return self.suit > other.suit
        else:
            return self.value > other.value

    def __hash__(self):
        return hash(repr(self))


@dataclass
@total_ordering
class Run:
    """
    Represents a run of cards and their collective value.
    """

    cards: List[Card]
    score: int

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "score")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.score == other.score

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        else:
            return self.score > other.score


# TODO: Use attr for simple classes
# TODO: Set up logging
class Deck:
    """
    Represents a standard 52 card deck.
    """

    def __init__(self):
        self.cards_remaining: List[Card] = [
            Card(suit, value) for suit in range(4) for value in range(13)
        ]
        self.shuffle()
        self.cards_dealt: List[Card] = list()

    def shuffle(self):
        """
        Randomly shuffle the remaining cards in the deck.
        """
        r = random.SystemRandom()
        r.shuffle(self.cards_remaining)

    def deal(self, num_cards: int) -> List[Card]:
        """
        Deal a specified number of cards by removing them from the remaining Deck.
        :param num_cards: How many cards to deal.
        :return: List[Card]
        """
        drawn = self.cards_remaining[:num_cards]
        del self.cards_remaining[:num_cards]
        self.cards_dealt += drawn
        return drawn

    def cards_remaining(self) -> List[Card]:
        """
        Show the cards left in the deck.
        :return: List[Card]
        """
        return self.cards_remaining

    def cards_dealt(self) -> List[Card]:
        """
        Show the cards played from the deck.
        :return: List[Card]
        """
        pass


class Hand:
    """
    Represents a hand of cards with associated methods.
    """

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __str__(self):
        return str([self.cards])

    def select(self, *args: int):
        selection_idx = list(*args)
        selected = [self.cards[i] for i in selection_idx]
        self.cards = list(set(self.cards) - set(selected))
        return selected


@dataclass
class Player:
    """
    Holds information regarding a card player.
    """

    name: str = ""
    game_score: int = 0
    role: str = ""
    round_score: int = 0
    turns_taken: int = 0
    hand: Hand = field(default_factory=list)
