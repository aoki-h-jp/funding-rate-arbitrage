"""
An example of fetching funding rate
"""
from frarb import FundingRateArbitrage
from frarb.utils import Exchange


if __name__ == '__main__':
    # fetch from binance
    fr = FundingRateArbitrage()
    fr.fetch_all_funding_rate(Exchange.BINANCE)
