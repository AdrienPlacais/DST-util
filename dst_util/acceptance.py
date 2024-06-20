"""Define several functions to plot and format acceptance files."""

from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import Colormap, ListedColormap


def plot_same_acceptance_four_times(
    data: pd.DataFrame,
    plot_single_kwargs: dict[tuple[str, str], dict[str, Any]],
    axes: Any,
    bins: int,
) -> Any:
    """Plot all the desired acceptances."""
    columns = list(plot_single_kwargs.keys())[0]
    kwargs = list(plot_single_kwargs.values())[0]
    acceptance_data = [
        _plot_single_acceptance(axis, data, columns, bins=bins, **kwargs)
        for axis in axes.flatten()
    ]
    return acceptance_data


def _plot_single_acceptance(
    axis: Axes,
    data: pd.DataFrame,
    columns: tuple[str, str],
    bins: int = 500,
    cmap: Colormap = ListedColormap(["black", "white"]),
    grid: bool = True,
    cmin: float | None = 1.0,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    range: (
        tuple[tuple[float, float], tuple[float, float]]
        | Literal["as_plot_limits"]
        | None
    ) = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Plot the acceptance in phase-spaces specified by ``columns``."""
    x = data[columns[0]]
    y = data[columns[1]]

    if range == "as_plot_limits":
        assert xlim is not None
        assert ylim is not None
        range = (xlim, ylim)
    h, xedges, yedges = np.histogram2d(x, y, bins=bins, range=range)
    accepted_h = np.where(h > 0, 1, 0).T

    axis.pcolormesh(xedges, yedges, accepted_h, cmap=cmap, edgecolors="face")
    title = " - ".join(columns)
    axis.set_title(title)
    if grid:
        plt.grid()
    if xlim:
        axis.set_xlim(xlim)
    if ylim:
        axis.set_ylim(ylim)
    return accepted_h, xedges, yedges
