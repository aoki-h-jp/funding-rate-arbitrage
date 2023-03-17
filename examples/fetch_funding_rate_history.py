"""
An example of fetching funding rate history
"""
from frarb import FundingRateArbitrage


if __name__ == '__main__':
    # fetch from binance
    fr = FundingRateArbitrage()
    # figure funding rate history
    fr.fetch_funding_rate_history(exchange='binance', symbol='BTC/USDT:USDT')
