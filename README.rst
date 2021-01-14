========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |
        |
    * - package
      - | |commits-since|

.. |commits-since| image:: https://img.shields.io/github/commits-since/DroneResponse/python-droneresponse-mathtools/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/DroneResponse/python-droneresponse-mathtools/compare/v0.0.0...master



.. end-badges

Math tools

* Free software: MIT license

Installation
============

::

    pip install https://github.com/DroneResponse/python-droneresponse-mathtools

You can also install the in-development version with::

    pip install https://github.com/DroneResponse/python-droneresponse-mathtools/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    from droneresponse_mathtools import Lla
    white_field = Lla(41.714911, -86.242250, 0)
    pendle_rd = white_field.move_ned(106, 0, 0)


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Development Setup
-----------------
A complete development environment isn't necessary most of the time.
This setup lets test with multiple python interpreters.
It also lets you use the pre-commit to automatically clean the source code before commits.

To set up a complete development environment on Ubuntu, install python3.6, python3.7, python3.8, python3.9, pip and venv.
::

    sudo apt update
    sudo apt install --yes software-properties-common python3 python3-pip python3-venv
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install --yes python3.6 python3.7 python3.9

Install ``flake8`` and ``pre-commit`` with
::

    pip install pre-commit flake8

Set up ``pre-commit``
::

    cd python-droneresponse-mathtools
    pre-commit install

Set up ``bumpversion``
::

    pip install bumpversion
