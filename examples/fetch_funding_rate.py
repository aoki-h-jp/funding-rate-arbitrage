"""
An example of fetching funding rate
"""
from frarb import FundingRateArbitrage


if __name__ == '__main__':
    # fetch from binance
    fr = FundingRateArbitrage()
    print(fr.fetch_all_funding_rate(exchange='binance'))
