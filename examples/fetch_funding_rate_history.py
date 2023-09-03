"""
An example of fetching funding rate history
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage

if __name__ == "__main__":
    # fetch from binance
    fr = FundingRateArbitrage()
    # figure funding rate history
    fr.figure_funding_rate_history(exchange="binance", symbol="BTC/USDT:USDT")
