"""
An example of fetching funding rate
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage

if __name__ == "__main__":
    # fetch from all exchanges
    fr = FundingRateArbitrage()
    for ex in fr.get_exchanges():
        print(ex)
        print(fr.fetch_all_funding_rate(exchange=ex))
