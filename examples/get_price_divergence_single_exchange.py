"""
An example of fetching price divergence by single exchange.
"""
from frarb import FundingRateArbitrage


if __name__ == '__main__':
    fr = FundingRateArbitrage()
    # fetch price divergence on binance.
    print(fr.fetch_price_divergence_single_exchange(exchange='binance'))
