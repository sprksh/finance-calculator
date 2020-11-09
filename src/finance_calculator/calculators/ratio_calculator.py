import numpy as np
import pandas as pd
import math

days_in_year = 250
default_risk_free_rate = 0.05


class RatioCalculator:

    def __init__(self, nav_dataframe, benchmark_nav_dataframe=None, risk_free_rate=None, annualiser=None):
        self_nav_df = self._load(nav_dataframe)
        self.risk_free_rate = risk_free_rate
        self.annualiser = annualiser if annualiser else days_in_year
        if benchmark_nav_dataframe is None:
            benchmark_nav_dataframe = self.create_benchmark_nav_from_risk_free_rate(
                nav_dataframe, risk_free_rate
            )
        benchmark_nav_df = self._load(benchmark_nav_dataframe)
        self.combo_nav_df = self._merge(self_nav_df, benchmark_nav_df)
        self.beta_cache = None

    @staticmethod
    def _load(data, ):
        if data is None:
            return pd.DataFrame()
        ret = "returns"
        data[ret] = data["nav"].pct_change()

        return data

    def create_benchmark_nav_from_risk_free_rate(self, nav_dataframe, risk_free_rate):
        if not risk_free_rate: return None
        initial_value = 100
        risk_free_rate = risk_free_rate / self.annualiser
        benchmark_nav_df = nav_dataframe.filter(["nav"])
        initial_index = benchmark_nav_df.index.min()

        def apply_drag(row, initial_value, initial_index, rate):
            count = (row.name - initial_index).days
            return initial_value * math.pow(1 + rate, count)

        benchmark_nav_df["nav"] = benchmark_nav_df.apply(apply_drag, args=(initial_value, initial_index, risk_free_rate), axis=1)
        return benchmark_nav_df.filter(["nav"])

    @staticmethod
    def _merge(scheme_df, benchmark_df):
        if not benchmark_df.empty:
            combo_df = scheme_df.join(benchmark_df, how="left", rsuffix='_benchmark')
            return combo_df
        return scheme_df

    def get_treynor(self, period=None):
        beta_df = self.get_beta(period)
        df = self.combo_nav_df
        df = df.join(beta_df, how="inner", rsuffix='_beta')
        df["treynor"] = (df["returns"] - df["returns_benchmark"]) / df["beta"]
        return df.filter(["treynor"])

    def get_alpha(self, window):
        beta_df = self.get_beta(window)

        df = self.combo_nav_df

        df = df.join(beta_df, how="inner")
        df["cumulative_returns"] = df["returns"].cumsum()
        df["cumulative_returns_benchmark"] = df["returns_benchmark"].cumsum()
        df["alpha"] = df["cumulative_returns"] - (
            df["cumulative_returns_benchmark"]
            + df["beta"]
            * (df["cumulative_returns"] - df["cumulative_returns_benchmark"])
        )
        return df.filter(["alpha"])

    def get_beta(self, window):
        """
        https://stackoverflow.com/questions/39501277/efficient-python-pandas-stock-beta-calculation-on-many-dataframes

        beta = covariance(returns, benchmark returns) / variance(benchmark returns)
        also excel cov(a, b) = b.cov(a) in pandas
        """
        if self.beta_cache is not None:
            return self.beta_cache

        df = self.combo_nav_df.copy()
        df["var"] = df["returns_benchmark"].rolling(window=window).var()
        df["cov"] = df["returns_benchmark"].rolling(window=window).cov(df["returns"])
        df["beta"] = df["cov"]/df["var"]
        df = df.filter(["beta"])
        self.beta_cache = df
        return df

    def get_upside_capture(self, window):
        """
        requires benchmark data
        """

        df = self.combo_nav_df
        df["scheme_return_when_benchmark_up"] = df["returns"].where(
            df["returns_benchmark"] > 0, 0
        )
        df["benchmark_return_when_benchmark_up"] = df["returns_benchmark"].where(
            df["returns_benchmark"] > 0, 0
        )

        df["upside_cagr_fund"] = (1 + df["scheme_return_when_benchmark_up"]).rolling(
            window=window).apply(np.prod, raw=True) - 1
        df["upside_cagr_index"] = (1 + df["benchmark_return_when_benchmark_up"]).rolling(
            window=window).apply(np.prod, raw=True) - 1

        df["upside_capture_ratio"] = (1 + df["upside_cagr_fund"]) / (1 + df["upside_cagr_index"])
        return df

    def get_downside_capture(self, window):
        """
        requires benchmark data
        """
        df = self.combo_nav_df
        df["scheme_return_when_benchmark_down"] = df["returns"].where(
            df["returns_benchmark"] < 0, 0
        )
        df["benchmark_return_when_benchmark_down"] = df["returns_benchmark"].where(
            df["returns_benchmark"] < 0, 0
        )

        df["downside_cagr_fund"] = (1+df["scheme_return_when_benchmark_down"]).rolling(window=window).apply(np.prod, raw=True) - 1
        df["downside_cagr_index"] = (1+df["benchmark_return_when_benchmark_down"]).rolling(window=window).apply(np.prod, raw=True) - 1

        df["downside_capture_ratio"] = (1 - df["downside_cagr_fund"]) / (1 - df["downside_cagr_index"])
        return df

    def get_drawdown(self, window):
        """
        here window means that a max would be taken for that rolling window
        :param period:
        :return:
        """
        df = self.combo_nav_df

        df["nav_peak"] = df["nav"].rolling(window=window).max()
        df["drawdown"] = (df["nav"] / df["nav_peak"]) - 1

        # how to get days
        # df = df.tail(window)
        # max_drawdown_idx = df["drawdown"].idxmin()
        # max_drawdown_idx_peak = df["nav_peak"][max_drawdown_idx]
        # for i, r in df.iterrows():
        #     if i > max_drawdown_idx and r["nav"] >= max_drawdown_idx_peak:
        #         days = (i-max_drawdown_idx).days
        #         print(days)
        #         break

        return df

    def get_volatility(self, window):
        df = self.combo_nav_df
        df["volatility"] = (
            df["returns"].rolling(window=window).std() * math.sqrt(self.annualiser)
        )
        return df.filter(["volatility"])

    def get_sharpe(self, window):
        """
        https://stackoverflow.com/questions/49091044/python-rolling-sharpe-ratio-with-pandas-or-numpy
        """
        #   (rp - rf) / sigma p
        #   mean(per date returns row) - mean(per date benchmark return)
        #   -----------------------------------------------------------
        #                   std(excess returns)
        #

        df = self.combo_nav_df

        df["returns_mean"] = ((1+df["returns"].rolling(window=window).mean()) ** self.annualiser)-1
        df["benchmark_returns_mean"] = ((1+df["returns_benchmark"].rolling(window=window).mean()) ** self.annualiser)-1
        df["excess_returns_std"] = (df["returns"] - df["returns_benchmark"]).rolling(window=window).std() * math.sqrt(self.annualiser)
        df["sharpe"] = (df["returns_mean"] - df["benchmark_returns_mean"]) / df["excess_returns_std"]

        return df.filter(["sharpe"])

    def get_sortino(self, window):
        """
        Similar to sharpe, only negative returns are considered
        """
        df = self.combo_nav_df

        df["returns_mean"] = ((1 + df["returns"].rolling(window=window).mean()) ** self.annualiser) - 1
        df["benchmark_returns_mean"] = ((1 + df["returns_benchmark"].rolling(window=window).mean()) ** self.annualiser) - 1
        df["excess_returns"] = df["returns"] - df["returns_benchmark"]
        df["excess_returns_downside"] = df["excess_returns"].where(df["excess_returns"] < 0, 0)
        df["downside_excess_returns_std"] = df["excess_returns_downside"].rolling(window=window).std() * math.sqrt(self.annualiser)

        df["sortino"] = (
                         df["returns_mean"] - df["benchmark_returns_mean"]
                     ) / df["downside_excess_returns_std"]

        return df.filter(["sortino"])
