import datetime

from finance_calculator import api as fc

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
    xirr = fc.get_xirr(cashflow_data)
    assert type(xirr) is float
