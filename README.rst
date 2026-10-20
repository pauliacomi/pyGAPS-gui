.. raw:: html

   <p align="center">
   <h1 align="center">
   <img alt="pyGAPS Logo" src="https://raw.githubusercontent.com/pauliacomi/pyGAPS-gui/master/docs/logo.svg" width="150px" />
   <h1 align="center">pyGAPS-gui</h1>
   </h1>
   </p>

========
Overview
========

pyGAPS-gui is a Graphical User Interface (GUI) for
`pyGAPS <https://github.com/pauliacomi/pyGAPS>`__. It can be used to
import, process and fit adsorption isotherms in various formats.

Download the latest version for your system in the
`releases <https://github.com/pauliacomi/pyGAPS-gui/releases>`__
section.

.. raw:: html

    <a style="text-decoration:none" href="https://github.com/pauliacomi/pyGAPS-gui/releases/latest/download/pyGAPS-gui.msi">
        <img src="https://img.shields.io/badge/download-windows-blue.svg" alt="Win link" />
    </a>
    <a style="text-decoration:none" href="https://github.com/pauliacomi/pyGAPS-gui/releases/latest/download/pyGAPS-gui-macos.zip">
        <img src="https://img.shields.io/badge/download-mac-lightgrey" alt="Mac link" />
    </a>
    <a style="text-decoration:none" href="https://github.com/pauliacomi/pyGAPS-gui/releases/latest/download/pyGAPS-gui-linux-x86_64.tar.gz">
        <img src="https://img.shields.io/badge/download-linux-orange" alt="Linux link" />
    </a>

--------------

pyGAPS-gui is currently **alpha** software. Things may break and change
without warning. You have been warned.

--------------

Features
========

-  Advanced adsorption data import and manipulation.
-  Routine analysis such as BET/Langmuir surface area, t-plot, alpha-s,
   Dubinin plots etc.
-  Pore size distribution calculations for mesopores (BJH,
   Dollimore-Heal).
-  Pore size distribution calculations for micropores (Horvath-Kawazoe).
-  Pore size distribution calculations using DFT kernels
-  Isotherm model fitting (Henry, Langmuir, DS/TS Langmuir, etc..)
-  Isosteric enthalpy of adsorption calculation.
-  IAST calculations for binary and multicomponent adsorption.
-  Parsing to and from multiple formats such as Excel, CSV and JSON.
-  An sqlite database backend for storing and retrieving data.
-  Simple methods for isotherm graphing and comparison.

.. figure:: docs/screenshot.png
   :alt: Screenshot


Installation for development
============================

To install the development version of pyGAPS-gui, pull this GitHub repo.

.. code:: bash

   git clone https://github.com/pauliacomi/pyGAPS-gui

Set up a virtual environment and install pyGAPS-gui. Python 3.8 is no longer
supported. CI targets Python 3.9 through 3.14; Python 3.14 is recommended for
development and is used to build release bundles. Python 3.9 is retained for
compatibility despite being end-of-life.

Using ``venv`` on Linux or macOS:

.. code:: bash

   cd pyGAPS-gui
   python -m venv ./.venv
   source ./.venv/bin/activate
   pip install .

Or using ``venv`` on Windows:

.. code:: pwsh

   cd pyGAPS-gui
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install .

Then run the app:

.. code:: bash

   pygapsgui
   # or
   python pyGAPS-gui.py
