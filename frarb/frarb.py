import ccxt
import pandas as pd


class FundingRateArbitrage:
    def __init__(self):
        self.exchanges = ['binance', 'bybit', 'okx', 'bitget', 'gate', 'coinex']
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
        perp = [p for p in info if info[p]['linear']]
        return {p: ex.fetch_funding_rate(p)['fundingRate'] for p in perp}

    def display_large_divergence_single_exchange(self, exchange: str, minus=False, display_num=10) -> pd.DataFrame:
        """
        Display large funding rate divergence on single CEX.
        Args:
            exchange (str): Name of exchange (binance, bybit, ...)
            minus (bool): Sorted by minus FR or plus FR.
            display_num (int): Number of display.

        Returns (pd.DataFrame): DataFrame sorted by large funding rate divergence.

        """
        fr = self.fetch_all_funding_rate(exchange=exchange)
        columns = ['Funding Rate [%]', 'Commission [%]', 'Revenue [/100 USDT]']
        sr_fr = pd.Series(list(fr.values())) * 100
        if minus:
            cm = self.get_commission(exchange=exchange, trade='futures', taker=self.is_taker, by_token=self.by_token)\
                 + self.get_commission(exchange=exchange, trade='options', taker=self.is_taker, by_token=self.by_token)\
                 + self.get_commission(exchange=exchange, trade='spot', taker=self.is_taker, by_token=self.by_token)
            sr_cm = pd.Series([cm * 2 for i in range(len(sr_fr))])
            sr_rv = abs(sr_fr) - sr_cm
        else:
            cm = self.get_commission(exchange=exchange, trade='futures', taker=self.is_taker, by_token=self.by_token) \
                 + self.get_commission(exchange=exchange, trade='spot', taker=self.is_taker, by_token=self.by_token)
            sr_cm = pd.Series([cm * 2 for i in range(len(sr_fr))])
            sr_rv = sr_fr - sr_cm

        df = pd.concat([sr_fr, sr_cm, sr_rv], axis=1)
        df.index = list(fr.keys())
        df.columns = columns
        return df.sort_values(by=columns[0], ascending=minus).head(display_num)

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
        if exchange == 'binance':
            if trade == 'spot':
                if by_token:
                    return 0.075
                else:
                    return 0.1
            elif trade == 'futures':
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
            elif trade == 'options':
                return 0.02
            else:
                raise KeyError

        # https://www.bybit.com/ja-JP/help-center/bybitHC_Article?id=360039261154&language=ja
        if exchange == 'bybit':
            if trade == 'spot':
                return 0.1
            elif trade == 'futures':
                if taker:
                    return 0.06
                else:
                    return 0.01
            elif trade == 'options':
                return 0.03
            else:
                raise KeyError

        # https://www.okx.com/fees
        if exchange == 'okx':
            if trade == 'spot':
                if taker:
                    return 0.1
                else:
                    return 0.08
            elif trade == 'futures':
                if taker:
                    return 0.05
                else:
                    return 0.02
            elif trade == 'options':
                if taker:
                    return 0.03
                else:
                    return 0.02
            else:
                raise KeyError

        # https://www.bitget.com/ja/rate/
        if exchange == 'bitget':
            if trade == 'spot':
                if by_token:
                    return 0.08
                else:
                    return 0.1
            elif trade == 'futures':
                if taker:
                    return 0.051
                else:
                    return 0.017
            else:
                raise KeyError

        # https://www.gate.io/ja/fee
        if exchange == 'gate':
            if trade == 'spot':
                if by_token:
                    return 0.15
                else:
                    return 0.2
            elif trade == 'futures':
                if taker:
                    return 0.05
                else:
                    return 0.015
            else:
                raise KeyError

        # https://www.coinex.zone/fees?type=spot&market=normal
        if exchange == 'gate':
            if trade == 'spot':
                if by_token:
                    return 0.16
                else:
                    return 0.2
            elif trade == 'futures':
                if taker:
                    return 0.05
                else:
                    return 0.03
            else:
                raise KeyError
