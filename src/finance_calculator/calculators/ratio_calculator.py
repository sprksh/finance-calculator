import pandas as pd
import numpy as np


class FinanceCalculator:
    def __init__(self, self_nav_data, benchmark_nav_data=None):
        self.self_nav_df = None
        self.benchmark_nav_df = None

        self._load(self_nav_data, benchmark_nav_data)

    def _load(self, self_nav_data, benchmark_nav_data):
        def _create_date_nav_df(nav_data, benchmark=False):
            nav, ret, c_ret = "nav", "returns", "cumulative_returns"
            if benchmark:
                nav, ret, c_ret = [_ + "_benchmark" for _ in [nav, ret, c_ret]]

            df = pd.DataFrame(nav_data, columns=["date", nav])
            pd.to_datetime(df["date"])
            df.set_index("date")
            df[ret] = df[nav].pct_change()
            df[c_ret] = df[ret].cumsum()
            return df

        self.self_nav_df = _create_date_nav_df(self_nav_data)
        if benchmark_nav_data:
            self.benchmark_nav_df = _create_date_nav_df(benchmark_nav_data)
            self.self_nav_df.join(self.benchmark_nav_df, how="inner")

    def get_treynor(self):
        beta_df = self.get_beta()

        df = self.self_nav_df
        df.join(beta_df, how="inner")
        df["treynor"] = (df["returns"] - df["returns_benchmark"]) / df["beta"]
        return df

    def get_alpha(self):
        beta_df = self.get_beta()

        df = self.self_nav_df
        df.join(beta_df, how="inner")
        df["alpha"] = df["cumulative_returns"] - (
            df["cumulative_returns_benchmark"]
            + df["beta"]
            * (df["cumulative_returns"] - df["cumulative_returns_benchmark"])
        )
        return df

    def get_beta(self):
        """
        https://stackoverflow.com/questions/39501277/efficient-python-pandas-stock-beta-calculation-on-many-dataframes
        """

        def beta(df):
            market = df["nav_benchmark"]
            df = df.drop("nav_benchmark", axis=1)

            X = market.values.reshape(-1, 1)
            X = np.concatenate([np.ones_like(X), X], axis=1)
            b = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(df.values)
            return pd.Series(b[1], df.columns, name=df.index[-1])

        def roll(df, w):
            for i in range(df.shape[0] - w + 1):
                yield pd.DataFrame(
                    df.values[i : i + w, :], df.index[i : i + w], df.columns
                )

        df = self.self_nav_df
        betas = pd.concat(
            [beta(sdf) for sdf in roll(df.pct_change().dropna(), 12)], axis=1
        ).T
        return betas

    def get_upside_capture(self):
        """
        requires benchmark data
        """

        df = self.self_nav_df
        df["scheme_return_when_benchmark_up"] = df["returns"].where(
            df["returns"] > 0, 0
        )
        df["benchmark_return_when_benchmark_up"] = df["returns"].where(
            df["returns"] > 0, 0
        )

        df["upside_cagr_fund"] = df["scheme_return_when_benchmark_up"].rolling(60).sum()
        df["upside_cagr_index"] = (
            df["benchmark_return_when_benchmark_up"].rolling(60).sum()
        )

        df["upside_capture_ratio"] = df["upside_cagr_fund"] / df["upside_cagr_index"]
        return df

    def get_downside_capture(self):
        """
        requires benchmark data
        """
        df = self.self_nav_df
        df["scheme_return_when_benchmark_down"] = df["returns"].where(
            df["returns"] < 0, 0
        )
        df["benchmark_return_when_benchmark_down"] = df["returns"].where(
            df["returns"] < 0, 0
        )

        df["downside_cagr_fund"] = (
            df["scheme_return_when_benchmark_down"].rolling(60).sum()
        )
        df["downside_cagr_index"] = (
            df["benchmark_return_when_benchmark_down"].rolling(60).sum()
        )

        df["downside_capture_ratio"] = (
            df["downside_cagr_fund"] / df["downside_cagr_index"]
        )
        return df

    def get_drawdown(self):
        # instead work on nav
        df = self.self_nav_df
        df["scheme_peak_return"] = df["returns"].rolling(window=60).max()
        df["drawdown"] = df["returns"] - df["scheme_peak_return"]
        df["drawdown %"] = -df["drawdown"] / df["scheme_peak_return"]
        return df

    def get_volatility(self):
        self.self_nav_df["volatility"] = (
            self.self_nav_df["returns"].rolling(window=60).std()
        )
        return self.self_nav_df

    def get_sharpe(self):
        """
        https://stackoverflow.com/questions/49091044/python-rolling-sharpe-ratio-with-pandas-or-numpy
        """

        def my_rolling_sharpe(y):
            return np.sqrt(21) * (
                y.mean() / y.std()
            )  # 21 days per month X 6 months = 126

        df = self.self_nav_df
        df["rolling_sharpe"] = df["returns"].rolling(60).apply(my_rolling_sharpe)
        # df['rolling_sharpe_2'] = [my_rolling_sharpe(df.loc[d - \
        # pd.offsets.DateOffset(months=6):d, 'returns']) for d in df.index]
        return df

    def get_sortino(self):
        """
        Similar to sharpe, only negative returns are considered
        """

        def my_rolling_sortino(y):
            return np.sqrt(60) * (
                y.mean() / y.std()
            )  # 21 days per month X 6 months = 126

        df = self.self_nav_df
        df["downside_return"] = df["returns"].where(df["returns"] < 0, 0)
        df["rolling_sortino"] = (
            df["downside_return"].rolling(60).apply(my_rolling_sortino)
        )
        return df
