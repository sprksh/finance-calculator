import pandas as pd
from src.finance_calculator.calculators.portfolio_calculator import XIRR
from src.finance_calculator.calculators.ratio_calculator import RatioCalculator


def get_xirr(cashflows) -> int:
    """
    Returns Excel style xirr
    IRR: The internal rate of return is a metric used in financial analysis to estimate the
    profitability of potential investments. The internal rate of return is a discount
    rate that makes the net present value (NPV) of all cash flows equal to zero in a
    discounted cash flow analysis. IRR calculations rely on the same formula as NPV does.
    XIRR is used when the cash flow model does not exactly have annual periodic cash flows.
    (Investopedia)

    :param cashflows:
    :return: int
    """
    if isinstance(cashflows, pd.DataFrame):
        pass
    if isinstance(cashflows, list):
        if not all(isinstance(item, tuple) for item in cashflows):
            raise TypeError("expected a list of tuple of (date, amount)")
    else:
        raise TypeError("function called for unsupported data types.")
    return XIRR(cashflows).get_xirr()


def _verify_nav_df(nav_dataframe):
    if "nav" not in nav_dataframe.columns:
        raise ValueError("nav dataframe must have 'nav' column")
    if nav_dataframe.nav.dtype not in [int, float]:
        raise ValueError("nav values must be in int, float or decimal")
    # if not nav_dataframe.index.is_all_dates:
    #     raise ValueError("nav dataframe index must be date")
    return nav_dataframe


def _transform_df(nav_data):
    if not isinstance(nav_data, pd.DataFrame):
        nav_data = _convert_data_to_df(nav_data)
    if "date" in nav_data.columns and nav_data["date"].dtype == str:
        nav_data["date"] = pd.to_datetime(nav_data["date"])
    nav_data.set_index("date", inplace=True)
    _verify_nav_df(nav_data)
    return nav_data


def _convert_data_to_df(nav_data):
    df = pd.DataFrame()
    if isinstance(nav_data, list):
        if not all(isinstance(item, tuple) for item in nav_data):
            raise TypeError("")
        df = pd.DataFrame(nav_data, columns=["date", "nav"])
    elif isinstance(nav_data, dict):
        cols = nav_data.keys()
        if "date" not in cols or "nav" not in cols:
            raise TypeError("dictionary must contain 'nav' and 'date' columns.")
        pd.DataFrame(nav_data)
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise Exception("unhandled Exception, could not create dataframe")
    # convert dict, tuple and list data-types to pandas df before passing on.
    return df


def get_drawdown(nav_data, period, window, tail=True):
    """
    A drawdown is a peak-to-trough decline during a specific period for an investment,
    trading account, or fund. A drawdown is usually quoted as the percentage between the
    peak and the subsequent trough. If a trading account has $10,000 in it, and the funds
    drop to $9,000 before moving back above $10,000, then the trading account witnessed
    a 10% drawdown. (Investopedia)

    :param nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    df = RatioCalculator(nav_dataframe).get_drawdown(period, window)
    return float(df["drawdown %"][-1]) if tail else df


def get_volatility(nav_data, period, window, tail=True):
    """
    Volatility is a statistical measure of the dispersion of returns for a given security
    or market index. In most cases, the higher the volatility, the riskier the security.
    Volatility is often measured as either the standard deviation or variance between returns
    from that same security or market index. (Investopedia)

    :param nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    df = RatioCalculator(nav_dataframe).get_volatility(period, window)
    return float(df["volatility"][-1]) if tail else df


def get_sharpe(nav_data, period, window, risk_free_rate=0, tail=True):
    """
    The Sharpe ratio was developed by Nobel laureate William F. Sharpe and is used to help
    investors understand the return of an investment compared to its risk.﻿ The ratio is the
    average return earned in excess of the risk-free rate per unit of volatility or total risk.
    Volatility is a measure of the price fluctuations of an asset or portfolio. (Investopedia)

    :param nav_data:
    :param period: int
    :param window: int
    :param risk_free_rate: float
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    df = RatioCalculator(nav_dataframe).get_sharpe(period, window)
    return float(df["sharpe"][-1]) if tail else df


def get_sortino(nav_data, period, window, tail=True):
    """
    The Sortino ratio is a variation of the Sharpe ratio that differentiates harmful volatility
    from total overall volatility by using the asset's standard deviation of negative portfolio
    returns—downside deviation—instead of the total standard deviation of portfolio returns.
    The Sortino ratio takes an asset or portfolio's return and subtracts the risk-free rate,
    and then divides that amount by the asset's downside deviation. (Investopedia)

    :param nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    df = RatioCalculator(nav_dataframe).get_sortino(period, window)
    return float(df["sortino"][-1]) if tail else df


def get_treynor(nav_data, benchmark_nav_data, period, window, tail=True):
    """
    The Treynor ratio, also known as the reward-to-volatility ratio, is a performance metric for
    determining how much excess return was generated for each unit of risk taken on by a portfolio.
    (Investopedia)

    :param nav_data:
    :param benchmark_nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    benchmark_nav_dataframe = _transform_df(benchmark_nav_data)
    df = RatioCalculator(
        nav_dataframe, benchmark_nav_dataframe=benchmark_nav_dataframe
    ).get_treynor(period, window)
    return float(df["treynor"][-1]) if tail else df


def get_alpha(nav_data, benchmark_nav_data, period, window, tail=True):
    """
    Alpha describes a strategy's ability to beat the market, or it's "edge." Alpha is thus also
    often referred to as “excess return” or “abnormal rate of return,” which refers to the idea
    that markets are efficient, and so there is no way to systematically earn returns that exceed
    the broad market as a whole. Alpha is often used in conjunction with beta (the Greek letter β),
    which measures the broad market's overall volatility or risk, known as systematic market risk.
    (Investopedia)

    :param nav_data:
    :param benchmark_nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    benchmark_nav_dataframe = _transform_df(benchmark_nav_data)
    df = RatioCalculator(
        nav_dataframe, benchmark_nav_dataframe=benchmark_nav_dataframe
    ).get_alpha(period, window)
    return float(df["alpha"][-1]) if tail else df


def get_beta(nav_data, benchmark_nav_data, period, window, tail=True):
    """
    Beta is a measure of the volatility—or systematic risk—of a security or portfolio compared
    to the market as a whole. Beta is used in the capital asset pricing model (CAPM), which
    describes the relationship between systematic risk and expected return for assets (usually
    stocks). CAPM is widely used as a method for pricing risky securities and for generating
    estimates of the expected returns of assets, considering both the risk of those assets
    and the cost of capital. (Investopedia)

    :param nav_data:
    :param benchmark_nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    benchmark_nav_dataframe = _transform_df(benchmark_nav_data)
    df = RatioCalculator(
        nav_dataframe, benchmark_nav_dataframe=benchmark_nav_dataframe
    ).get_beta(period, window)
    return float(df["beta"][-1]) if tail else df


def get_upside_capture(nav_data, benchmark_nav_data, period, window, tail=True):
    """
    The up-market capture ratio is the statistical measure of an investment manager's overall
    performance in up-markets. It is used to evaluate how well an investment manager performed
    relative to an index during periods when that index has risen. The ratio is calculated by
    dividing the manager's returns by the returns of the index during the up-market and
    multiplying that factor by 100. (Investopedia)

    :param nav_data:
    :param benchmark_nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    benchmark_nav_dataframe = _transform_df(benchmark_nav_data)
    df = RatioCalculator(
        nav_dataframe, benchmark_nav_dataframe=benchmark_nav_dataframe
    ).get_upside_capture(period, window)
    return float(df["upside_capture_ratio"][-1]) if tail else df


def get_downside_capture(nav_data, benchmark_nav_data, period, window, tail=True):
    """
    The down-market capture ratio is a statistical measure of an investment manager's overall
    performance in down-markets. It is used to evaluate how well an investment manager performed
    relative to an index during periods when that index has dropped. The ratio is calculated by
    dividing the manager's returns by the returns of the index during the down-market and
    multiplying that factor by 100. (Investopedia)

    :param nav_data:
    :param benchmark_nav_data:
    :param period: int
    :param window: int
    :param tail: bool
    :return:
    """
    nav_dataframe = _transform_df(nav_data)
    benchmark_nav_dataframe = _transform_df(benchmark_nav_data)
    df = RatioCalculator(
        nav_dataframe, benchmark_nav_dataframe=benchmark_nav_dataframe
    ).get_downside_capture(period, window)
    return float(df["downside_capture_ratio"][-1]) if tail else df
