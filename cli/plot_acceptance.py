#!/usr/bin/env python3
"""Provide a CLI to plot acceptance (you can add density)."""
import argparse
from pathlib import Path

from dst_util.wrappers import plot_acceptance


def main():
    """Define function called when script is run."""
    parser = argparse.ArgumentParser("plot_acceptance")
    parser.add_argument(
        "-a",
        "--acceptance",
        help="ASCII file holding acceptance. Not generated automatically by TraceWin, cf doc.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--density",
        help="ASCII file holding input distribution. Generally part_rfq.txt.",
        type=str,
        required=False,
        default=None,
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
    plot_acceptance(
        Path(args.acceptance),
        Path(args.density) if args.density is not None else None,
        args.bins,
        args.save,
    )


if __name__ == "__main__":
    main()
