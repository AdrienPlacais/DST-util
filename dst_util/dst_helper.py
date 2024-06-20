from collections.abc import Collection
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure


def is_binary(filepath: Path) -> bool:
    """Determine if extension corresponds to a binary file."""
    extension = filepath.suffix
    if extension == ".txt":
        return False
    if extension == ".dst":
        return True
    raise ValueError(f"{extension = } not understood in {filepath = }")


def read(filepath: Path) -> pd.DataFrame:
    """Read the given file."""
    with open(filepath, "r") as f:
        data = pd.read_csv(f, skiprows=2, sep=r"\s+")
    return data


def save_all_distributions(
    all_data: Collection[tuple[np.ndarray, np.ndarray, np.ndarray]],
    all_columns: Collection[Collection[str]],
    original_filepath: Path,
) -> None:
    """Save distribution for pgfplots and figures."""
    for data, columns in zip(all_data, all_columns):
        name = original_filepath.stem + "_" + "_".join(columns).replace(" ", "_")
        filepath = original_filepath.with_stem(name).with_suffix(".csv")
        _save_single_hist(filepath, *data, add_log_column=True)


def save_all_acceptances(
    all_data: Collection[tuple[np.ndarray, np.ndarray, np.ndarray]],
    all_columns: Collection[Collection[str]],
    original_filepath: Path,
) -> None:
    """Save distribution for pgfplots and figures."""
    for data, columns in zip(all_data, all_columns):
        name = (
            original_filepath.stem
            + "_acceptance_"
            + "_".join(columns).replace(" ", "_")
        )
        filepath = original_filepath.with_stem(name).with_suffix(".csv")
        _save_single_hist(filepath, *data, add_log_column=False)


def save_figure(fig: Figure, filepath: Path, acceptance: bool = False) -> None:
    """Save the given figure."""
    out = filepath.with_suffix(".png")
    if acceptance:
        out = filepath.with_suffix(".acceptance.png")
    fig.savefig(out)
    print(f"Saved figure in {filepath = }")


def _save_single_hist(
    filepath: Path,
    hist: np.ndarray,
    xedges: np.ndarray,
    yedges: np.ndarray,
    add_log_column: bool = True,
) -> None:
    """Save the histogram data in a format easy to understand for pgf."""
    data = []
    for i in range(len(xedges) - 1):
        for j in range(len(yedges) - 1):
            data.append([xedges[i], yedges[j], hist[i, j]])

    df = pd.DataFrame(data, columns=("x", "y", "z"))
    if add_log_column:
        df["zlog"] = np.log10(df["z"])

    df.to_csv(filepath, index=False, na_rep="nan", sep=" ")
    print(f"Saved dataframe in {filepath = }")
