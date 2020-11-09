========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/finance_calculator/badge/?style=flat
    :target: https://readthedocs.org/projects/finance_calculator
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/sprksh/finance_calculator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sprksh/finance_calculator

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/sprksh/finance_calculator?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/sprksh/finance_calculator

.. |codecov| image:: https://codecov.io/gh/sprksh/finance_calculator/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sprksh/finance-calculator

.. |requires| image:: https://requires.io/enterprise/sprksh/finance-calculator/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/enterprise/sprksh/finance-calculator/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/finance-calculator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/finance-calculator

.. |wheel| image:: https://img.shields.io/pypi/wheel/finance-calculator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/finance-calculator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/finance-calculator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/finance-calculator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/finance-calculator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/finance-calculator

.. |commits-since| image:: https://img.shields.io/github/commits-since/sprksh/finance_calculator/v0.0.5.svg
    :alt: Commits since latest release
    :target: https://github.com/sprksh/finance-calculator/compare/v0.0.5...master



.. end-badges

A simple python tool for calculating ratios used to measure portfolio performance.
Ratios include alpha, beta, sharpe, volatility, upside capture, downside capture, sortino ratio,
treynor ratio, drawdown etc.

It also can be used to calculating portfolio returns like XIRR. (twirr, holding period return etc. will be added).

The tool is largely based on pandas and numpy and is capable of giving continuous (rolling) values of ratios
wherever required in the form of a pandas dataframe. All data (portfolio/ navs/ market) needs to be passed in
arguments based on the function getting called.

For example
- XIRR can be calculated from portfolio cashflows [(date, amount)].
- Sharpe ratio will need scheme/portfolio nav [(date, nav)].
- Alpha will need both scheme nav as well as benchmark nav.


For definitions of above terms, check Investopedia. You can find the examples of
few of these ratios here. https://www.valueresearchonline.com/funds/197/sbi-large-and-midcap-fund

* Free software: BSD 2-Clause License

Installation
============

::

    pip install finance-calculator

You can also install the in-development version with::

    pip install https://github.com/sprksh/finance-calculator/archive/master.zip


Documentation
=============


https://finance-calculator.readthedocs.io/


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
