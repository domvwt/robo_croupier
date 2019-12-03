# -*- coding: utf-8 -*-
"""Main module."""
from robo_croupier.ginrummy import GinRummy


def main() -> None:
    game = GinRummy()
    game.setup_actions()
    pass


if __name__ == "__main__":
    main()
