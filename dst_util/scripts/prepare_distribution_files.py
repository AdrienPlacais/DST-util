#!/usr/bin/env python3
"""Provide a frontend for CLI."""
import argparse
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from acceptance_helper import plot_same_acceptance_four_times
from distribution_helper import plot_all_distributions
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from util import (
    is_binary,
    read,
    save_all_acceptances,
    save_all_distributions,
    save_figure,
)


def plot(
    filepath_density: Path | None = None,
    filepath_acceptance: Path | None = None,
    bins: int = 500,
    save: bool = True,
) -> Any:
    """Plot density and/or acceptance on the same figure."""
    fig, axes = plt.subplots(nrows=2, ncols=2)
    plot_single_kwargs = {
        ("Phase(deg)", "Energy(MeV)"): {
            # "xlim": (-15, 15),
            # "ylim": (98, 100.5),
            "xlim": (-30, 30),
            "ylim": (14, 19),
            "range": "as_plot_limits",
        },
    }
    if filepath_acceptance is not None:
        _wrapper_acceptance(
            filepath_acceptance, plot_single_kwargs, fig, axes, bins=200, save=save
        )
    plot_single_kwargs = {
        ("x(mm)", "x'(mrad)"): {"xlim": (-40.0, 40.0), "ylim": (-25.0, 25.0)},
        ("y(mm)", "y'(mrad)"): {"xlim": (-40.0, 40.0), "ylim": (-25.0, 25.0)},
        ("Phase(deg)", "Energy(MeV)"): {
            # "xlim": (-15, 15),
            # "ylim": (98, 100.5),
            "xlim": (-30, 30),
            "ylim": (14, 19),
            "range": "as_plot_limits",
        },
        ("x(mm)", "y(mm)"): {"xlim": (-40.0, 40.0), "ylim": (-40.0, 40.0)},
    }
    if filepath_density is not None:
        _wrapper_distrib(
            filepath_density, plot_single_kwargs, fig, axes, bins=bins, save=save
        )


def _wrapper_distrib(
    filepath: Path,
    plot_single_kwargs: dict,
    fig: Figure,
    axes: Axes,
    bins: int = 500,
    save: bool = True,
):
    """Plot x-x', y-y', phi-W and x-y phase space distributions."""
    if is_binary(filepath):
        raise NotImplementedError
    data = read(filepath)

    hist_data = plot_all_distributions(data, plot_single_kwargs, axes, bins=bins)

    if save:
        save_all_distributions(hist_data, plot_single_kwargs.keys(), filepath)
        save_figure(fig, filepath)
    return hist_data


def _wrapper_acceptance(
    filepath: Path,
    plot_single_kwargs: dict,
    fig: Figure,
    axes: Axes,
    bins: int = 500,
    save: bool = True,
) -> Any:
    """Plot acceptance in x-x', y-y', phi-W and x-y phase spaces."""
    if is_binary(filepath):
        raise NotImplementedError

    data = read(filepath)
    acceptance_data = plot_same_acceptance_four_times(
        data, plot_single_kwargs, axes, bins=bins
    )

    if save:
        save_all_acceptances(acceptance_data, plot_single_kwargs.keys(), filepath)
        save_figure(fig, filepath)

    return acceptance_data


if __name__ == "__main__":
    accept = Path(
        "/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/nominal_accepted.txt"
    )
    density=Path(
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
