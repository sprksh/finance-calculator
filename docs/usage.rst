=====
Usage
=====

To use finance_calculator in a project::

    >>> import finance_calculator as fc

    >>> drawdown = fc.get_drawdown(scheme_data)
    >>> volatility = fc.get_volatility(scheme_data)
    >>> sharpe = fc.get_sharpe(scheme_data, benchmark_data)
    >>> sortino = fc.get_sortino(scheme_data, benchmark_data)
    >>> treynor = fc.get_treynor(scheme_data, benchmark_data)
    >>> alpha = fc.get_alpha(scheme_data, benchmark_data)
    >>> beta = fc.get_beta(scheme_data, benchmark_data)
    >>> upside_capture = fc.get_upside_capture(scheme_data, benchmark_data)
    >>> downside_capture = fc.get_downside_capture(scheme_data, benchmark_data)

If you want only current value of a given ratio, you can use ``tail=True`` as a keyword argument
in all of these functions. With ``tail=False`` it will give a pandas dataframe with values in a
rolling window fashion.

By default it is assumed that data is for 250 days of a year. Also rolling window is taken
to be 3 years by default. It can be used
as ``fc.get_sharpe(scheme_data, benchmark_data, window=500, annualiser=250)`` for
2 years rolling data. Annualiser is meant for annualising the values. If your data contains 365 days in a year
you should pass ``annualiser=365``. Normally, if it contains only working days, it will
by default take ``annualiser=250``.

Instead of benchmark_nav_data, an annual value of risk_free_rate can be given.
The calculator can use it in place of benchmark_nav_data. Internally, it will create
a benchmark nav df from the risk_free_rate.
The value can passed as ``fc.get_sharpe(scheme_data, risk_free_rate=0.05)`` for 5% of
annual risk free returns.

Also, if multiple out of these are needed for one set of data only, you can get
a ratio calculator instance and call the functions on that::

    >>> import finance_calculator as fc
    >>> rc = fc.get_ratio_calculator(nav_data, benchmark_nav_data)
    >>> beta_df = rc.get_beta(window=250*3)
    >>> alpha_df = rc.get_alpha(window=250*3)
    # similarly other ratios can be called
    # window needs to be passed for rolling window period in calculations.


This ensures that pre-processing is reduced for the data thus improving the performance.

The scheme data and the benchmark data can either be a pandas dataframe or list of tuples: (date, nav).

Also you can use it to calculate xirr::


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
