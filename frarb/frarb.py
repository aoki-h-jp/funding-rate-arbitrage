import utils
import ccxt
import pandas as pd


class FundingRateArbitrage:
    def __init__(self):
        pass

    def fetch_all_funding_rate(self, exchange: utils.Exchange) -> dict:
        """
        Fetch funding rates on all perpetual contracts listed on the exchange.

        Args:
            exchange (utils.Exchange): Exchange (binance, bybit, ...)

        Returns (dict): Dict of perpetual contract pair and funding rate

        """
        ex = getattr(ccxt, exchange)()
        info = ex.load_markets()
        perp = [p for p in info if info[p]['linear']]
        return {p: ex.fetch_funding_rate(p)['fundingRate'] for p in perp}
