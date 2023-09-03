"""
An example of displaying large divergence by single exchange.
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage

if __name__ == "__main__":
    fr = FundingRateArbitrage()
    # Display Top 5 large funding rate divergence on binance.
    print(
        fr.display_large_divergence_single_exchange(exchange="binance", display_num=5)
    )

    # Display Top 5 large funding rate divergence on bybit (minus FR).
    print(
        fr.display_large_divergence_single_exchange(
            exchange="bybit", display_num=5, minus=True
        )
    )

    # Display Top 5 large funding rate divergence on binance one by one.
    fr.display_one_by_one_single_exchange(exchange="binance", display_num=5)

    # Display Top 5 large funding rate divergence on bybit one by one (minus FR).
    fr.display_one_by_one_single_exchange(exchange="bybit", display_num=5, minus=True)
