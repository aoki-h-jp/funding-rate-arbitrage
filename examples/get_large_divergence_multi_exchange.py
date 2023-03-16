"""
An example of getting large divergence between multi exchange.
"""
from frarb import FundingRateArbitrage


if __name__ == '__main__':
    fr = FundingRateArbitrage()
    # Display Top 5 large funding rate divergence between multi exchange.
    print(fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='divergence'))

    # Display Top 5 large funding rate divergence between multi exchange sorted by revenue.
    print(fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='revenue'))
