#!/usr/bin/env python3
"""Provide a CLI to plot acceptance (you can add density)."""
import argparse
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from dst_util.wrappers import wrapper_acceptance, wrapper_distrib


def plot(
    filepath_acceptance: Path,
    filepath_density: Path | None = None,
    bins: int = 500,
    save_hist_data: bool = False,
    plot_single_kwargs: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> Any:
    """Plot density and/or acceptance on the same figure."""
    fig, axes = plt.subplots(nrows=2, ncols=2)

    if plot_single_kwargs is None:
        plot_single_kwargs = {
            ("Phase(deg)", "Energy(MeV)"): {
                # "xlim": (-15, 15),
                # "ylim": (98, 100.5),
                "xlim": (-30, 30),
                "ylim": (14, 19),
                "range": "as_plot_limits",
            },
        }
    wrapper_acceptance(
        filepath_acceptance,
        plot_single_kwargs,
        fig,
        axes,
        bins=200,
        save_hist_data=save_hist_data,
    )
    if filepath_density is None:
        return
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
    wrapper_distrib(
        filepath_density,
        plot_single_kwargs,
        fig,
        axes,
        bins=bins,
        save_hist_data=save_hist_data,
    )


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
    plot(
        Path(args.acceptance),
        Path(args.density) if args.density is not None else None,
        args.bins,
        args.save,
    )


if __name__ == "__main__":
    main()
