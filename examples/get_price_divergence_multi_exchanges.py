"""
An example of fetching price divergence by multi exchanges.
"""
from frarb import FundingRateArbitrage


if __name__ == '__main__':
    fr = FundingRateArbitrage()
    # fetch price divergence between multi CEXs futures.
    print(fr.fetch_price_divergence_multi_exchanges())
