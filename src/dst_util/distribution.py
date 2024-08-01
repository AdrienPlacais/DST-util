"""Define several functions to plot and format distribution files."""

from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import Colormap, Normalize


def plot_all_distributions(
    data: pd.DataFrame,
    plot_single_kwargs: dict[tuple[str, str], dict[str, Any]],
    axes: Any,
    bins: int,
) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Plot all the desired distributions."""
    hist_data = [
        _plot_single_distribution(axis, data, columns, bins=bins, **kwargs)
        for axis, columns, kwargs in zip(
            axes.flatten(),
            plot_single_kwargs.keys(),
            plot_single_kwargs.values(),
            strict=True,
        )
    ]
    return hist_data


def _plot_single_distribution(
    axis: Axes,
    data: pd.DataFrame,
    columns: tuple[str, str],
    bins: int = 500,
    cmap: Colormap = plt.colormaps["rainbow"],
    grid: bool = True,
    cmin: float | None = 1.0,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    norm: Normalize | str = "log",
    range: (
        tuple[tuple[float, float], tuple[float, float]]
        | Literal["as_plot_limits"]
        | None
    ) = None,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Plot the distribution specified by ``columns``."""
    x = data[columns[0]]
    y = data[columns[1]]

    if range == "as_plot_limits":
        assert xlim is not None
        assert ylim is not None
        range = (xlim, ylim)
    h, xedges, yedges, image = axis.hist2d(
        x, y, bins=bins, cmin=cmin, cmap=cmap, norm=norm, range=range, **kwargs
    )
    title = " - ".join(columns)
    axis.set_title(title)
    if grid:
        plt.grid()
    if xlim:
        axis.set_xlim(xlim)
    if ylim:
        axis.set_ylim(ylim)
    return h, xedges, yedges
