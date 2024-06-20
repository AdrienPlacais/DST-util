#!/usr/bin/env python3
"""Provide a frontend for CLI."""
import argparse
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from acceptance import plot_same_acceptance_four_times
from distribution import plot_all_distributions
from dst_helper import (
    is_binary,
    read,
    save_all_acceptances,
    save_all_distributions,
    save_figure,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure

if __name__ == "__main__":
    accept = Path(
        "/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/nominal_accepted.txt"
    )
    density = Path(
        "/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/part_rfq1.txt"
    )
    plot(filepath_density=density, filepath_acceptance=accept)
    # parser = argparse.ArgumentParser("prepare_distribution_file")
    # parser.add_argument(
    #     "-d",
    #     "--density",
    #     help="ASCII file holding distribution. Generally part_dtl1.txt or part_rfq.txt.",
    #     type=str,
    #     required=False,
    #     default=None,
    # )
    # parser.add_argument(
    #     "-a",
    #     "--acceptance",
    #     help="ASCII file holding acceptance. Not generated automatically by TraceWin, cf doc.",
    #     type=str,
    #     required=False,
    #     default=None,
    # )
    # parser.add_argument(
    #     "-b",
    #     "--bins",
    #     help="Number of bins for the figure and files.",
    #     type=int,
    #     required=False,
    #     default=500,
    # )
    # args = parser.parse_args()
    # hist_data = plot(
    #     Path(args.density) if args.density is not None else None,
    #     Path(args.acceptance) if args.acceptance is not None else None,
    #     args.bins,
    # )
