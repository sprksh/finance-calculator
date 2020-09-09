=====
Usage
=====

To use finance_calculator in a project::

	import finance_calculator as fc


.. code-block:: python

    df = fc.get_treynor(scheme_data, benchmark_data, 250, 22)
    df = fc.get_alpha(scheme_data, benchmark_data, 250, 22)
    df = fc.get_beta(scheme_data, benchmark_data, 250, 22)
    df = fc.get_upside_capture(scheme_data, benchmark_data, 250, 22)
    df = fc.get_downside_capture(scheme_data, benchmark_data, 250, 22)
    df = fc.get_drawdown(scheme_data, 250, 22)
    df = fc.get_volatility(scheme_data, 250, 22)
    df = fc.get_sharpe(scheme_data, 250, 22)
    df = fc.get_sortino(scheme_data, 250, 22)


If you want only current value of a given ratio, you can use ``tail=True`` as a keyword argument in all of these functions.

The scheme data and the benchmark data can either be a pandas dataframe or list of tuples: (date, nav).

Also you can use it to calculate xirr:

.. code-block:: python

    >>> import finance_calculator as fc
    >>> cashflow_data = [
        (datetime.date(2020, 3, 1), 10000),
        (datetime.date(2020, 4, 1), 10000),
        (datetime.date(2020, 5, 1), 10000),
        (datetime.date(2020, 6, 1), 10000),
        (datetime.date(2020, 7, 1), 10000),
        (datetime.date(2020, 8, 1), -60000),
    ]
    >>> xirr = fc.get_xirr(cashflow_data)
