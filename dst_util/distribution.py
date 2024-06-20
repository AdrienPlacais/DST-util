"""Define several functions to plot and format distribution files."""

import math
from collections.abc import Collection
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import Colormap, Normalize
from matplotlib.figure import Figure


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


def _save_single_distribution(
    filepath: Path,
    hist: np.ndarray,
    xedges: np.ndarray,
    yedges: np.ndarray,
) -> None:
    """Save the histogram data in a format easy to understand for pgf."""
    data = []
    for i in range(len(xedges) - 1):
        for j in range(len(yedges) - 1):
            data.append([xedges[i], yedges[j], hist[i, j], math.log10(hist[i, j])])

    df = pd.DataFrame(data, columns=("x", "y", "z", "zlog"))
    df.to_csv(filepath, index=False, na_rep="nan", sep=" ")
    print(f"Saved dataframe in {filepath = }")


def save_all_distributions(
    all_data: Collection[tuple[np.ndarray, np.ndarray, np.ndarray]],
    all_columns: Collection[Collection[str]],
    fig: Figure,
    original_filepath: Path,
) -> None:
    """Save distribution for pgfplots and figures."""
    for data, columns in zip(all_data, all_columns):
        name = original_filepath.stem + "_" + "_".join(columns).replace(" ", "_")
        filepath = original_filepath.with_stem(name).with_suffix(".csv")
        _save_single_distribution(filepath, *data)
    fig.savefig(original_filepath.with_suffix(".png"))
