from setuptools import find_packages, setup

setup(
    name="dst_util",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["matplotlib", "numpy", "pandas", "setuptools"],
    entry_points={
        "console_scripts": [
            "plot_acceptance-cli=cli.plot_acceptance:main",
            "plot_distribution-cli=cli.plot_distribution:main",
            "dst_util-gui=gui.gui:main",
        ],
    },
    author="Adrien Plaçais",
    description="A set of tools to manipulate TraceWin .dst files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",  # Update as needed
)
