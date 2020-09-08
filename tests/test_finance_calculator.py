
from src.finance_calculator.calculators.ratio_calculator import FinanceCalculator
from src.finance_calculator.cli import main
from tests.test_nav_data import scheme_data, benchmark_data

f = FinanceCalculator(scheme_data, benchmark_data)


def test_treynor():
    df = f.get_treynor()
    assert df is not None


def test_alpha():
    df = f.get_alpha()
    assert df is not None


def test_beta():
    df = f.get_beta()
    assert df is not None


def test_upside_capture():
    df = f.get_upside_capture()
    assert df is not None


def test_downside_capture():
    df = f.get_downside_capture()
    assert df is not None


def test_drawdown():
    df = f.get_drawdown()
    assert df is not None


def test_volatility():
    df = f.get_volatility()
    assert df is not None


def test_sharpe():
    df = f.get_sharpe()
    assert df is not None


def test_sortino():
    df = f.get_sortino()
    assert df is not None


def test_main():
    assert main([]) == 0
