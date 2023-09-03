"""
An example of getting commission.
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage

if __name__ == "__main__":
    fr = FundingRateArbitrage()
    # binance futures maker commission with BNB
    print("binance futures maker commission with BNB")
    print(
        fr.get_commission(
            exchange="binance", trade="futures", taker=False, by_token=True
        )
    )

    # bybit spot taker commission
    print("bybit spot taker commission")
    print(fr.get_commission(exchange="bybit", trade="spot"))

    # OKX spot maker commission
    print("OKX spot maker commission")
    print(fr.get_commission(exchange="okx", trade="spot", taker=False))
