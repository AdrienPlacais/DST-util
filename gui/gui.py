#!/usr/bin/env python3
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt

from dst_util.wrappers import plot_acceptance, plot_distribution


class DSTUtilApp(tk.Tk):
    """Hold the tkinter window."""

    def __init__(self) -> None:
        """Instantiate object."""
        super().__init__()

        self.title("DST Util GUI")
        self.geometry("1200x800")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.create_acceptance_tab()
        self.create_distribution_tab()

    def create_acceptance_tab(self) -> None:
        """Define the first tab, to plot acceptances."""
        acceptance_frame = ttk.Frame(self.notebook)
        self.notebook.add(acceptance_frame, text="Acceptance")

        # Filepath acceptance (mandatory)
        self.filepath_acceptance = tk.StringVar(
            value="/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/failed_14/accepted.txt"
        )
        file_acceptance_label = ttk.Label(
            acceptance_frame, text="Filepath Acceptance:"
        )
        file_acceptance_label.grid(row=0, column=0, padx=10, pady=10)
        file_acceptance_entry = ttk.Entry(
            acceptance_frame, textvariable=self.filepath_acceptance, width=40
        )
        file_acceptance_entry.grid(row=0, column=1, padx=10, pady=10)
        file_acceptance_button = ttk.Button(
            acceptance_frame,
            text="Browse",
            command=lambda: self.browse_file(self.filepath_acceptance),
        )
        file_acceptance_button.grid(row=0, column=2, padx=10, pady=10)

        # Filepath density (optional)
        self.filepath_density_acc = tk.StringVar(
            value="/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/in.txt"
        )
        file_density_label = ttk.Label(
            acceptance_frame, text="Filepath Density (optional):"
        )
        file_density_label.grid(row=1, column=0, padx=10, pady=10)
        file_density_entry = ttk.Entry(
            acceptance_frame, textvariable=self.filepath_density_acc, width=40
        )
        file_density_entry.grid(row=1, column=1, padx=10, pady=10)
        file_density_button = ttk.Button(
            acceptance_frame,
            text="Browse",
            command=lambda: self.browse_file(self.filepath_density_acc),
        )
        file_density_button.grid(row=1, column=2, padx=10, pady=10)

        # Bins acceptance
        self.bins_acceptance = tk.IntVar(value=200)
        bins_acceptance_label = ttk.Label(
            acceptance_frame, text="Bins Acceptance:"
        )
        bins_acceptance_label.grid(row=2, column=0, padx=10, pady=10)
        bins_acceptance_entry = ttk.Entry(
            acceptance_frame, textvariable=self.bins_acceptance, width=10
        )
        bins_acceptance_entry.grid(row=2, column=1, padx=10, pady=10)

        # Bins density
        self.bins_density = tk.IntVar(value=500)
        bins_density_label = ttk.Label(acceptance_frame, text="Bins Density:")
        bins_density_label.grid(row=3, column=0, padx=10, pady=10)
        bins_density_entry = ttk.Entry(
            acceptance_frame, textvariable=self.bins_density, width=10
        )
        bins_density_entry.grid(row=3, column=1, padx=10, pady=10)

        # Save histogram data checkbox
        self.save_hist_data_acceptance = tk.BooleanVar(value=False)
        save_hist_checkbox_acceptance = ttk.Checkbutton(
            acceptance_frame,
            text="Save histogram data",
            variable=self.save_hist_data_acceptance,
        )
        save_hist_checkbox_acceptance.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10
        )

        # Invert acceptance colors checkbox
        self.invert_acceptance_colors = tk.BooleanVar(value=False)
        invert_colors_checkbox = ttk.Checkbutton(
            acceptance_frame,
            text="Invert acceptance colors",
            variable=self.invert_acceptance_colors,
        )
        invert_colors_checkbox.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10
        )

        # Plot kwargs (xlim and ylim for subplots)
        self.plot_kwargs_acceptance = {
            ("x(mm)", "x'(mrad)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-25.0, 25.0"),
                "additional": tk.StringVar(value=""),
            },
            ("y(mm)", "y'(mrad)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-25.0, 25.0"),
                "additional": tk.StringVar(value=""),
            },
            ("Phase(deg)", "Energy(MeV)"): {
                "xlim": tk.StringVar(value="-20, 20"),
                "ylim": tk.StringVar(value="16, 17"),
                "additional": tk.StringVar(value="range='as_plot_limits'"),
            },
            ("x(mm)", "y(mm)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-40.0, 40.0"),
                "additional": tk.StringVar(value=""),
            },
        }

        row_offset = 6
        for i, ((x_label, y_label), kwargs) in enumerate(
            self.plot_kwargs_acceptance.items()
        ):
            label_frame = ttk.LabelFrame(
                acceptance_frame, text=f"{x_label} vs {y_label}"
            )
            label_frame.grid(
                row=row_offset + i,
                column=0,
                columnspan=3,
                padx=10,
                pady=5,
                sticky="ew",
            )

            xlim_label = ttk.Label(label_frame, text="xlim:")
            xlim_label.grid(row=0, column=0, padx=5, pady=5)
            xlim_entry = ttk.Entry(
                label_frame, textvariable=kwargs["xlim"], width=20
            )
            xlim_entry.grid(row=0, column=1, padx=5, pady=5)

            ylim_label = ttk.Label(label_frame, text="ylim:")
            ylim_label.grid(row=0, column=2, padx=5, pady=5)
            ylim_entry = ttk.Entry(
                label_frame, textvariable=kwargs["ylim"], width=20
            )
            ylim_entry.grid(row=0, column=3, padx=5, pady=5)

            additional_kwargs_label = ttk.Label(
                label_frame, text="Additional kwargs (key=value):"
            )
            additional_kwargs_label.grid(row=1, column=0, padx=5, pady=5)
            additional_kwargs_entry = ttk.Entry(
                label_frame, textvariable=kwargs["additional"], width=40
            )
            additional_kwargs_entry.grid(
                row=1, column=1, columnspan=3, padx=5, pady=5
            )

        # Plot button
        plot_button = ttk.Button(
            acceptance_frame, text="Plot", command=self.plot_acceptance
        )
        plot_button.grid(
            row=row_offset + len(self.plot_kwargs_acceptance) + 1,
            column=0,
            columnspan=3,
            padx=10,
            pady=10,
        )

    def create_distribution_tab(self) -> None:
        """Create the second tab."""
        distribution_frame = ttk.Frame(self.notebook)
        self.notebook.add(distribution_frame, text="Distribution")

        # File selection
        self.filepath_density = tk.StringVar(
            value="/home/placais/Documents/Conferences/2024.08_LINAC2024/presentation/data/dtl_minerva/failed_14/out.txt"
        )
        file_label = ttk.Label(distribution_frame, text="File to plot:")
        file_label.grid(row=0, column=0, padx=10, pady=10)
        file_entry = ttk.Entry(
            distribution_frame, textvariable=self.filepath_density, width=40
        )
        file_entry.grid(row=0, column=1, padx=10, pady=10)
        file_button = ttk.Button(
            distribution_frame,
            text="Browse",
            command=lambda: self.browse_file(self.filepath_density),
        )
        file_button.grid(row=0, column=2, padx=10, pady=10)

        # Number of bins
        self.bins = tk.IntVar(value=500)
        bins_label = ttk.Label(distribution_frame, text="Number of bins:")
        bins_label.grid(row=1, column=0, padx=10, pady=10)
        bins_entry = ttk.Entry(
            distribution_frame, textvariable=self.bins, width=10
        )
        bins_entry.grid(row=1, column=1, padx=10, pady=10)

        # Save histogram data
        self.save_hist_data = tk.BooleanVar(value=False)
        save_hist_checkbox = ttk.Checkbutton(
            distribution_frame,
            text="Save histogram data",
            variable=self.save_hist_data,
        )
        save_hist_checkbox.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10
        )

        # Plot kwargs (xlim and ylim for subplots)
        self.plot_kwargs = {
            ("x(mm)", "x'(mrad)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-25.0, 25.0"),
                "additional": tk.StringVar(value=""),
            },
            ("y(mm)", "y'(mrad)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-25.0, 25.0"),
                "additional": tk.StringVar(value=""),
            },
            ("Phase(deg)", "Energy(MeV)"): {
                "xlim": tk.StringVar(value="-15, 15"),
                "ylim": tk.StringVar(value="98, 100.5"),
                "additional": tk.StringVar(value="range='as_plot_limits'"),
            },
            ("x(mm)", "y(mm)"): {
                "xlim": tk.StringVar(value="-40.0, 40.0"),
                "ylim": tk.StringVar(value="-40.0, 40.0"),
                "additional": tk.StringVar(value=""),
            },
        }

        row_offset = 3
        for i, ((x_label, y_label), kwargs) in enumerate(
            self.plot_kwargs.items()
        ):
            label_frame = ttk.LabelFrame(
                distribution_frame, text=f"{x_label} vs {y_label}"
            )
            label_frame.grid(
                row=row_offset + i,
                column=0,
                columnspan=3,
                padx=10,
                pady=5,
                sticky="ew",
            )

            xlim_label = ttk.Label(label_frame, text="xlim:")
            xlim_label.grid(row=0, column=0, padx=5, pady=5)
            xlim_entry = ttk.Entry(
                label_frame, textvariable=kwargs["xlim"], width=20
            )
            xlim_entry.grid(row=0, column=1, padx=5, pady=5)

            ylim_label = ttk.Label(label_frame, text="ylim:")
            ylim_label.grid(row=0, column=2, padx=5, pady=5)
            ylim_entry = ttk.Entry(
                label_frame, textvariable=kwargs["ylim"], width=20
            )
            ylim_entry.grid(row=0, column=3, padx=5, pady=5)

            additional_kwargs_label = ttk.Label(
                label_frame, text="Additional kwargs (key=value):"
            )
            additional_kwargs_label.grid(row=1, column=0, padx=5, pady=5)
            additional_kwargs_entry = ttk.Entry(
                label_frame, textvariable=kwargs["additional"], width=40
            )
            additional_kwargs_entry.grid(
                row=1, column=1, columnspan=3, padx=5, pady=5
            )

        # Plot button
        plot_button = ttk.Button(
            distribution_frame, text="Plot", command=self.plot_distribution
        )
        plot_button.grid(
            row=row_offset + len(self.plot_kwargs) + 1,
            column=0,
            columnspan=3,
            padx=10,
            pady=10,
        )

    def browse_file(self, path_var) -> None:
        """Open the filedialog and set the ``path_var``."""
        file_path = filedialog.askopenfilename()
        if file_path:
            path_var.set(file_path)

    def plot_distribution(self) -> None:
        """Plot the density."""
        filepath_density = self.filepath_density.get()
        bins = self.bins.get()
        save_hist_data = self.save_hist_data.get()

        plot_single_kwargs = {}

        for (x_label, y_label), kwargs in self.plot_kwargs.items():
            plot_kwargs_entry = {
                "xlim": tuple(map(float, kwargs["xlim"].get().split(","))),
                "ylim": tuple(map(float, kwargs["ylim"].get().split(","))),
            }
            # Parse additional kwargs for each subplot
            additional_kwargs = kwargs["additional"].get()
            if additional_kwargs:
                for kwarg in additional_kwargs.split(","):
                    key, value = kwarg.split("=")
                    plot_kwargs_entry[key.strip()] = eval(value.strip())

            plot_single_kwargs[(x_label, y_label)] = plot_kwargs_entry

        if not filepath_density:
            messagebox.showerror("Error", "Please select a file to plot.")
            return

        try:
            plot_distribution(
                filepath_density=Path(filepath_density),
                bins=bins,
                save_hist_data=save_hist_data,
                plot_single_kwargs=plot_single_kwargs,
            )
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_acceptance(self) -> None:
        """Plot the acceptance."""
        filepath_acceptance = Path(self.filepath_acceptance.get())
        filepath_density = (
            Path(self.filepath_density_acc.get())
            if self.filepath_density_acc.get()
            else None
        )
        bins_acceptance = self.bins_acceptance.get()
        bins_density = self.bins_density.get()

        save_hist_data = self.save_hist_data.get()
        invert_acceptance_colors = self.invert_acceptance_colors.get()

        # Parse plot_single_kwargs
        plot_single_kwargs = {}
        for (x_label, y_label), kwargs in self.plot_kwargs_acceptance.items():
            plot_kwargs_entry = {
                "xlim": tuple(map(float, kwargs["xlim"].get().split(","))),
                "ylim": tuple(map(float, kwargs["ylim"].get().split(","))),
            }
            # Parse additional kwargs for each subplot
            additional_kwargs = kwargs["additional"].get()
            if additional_kwargs:
                for kwarg in additional_kwargs.split(","):
                    key, value = kwarg.split("=")
                    plot_kwargs_entry[key.strip()] = eval(value.strip())

            plot_single_kwargs[(x_label, y_label)] = plot_kwargs_entry

        if not filepath_acceptance:
            messagebox.showerror(
                "Error", "Please select a file for acceptance."
            )
            return

        try:
            # Call the appropriate plotting function from your acceptance module
            # Replace `plot_acceptance` with the actual function name if different
            plot_acceptance(
                filepath_acceptance,
                filepath_density=filepath_density,
                bins_acceptance=bins_acceptance,
                bins_density=bins_density,
                plot_single_kwargs=plot_single_kwargs,
                save_hist_data=save_hist_data,
                invert_acceptance_colors=invert_acceptance_colors,
            )
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main() -> None:
    """Create the interactive window."""
    app = DSTUtilApp()
    app.mainloop()


if __name__ == "__main__":
    main()
