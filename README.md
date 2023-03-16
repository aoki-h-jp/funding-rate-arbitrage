# funding-rate-arbitrage
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110//)

## Note
This is work in progress.

## Python library for funding rate arbitrage

A framework to help you easily perform funding rate arbitrage on the following major centralized cryptocurrency exchanges (CEX).

- binance
- bybit
- OKX
- gate.io
- CoinEx
- Bitget

This library can detect perpetual contract with a large divergence in funding rates between CEXs.

**NOTE: This library does not include the feature to perform automatic funding rate arbitrage.**

## Installation


```bash
git clone https://github.com/aoki-h-jp/funding-rate-arbitrage.git
pip install funding-rate-arbitrage
```

## Usage
### Fetch FR & commission
```python
from frarb import FundingRateArbitrage

fr = FundingRateArbitrage()

# fetch all perp funding rate on binance
fr_binance = fr.fetch_all_funding_rate(exchange='binance')

# get commission on binance with futures, maker
cm_binance = fr.get_commission(exchange='binance', trade='futures', taker=False)
```

### Display large FR divergence on single CEX
```python
# display large funding rate divergence on bybit
>>> fr.display_large_divergence_single_exchange(exchange='bybit', display_num=5)
                 Funding Rate [%]  Commission [%]  Revenue [/100 USDT]
CTC/USDT:USDT              0.1794            0.32              -0.1406
CREAM/USDT:USDT            0.0338            0.32              -0.2862
TWT/USDT:USDT              0.0295            0.32              -0.2905
TLM/USDT:USDT              0.0252            0.32              -0.2948
JASMY/USDT:USDT            0.0100            0.32              -0.3100
```


## Disclaimer
This project is for educational purposes only. You should not construe any such information or other material as legal,
tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation,
endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial
instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the
securities laws of such jurisdiction.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs,
or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.