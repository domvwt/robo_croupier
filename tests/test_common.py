from robo_croupier.common import Deck


def test_deck():
    deck = Deck()
    assert len(deck.cards_remaining) == 52


def main():
    deck = Deck()
    print(deck.cards_remaining)


if __name__ == "__main__":
    main()
