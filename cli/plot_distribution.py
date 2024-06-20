#!/usr/bin/env python3
"""Provide a CLI to plot distribution."""
import argparse
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from dst_util.wrappers import wrapper_distrib


def plot(
    filepath_density: Path,
    bins: int = 500,
    save_hist_data: bool = False,
    plot_single_kwargs: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> Any:
    """Plot density and/or acceptance on the same figure."""
    fig, axes = plt.subplots(nrows=2, ncols=2)

    if plot_single_kwargs is None:
        plot_single_kwargs = {
            ("x(mm)", "x'(mrad)"): {"xlim": (-40.0, 40.0), "ylim": (-25.0, 25.0)},
            ("y(mm)", "y'(mrad)"): {"xlim": (-40.0, 40.0), "ylim": (-25.0, 25.0)},
            ("Phase(deg)", "Energy(MeV)"): {
                "xlim": (-15, 15),
                "ylim": (98, 100.5),
                "range": "as_plot_limits",
            },
            ("x(mm)", "y(mm)"): {"xlim": (-40.0, 40.0), "ylim": (-40.0, 40.0)},
        }
    wrapper_distrib(
        filepath_density, plot_single_kwargs, fig, axes, bins=bins, save=save_hist_data
    )


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
    plot(Path(args.density), args.bins, args.save)


if __name__ == "__main__":
    main()
