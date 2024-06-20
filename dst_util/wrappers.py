"""Define wrapper functions that call proper funcs at proper time."""

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from dst_util.acceptance import plot_same_acceptance_four_times
from dst_util.distribution import plot_all_distributions
from dst_util.dst_helper import (
    is_binary,
    read,
    save_all_acceptances,
    save_all_distributions,
    save_figure,
)


def plot_distribution(
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
    _wrapper_distrib(
        filepath_density,
        plot_single_kwargs,
        fig,
        axes,
        bins=bins,
        save_hist_data=save_hist_data,
    )


def _wrapper_distrib(
    filepath: Path,
    plot_single_kwargs: dict,
    fig: Figure,
    axes: Axes,
    bins: int = 500,
    save_hist_data: bool = True,
) -> Any:
    """Plot x-x', y-y', phi-W and x-y phase space distributions."""
    if is_binary(filepath):
        raise NotImplementedError
    data = read(filepath)

    hist_data = plot_all_distributions(data, plot_single_kwargs, axes, bins=bins)

    save_figure(fig, filepath)
    if save_hist_data:
        save_all_distributions(hist_data, plot_single_kwargs.keys(), filepath)
    return hist_data


def plot_acceptance(
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
    _wrapper_acceptance(
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
    _wrapper_distrib(
        filepath_density,
        plot_single_kwargs,
        fig,
        axes,
        bins=bins,
        save_hist_data=save_hist_data,
    )


def _wrapper_acceptance(
    filepath: Path,
    plot_single_kwargs: dict,
    fig: Figure,
    axes: Axes,
    bins: int = 500,
    save_hist_data: bool = True,
) -> Any:
    """Plot acceptance in x-x', y-y', phi-W and x-y phase spaces."""
    if is_binary(filepath):
        raise NotImplementedError

    data = read(filepath)
    acceptance_data = plot_same_acceptance_four_times(
        data, plot_single_kwargs, axes, bins=bins
    )

    save_figure(fig, filepath)
    if save_hist_data:
        save_all_acceptances(acceptance_data, plot_single_kwargs.keys(), filepath)

    return acceptance_data
