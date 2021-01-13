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

A collectio

* Free software: MIT license

Installation
============

::

    pip install droneresponse-mathtools

You can also install the in-development version with::

    pip install https://github.com/DroneResponse/python-droneresponse-mathtools/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import droneresponse_mathtools
    droneresponse_mathtools.longest()


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
A complete development environment isn't necessary unless for most people. This setup lets

To set up a complete development environment on Ubuntu, install python3.6, python3.7, python3.8, python3.9
::

    sudo apt update
    sudo apt install --yes software-properties-common python3
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install --yes python3.6 python3.7 python3.9

Also install pypy3.7. by downloading the lastest version from
<https://www.pypy.org/download.html>
Then extract it and add it's executables to your ``PATH`` variable.

