"""
Main class of funding-rate-arbitrage
"""
import logging
from datetime import datetime

import ccxt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ccxt import ExchangeError
from numpy import ndarray
from rich import print
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("rich")


class FundingRateArbitrage:
    def __init__(self):
        self.exchanges = ["binance", "bybit", "okx", "bitget", "gate", "coinex"]
        # commission
        self.is_taker = True
        self.by_token = False

    @staticmethod
    def fetch_all_funding_rate(exchange: str) -> dict:
        """
        Fetch funding rates on all perpetual contracts listed on the exchange.

        Args:
            exchange (str): Name of exchange (binance, bybit, ...)

        Returns (dict): Dict of perpetual contract pair and funding rate.

        """
        ex = getattr(ccxt, exchange)()
        info = ex.load_markets()
        perp = [p for p in info if info[p]["linear"]]
        fr_d = {}
        for p in perp:
            try:
                fr_d[p] = ex.fetch_funding_rate(p)["fundingRate"]
            except ExchangeError:
                log.exception(f"{p} is not perp.")
        return fr_d

    @staticmethod
    def fetch_funding_rate_history(exchange: str, symbol: str) -> tuple:
        """
        Fetch funding rates on perpetual contracts listed on the exchange.

        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            symbol (str): Symbol (BTC/USDT:USDT, ETH/USDT:USDT, ...).

        Returns (tuple): settlement time, funding rate.

        """
        ex = getattr(ccxt, exchange)()
        funding_history_dict = ex.fetch_funding_rate_history(symbol=symbol)
        funding_time = [
            datetime.fromtimestamp(d["timestamp"] * 0.001) for d in funding_history_dict
        ]
        funding_rate = [d["fundingRate"] * 100 for d in funding_history_dict]
        return funding_time, funding_rate

    def figure_funding_rate_history(self, exchange: str, symbol: str) -> None:
        """
        Figure funding rates on perpetual contracts listed on the exchange.

        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            symbol (str): Symbol (BTC/USDT:USDT, ETH/USDT:USDT, ...).

        Returns: None

        """
        funding_time, funding_rate = self.fetch_funding_rate_history(
            exchange=exchange, symbol=symbol
        )
        plt.plot(funding_time, funding_rate, label="funding rate")
        plt.hlines(
            xmin=funding_time[0],
            xmax=funding_time[-1],
            y=sum(funding_rate) / len(funding_rate),
            label="average",
            colors="r",
            linestyles="-.",
        )
        plt.title(f"Funding rate history {symbol}")
        plt.xlabel("timestamp")
        plt.ylabel("Funding rate [%]")
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def get_funding_rate_volatility(self, exchange: str, symbol: str) -> ndarray:
        """
        Get funding rate standard deviation volatility on all perpetual contracts listed on the exchange.

        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            symbol (str): Symbol (BTC/USDT:USDT, ETH/USDT:USDT, ...).

        Returns: Funding rate standard deviation volatility.

        """
        _, funding_rate = self.fetch_funding_rate_history(
            exchange=exchange, symbol=symbol
        )
        return np.std(funding_rate)

    def display_large_divergence_single_exchange(
        self, exchange: str, minus=False, display_num=10
    ) -> pd.DataFrame:
        """
        Display large funding rate divergence on single CEX.
        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            minus (bool): Sorted by minus FR or plus FR.
            display_num (int): Number of display.

        Returns (pd.DataFrame): DataFrame sorted by large funding rate divergence.

        """
        return (
            self.get_large_divergence_dataframe_single_exchange(
                exchange=exchange, minus=minus
            )
            .sort_values(by="Funding Rate [%]", ascending=minus)
            .head(display_num)
        )

    def display_large_divergence_multi_exchange(
        self, display_num=10, sorted_by="revenue"
    ) -> pd.DataFrame:
        """
        Display large funding rate divergence between multi CEX.
        "multi CEX" refers to self.exchanges.
        Args:
            display_num (int): Number of display.
            sorted_by (str): Sorted by "revenue" or "divergence"

        Returns (pd.DataFrame): DataFrame sorted by large funding rate divergence.

        """
        if sorted_by == "revenue":
            sorted_by = "Revenue [/100 USDT]"
        elif sorted_by == "divergence":
            sorted_by = "Divergence [%]"
        else:
            log.error(f"{sorted_by} is not available.")
            raise KeyError

        return (
            self.get_large_divergence_dataframe_multi_exchanges()
            .sort_values(by=sorted_by, ascending=False)
            .head(display_num)
        )

    def get_large_divergence_dataframe_single_exchange(
        self, exchange: str, minus=False
    ):
        """
        Get large funding rate divergence on single CEX.
        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            minus (bool): Sorted by minus FR or plus FR.

        Returns (pd.DataFrame): large funding rate divergence DataFrame.

        """
        fr = self.fetch_all_funding_rate(exchange=exchange)
        columns = ["Funding Rate [%]", "Commission [%]", "Revenue [/100 USDT]"]
        sr_fr = pd.Series(list(fr.values())) * 100
        # TODO: Check perp or spot or options exists on CEX.
        if minus:
            cm = (
                self.get_commission(
                    exchange=exchange,
                    trade="futures",
                    taker=self.is_taker,
                    by_token=self.by_token,
                )
                + self.get_commission(
                    exchange=exchange,
                    trade="options",
                    taker=self.is_taker,
                    by_token=self.by_token,
                )
                + self.get_commission(
                    exchange=exchange,
                    trade="spot",
                    taker=self.is_taker,
                    by_token=self.by_token,
                )
            )
            sr_cm = pd.Series([cm * 2 for i in range(len(sr_fr))])
            sr_rv = abs(sr_fr) - sr_cm
        else:
            cm = self.get_commission(
                exchange=exchange,
                trade="futures",
                taker=self.is_taker,
                by_token=self.by_token,
            ) + self.get_commission(
                exchange=exchange,
                trade="spot",
                taker=self.is_taker,
                by_token=self.by_token,
            )
            sr_cm = pd.Series([cm * 2 for i in range(len(sr_fr))])
            sr_rv = sr_fr - sr_cm

        df = pd.concat([sr_fr, sr_cm, sr_rv], axis=1)
        df.index = list(fr.keys())
        df.columns = columns
        return df

    def get_large_divergence_dataframe_multi_exchanges(self):
        """
        Get large funding rate divergence between multi CEX.
        "multi CEX" refers to self.exchanges.
        Returns (pd.DataFrame): large funding rate divergence DataFrame.

        """
        df = pd.DataFrame()
        for ex in self.exchanges:
            log.info(f"fetching {ex}")
            fr = self.fetch_all_funding_rate(exchange=ex)
            df_ex = pd.DataFrame(fr.values(), index=list(fr.keys()), columns=[ex]).T
            df = pd.concat([df, df_ex])
        df = df.T * 100

        diff_d = {}
        for i, data in df.iterrows():
            diff = data.max() - data.min()
            diff_d[i] = diff

        df_diff = pd.DataFrame(
            diff_d.values(), index=list(diff_d.keys()), columns=["Divergence [%]"]
        ).T
        df = pd.concat([df.T, df_diff]).T

        comm_list = []
        for i in df.index:
            max_fr_exchange = df.loc[i][:-1].idxmax()
            min_fr_exchange = df.loc[i][:-1].idxmin()
            max_fr = df.loc[i][:-1].max()
            min_fr = df.loc[i][:-1].min()
            # TODO: Check perp or spot or options exists on CEX.
            if max_fr >= 0 and min_fr >= 0:
                min_commission = self.get_commission(
                    exchange=min_fr_exchange, trade="spot"
                )
                max_commission = self.get_commission(
                    exchange=max_fr_exchange, trade="futures"
                )
            elif max_fr >= 0 > min_fr:
                max_commission = self.get_commission(
                    exchange=max_fr_exchange, trade="futures"
                )
                min_commission = self.get_commission(
                    exchange=min_fr_exchange, trade="futures"
                )
            else:
                try:
                    max_commission = self.get_commission(
                        exchange=max_fr_exchange, trade="options"
                    ) + self.get_commission(exchange=max_fr_exchange, trade="spot")
                    min_commission = self.get_commission(
                        exchange=min_fr_exchange, trade="futures"
                    )
                except KeyError:
                    max_commission = self.get_commission(
                        exchange=max_fr_exchange, trade="futures"
                    )
                    min_commission = self.get_commission(
                        exchange=min_fr_exchange, trade="futures"
                    )
            sum_of_commission = 2 * (max_commission + min_commission)
            comm_list.append(sum_of_commission)

        comm_d = {index: commission for index, commission in zip(df.index, comm_list)}
        df_comm = pd.DataFrame(
            comm_d.values(), index=list(comm_d.keys()), columns=["Commission [%]"]
        ).T
        df = pd.concat([df.T, df_comm]).T

        revenue = [
            diff_value - comm_value
            for diff_value, comm_value in zip(diff_d.values(), comm_d.values())
        ]
        df_rv = pd.DataFrame(
            revenue, index=list(comm_d.keys()), columns=["Revenue [/100 USDT]"]
        ).T
        df = pd.concat([df.T, df_rv]).T

        return df

    def display_one_by_one_single_exchange(
        self, exchange: str, minus=False, display_num=10
    ):
        """

        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            minus (bool): Sorted by minus FR or plus FR.
            display_num (int): Number of display.

        Returns: None

        """
        df = self.get_large_divergence_dataframe_single_exchange(
            exchange=exchange, minus=minus
        )
        # TODO: Check perp or spot or options exists on CEX.
        for i in (
            df.sort_values(by="Funding Rate [%]", ascending=minus)
            .head(display_num)
            .index
        ):
            print("------------------------------------------------")
            revenue = df.loc[i]["Revenue [/100 USDT]"]
            if revenue > 0:
                print(f"[bold deep_sky_blue1]Revenue: {revenue} / 100USDT[/]")
            else:
                print(f"[bold red]Revenue: {revenue} / 100USDT[/]")
            if minus:
                print(f"[bold red]SELL: {i} Options[/]")
                print(f"[bold blue]BUY: {i} Perp[/]")
            else:
                print(f"[bold red]SELL: {i} Perp[/]")
                print(f"[bold blue]BUY: {i} Spot[/]")
            print(f'Funding Rate: {df.loc[i]["Funding Rate [%]"]:.4f} %')
            print(f'Commission: {df.loc[i]["Commission [%]"]} %')

    def display_one_by_one_multi_exchanges(self, display_num=10, sorted_by="revenue"):
        """

        Args:
            display_num (int): Number of display.
            sorted_by (str): Sorted by "revenue" or "divergence"

        Returns: None

        """
        if sorted_by == "revenue":
            sorted_by = "Revenue [/100 USDT]"
        elif sorted_by == "divergence":
            sorted_by = "Divergence [%]"
        else:
            log.error(f"{sorted_by} is not available.")
            raise KeyError
        df = self.get_large_divergence_dataframe_multi_exchanges()
        # TODO: Check perp or spot or options exists on CEX.
        for i in df.sort_values(by=sorted_by, ascending=False).head(display_num).index:
            print("------------------------------------------------")
            revenue = df.loc[i]["Revenue [/100 USDT]"]
            if revenue > 0:
                print(f"[bold deep_sky_blue1]Revenue: {revenue:.4f} USDT / 100USDT[/]")
            else:
                print(f"[bold red]Revenue: {revenue:.4f} USDT / 100USDT[/]")
            max_fr_exchange = df.loc[i][:-3].idxmax()
            min_fr_exchange = df.loc[i][:-3].idxmin()
            max_fr = df.loc[i][:-3].max()
            min_fr = df.loc[i][:-3].min()
            if max_fr > 0 and min_fr > 0:
                print(
                    f"[bold red]SELL: {max_fr_exchange} {i} Perp (Funding Rate {max_fr:.4f} %)[/]"
                )
                print(f"[bold blue]BUY: {min_fr_exchange} {i} Spot[/]")
            elif max_fr > 0 > min_fr:
                print(
                    f"[bold red]SELL: {max_fr_exchange} {i} Perp (Funding Rate {max_fr:.4f} %)[/]"
                )
                print(
                    f"[bold blue]BUY: {min_fr_exchange} {i} Perp (Funding Rate {min_fr:.4f} %)[/]"
                )
            else:
                print(f"[bold red]SELL: {max_fr_exchange} {i} Options[/]")
                print(
                    f"[bold blue]BUY: {min_fr_exchange} {i} Perp (Funding Rate {min_fr:.4f} %)[/]"
                )
            print(f'Divergence: {df.loc[i]["Divergence [%]"]:.4f} %')
            print(f'Commission: {df.loc[i]["Commission [%]"]:.4f} %')

    def get_exchanges(self) -> list:
        """
        Get a list of exchanges.
        Returns (list): List of exchanges.

        """
        return self.exchanges

    def add_exchanges(self, exchange: str) -> list:
        """
        Add exchanges.
        Args:
            exchange (str): Name of the exchange you want to add.

        Returns (list): List of exchanges.

        """
        self.exchanges.append(exchange)
        return self.exchanges

    @staticmethod
    def get_commission(exchange: str, trade: str, taker=True, by_token=False) -> float:
        """
        Get commission.
        TODO: Get with ccxt or CEX API.
        Args:
            exchange (str): Name of exchanges (binance, bybit, ...)
            trade (str): Spot Trade or Futures Trade
            taker (bool): is Taker or is Maker
            by_token (bool): Pay with exchange tokens (BNB, CET, ...)

        Returns (float): Commission.

        """
        # https://www.binance.com/en/fee/schedule
        if exchange == "binance":
            if trade == "spot":
                if by_token:
                    return 0.075
                else:
                    return 0.1
            elif trade == "futures":
                if taker:
                    if by_token:
                        return 0.036
                    else:
                        return 0.04
                else:
                    if by_token:
                        return 0.018
                    else:
                        return 0.02
            elif trade == "options":
                return 0.02
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError

        # https://www.bybit.com/ja-JP/help-center/bybitHC_Article?id=360039261154&language=ja
        if exchange == "bybit":
            if trade == "spot":
                return 0.1
            elif trade == "futures":
                if taker:
                    return 0.06
                else:
                    return 0.01
            elif trade == "options":
                return 0.03
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError

        # https://www.okx.com/fees
        if exchange == "okx":
            if trade == "spot":
                if taker:
                    return 0.1
                else:
                    return 0.08
            elif trade == "futures":
                if taker:
                    return 0.05
                else:
                    return 0.02
            elif trade == "options":
                if taker:
                    return 0.03
                else:
                    return 0.02
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError

        # https://www.bitget.com/ja/rate/
        if exchange == "bitget":
            if trade == "spot":
                if by_token:
                    return 0.08
                else:
                    return 0.1
            elif trade == "futures":
                if taker:
                    return 0.051
                else:
                    return 0.017
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError

        # https://www.gate.io/ja/fee
        if exchange == "gate":
            if trade == "spot":
                if by_token:
                    return 0.15
                else:
                    return 0.2
            elif trade == "futures":
                if taker:
                    return 0.05
                else:
                    return 0.015
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError

        # https://www.coinex.zone/fees?type=spot&market=normal
        if exchange == "coinex":
            if trade == "spot":
                if by_token:
                    return 0.16
                else:
                    return 0.2
            elif trade == "futures":
                if taker:
                    return 0.05
                else:
                    return 0.03
            else:
                log.error(f"{trade} is not available on {exchange}.")
                raise KeyError
