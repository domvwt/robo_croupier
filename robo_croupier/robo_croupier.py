# -*- coding: utf-8 -*-
"""Main module."""
import random
from dataclasses import dataclass


@dataclass
class Card:
    suit: int
    value: int


class Deck:
    def __init__(self):
        self.cards_remaining = [
            Card(suit, value) for suit in range(4) for value in range(13)
        ]

    def shuffle(self):
        r = random.SystemRandom()
        r.shuffle(self.cards_remaining)

    def deal(self, num_cards):
        drawn = self.cards_remaining[:num_cards]
        del self.cards_remaining[:num_cards]
        return drawn

    def cards_remaining(self):
        return self.cards_remaining

    def cards_dealt(self):
        pass
