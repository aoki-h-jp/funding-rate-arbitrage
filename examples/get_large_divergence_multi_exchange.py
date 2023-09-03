"""
An example of getting large divergence between multi exchange.
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage

if __name__ == "__main__":
    fr = FundingRateArbitrage()
    # Display Top 5 large funding rate divergence between multi exchange.
    # print(fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='divergence'))

    # TODO:　Errors occur when running consecutively.
    # ccxt.base.errors.BadRequest: binance {"code":-1104,"msg":"Not all sent parameters were read; read '0' parameter(s) but was sent '1'."}
    # Display Top 5 large funding rate divergence between multi exchange sorted by revenue.
    # print(fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='revenue'))

    # Display Top 5 large funding rate divergence between multi exchange.
    fr.display_one_by_one_multi_exchanges(display_num=5)
