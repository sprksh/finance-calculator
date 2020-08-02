from src.finance_calculator.calculators.ratio_calculator import FinanceCalculator
from.test_data import *


def test_volatility():
    f = FinanceCalculator(scheme_data)
    volatility = f.get_volatility()
    return volatility


def test_beta():
    f = FinanceCalculator(scheme_data)
    f.get_beta()


def test_sharpe():
    f = FinanceCalculator(benchmark_data)
    df = f.get_sharpe()
    return df
