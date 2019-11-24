# -*- coding: utf-8 -*-
"""Console script for robo_croupier."""
import argparse
import sys


def main():
    """Console script for robo_croupier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into " "robo_croupier.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
