#!/usr/bin/env python3
"""Provide a CLI to plot distribution."""
import argparse
from pathlib import Path

from dst_util.wrappers import plot_distribution


def main():
    """Define function called when script is run."""
    parser = argparse.ArgumentParser("plot_distribution")
    parser.add_argument(
        "-d",
        "--density",
        help="ASCII file holding input distribution. Generally part_rfq.txt.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-b",
        "--bins",
        help="Number of bins for the figure and files.",
        type=int,
        required=False,
        default=500,
    )
    parser.add_argument(
        "-s",
        "--save",
        help="Flag to ask for saving of hist data.",
        action="store_false",
    )
    args = parser.parse_args()
    plot_distribution(Path(args.density), args.bins, args.save)


if __name__ == "__main__":
    main()
