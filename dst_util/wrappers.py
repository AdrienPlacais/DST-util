"""Define wrapper functions that call proper funcs at proper time."""

from pathlib import Path
from typing import Any

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


def wrapper_distrib(
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


def wrapper_acceptance(
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
