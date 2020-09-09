# flake8: noqa
from finance_calculator.calculators import api

__version__ = '0.0.1'


"""
xirr:
    input:
        cashflows with dates, (list of tuples)
        as_on_date: date
    returns:
        object:
            xirr (float)
            cashflow sum (float)
            current value (float)
xirr_movement:
    input:
        cashflows with dates, (list of tuples)
        checkpoint dates: (list)
    returns:
        list of objects:
            xirr with date (list of tuples)
            cashflow sum
            current value
volatility:
    input:
        nav with dates (list of tuples)
        period (from date, to date)
    returns:
        volatility (int)
sharpe:
    input:
        nav with dates (list of tuples)
        comparison nav with dates (list of tuples)
    returns:

beta:
    nav with dates
    comparison nav with dates
drawdown:
    nav with dates
capture:
    nav with dates
    comparison nav with dates

"""
