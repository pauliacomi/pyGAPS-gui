# pyGAPS-gui - adsorption data processing

## Overview

pyGAPS-GUI is a Graphical User Interface (GUI) for
[pyGAPS](https://github.com/pauliacomi/pyGAPS). It can be used to import,
process and fit adsorption isotherms in various formats.

Download the latest version for your system in the
[releases](https://github.com/pauliacomi/pyGAPS-gui/releases) section.

****

pyGAPS-gui is currently **alpha** software. Things may break and change without
warning. You have been warned.

****

## Features

- Advanced adsorption data import and manipulation.
- Routine analysis such as BET/Langmuir surface area, t-plot, alpha-s, Dubinin plots etc.
- Pore size distribution calculations for mesopores (BJH, Dollimore-Heal).
- Pore size distribution calculations for micropores (Horvath-Kawazoe).
- Pore size distribution calculations using DFT kernels
- Isotherm model fitting (Henry, Langmuir, DS/TS Langmuir, etc..)
- Isosteric enthalpy of adsorption calculation.
- IAST calculations for binary and multicomponent adsorption.
- Parsing to and from multiple formats such as Excel, CSV and JSON.
- An sqlite database backend for storing and retrieving data.
- Simple methods for isotherm graphing and comparison.

## Installation for development

To install the development version of pyGAPS-GUI, pull this GitHub repo

    git clone https://github.com/pauliacomi/pyGAPS-gui

Setup a virtual environment in which pyGAPS is installed. Also install a version
of qtpy with PyQt5/PyQt4/PySide2/PySide6. Then run the main app:

    python pyGAPS-gui.py

