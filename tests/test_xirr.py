import datetime

from src.finance_calculator.calculators.portfolio_calculator import XIRR


cashflow_data = [
    (datetime.date(2020, 3, 1), 10000),
    (datetime.date(2020, 4, 1), 10000),
    (datetime.date(2020, 5, 1), 10000),
    (datetime.date(2020, 6, 1), 10000),
    (datetime.date(2020, 7, 1), 10000),
    (datetime.date(2020, 8, 1), -60000),
]


# def test_xirr_xnpv():
#     cc = np.array([c for c in cashflow_data])
#     x = xirr(cc)
#     assert x is not None


def test_xirr_crude():
    x = XIRR(cashflow_data).get_xirr()
    assert x is not None
