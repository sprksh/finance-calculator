from src.finance_calculator.calculators import api as fc
from src.finance_calculator.cli import main
from tests.test_nav_data import scheme_data, benchmark_data


def test_treynor():
    df = fc.get_treynor(scheme_data, benchmark_data, 250, 22)
    assert df is not None


def test_alpha():
    df = fc.get_alpha(scheme_data, benchmark_data, 250, 22)
    assert df is not None


def test_beta():
    df = fc.get_beta(scheme_data, benchmark_data, 250, 22)
    assert df is not None


def test_upside_capture():
    df = fc.get_upside_capture(scheme_data, benchmark_data, 250, 22)
    assert df is not None


def test_downside_capture():
    df = fc.get_downside_capture(scheme_data, benchmark_data, 250, 22)
    assert df is not None


def test_drawdown():
    df = fc.get_drawdown(scheme_data, 250, 22)
    assert df is not None


def test_volatility():
    df = fc.get_volatility(scheme_data, 250, 22)
    assert df is not None


def test_sharpe():
    df = fc.get_sharpe(scheme_data, 250, 22)
    assert df is not None


def test_sortino():
    df = fc.get_sortino(scheme_data, 250, 22)
    assert df is not None


def test_main():
    assert main([]) == 0
