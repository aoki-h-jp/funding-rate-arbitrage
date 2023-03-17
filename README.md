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

### Fetch FR history
```python
from frarb import FundingRateArbitrage

fr = FundingRateArbitrage()

# figure funding rate history
fr.fetch_funding_rate_history(exchange='binance', symbol='BTC/USDT:USDT')
```
!['funding rate history example'](./img/readme_funding_rate_history.png)


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

# display Top 5 large funding rate divergence on bybit one by one.
>>> fr.display_one_by_one_single_exchange(exchange='bybit', display_num=5)
------------------------------------------------
Revenue: -0.1663 / 100USDT
SELL: CTC/USDT:USDT Perp
BUY: CTC/USDT:USDT Spot
Funding Rate: 0.1537 %
Commission: 0.32 %
------------------------------------------------
Revenue: -0.17200000000000001 / 100USDT
SELL: CREAM/USDT:USDT Perp
BUY: CREAM/USDT:USDT Spot
Funding Rate: 0.1480 %
Commission: 0.32 %
------------------------------------------------
Revenue: -0.2107 / 100USDT
SELL: BOBA/USDT:USDT Perp
BUY: BOBA/USDT:USDT Spot
Funding Rate: 0.1093 %
Commission: 0.32 %
------------------------------------------------
Revenue: -0.2854 / 100USDT
SELL: TLM/USDT:USDT Perp
BUY: TLM/USDT:USDT Spot
Funding Rate: 0.0346 %
Commission: 0.32 %
------------------------------------------------
Revenue: -0.2953 / 100USDT
SELL: TOMO/USDT:USDT Perp
BUY: TOMO/USDT:USDT Spot
Funding Rate: 0.0247 %
Commission: 0.32 %

# display Top 5 large funding rate divergence on bybit one by one (minus FR).
>>> fr.display_one_by_one_single_exchange(exchange='bybit', display_num=5, minus=True)
------------------------------------------------
Revenue: -0.1458 / 100USDT
SELL: ARPA/USDT:USDT Options
BUY: ARPA/USDT:USDT Perp
Funding Rate: -0.2342 %
Commission: 0.38 %
------------------------------------------------
Revenue: -0.2569 / 100USDT
SELL: MASK/USDT:USDT Options
BUY: MASK/USDT:USDT Perp
Funding Rate: -0.1231 %
Commission: 0.38 %
------------------------------------------------
Revenue: -0.3056 / 100USDT
SELL: APE/USD:USDC Options
BUY: APE/USD:USDC Perp
Funding Rate: -0.0744 %
Commission: 0.38 %
------------------------------------------------
Revenue: -0.3158 / 100USDT
SELL: SWEAT/USD:USDC Options
BUY: SWEAT/USD:USDC Perp
Funding Rate: -0.0642 %
Commission: 0.38 %
------------------------------------------------
Revenue: -0.3166 / 100USDT
SELL: APE/USDT:USDT Options
BUY: APE/USDT:USDT Perp
Funding Rate: -0.0634 %
Commission: 0.38 %
```

### Display large FR divergence between CEX
```python
# display large funding rate divergence between CEX.
>>> fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='divergence')
                 binance   bybit       okx  bitget    gate    coinex  Divergence [%]  Commission [%]  Revenue [/100 USDT]
FIL/USDT:USDT  -0.008948 -0.0229 -0.334535 -0.0084 -0.0240 -0.737473        0.729073           0.202             0.527073
HNT/USDT:USDT  -0.023885 -0.0125       NaN     NaN  0.0056  0.304442        0.328327           0.180             0.148327
WAXP/USDT:USDT       NaN     NaN       NaN     NaN  0.0100  0.205733        0.195733           0.500            -0.304267
AXS/USDT:USDT  -0.021292 -0.0385 -0.205174 -0.0212 -0.0282 -0.215217        0.194017           0.202            -0.007983
OP/USDT:USDT   -0.060397 -0.0228 -0.206011 -0.0601 -0.0147 -0.148713        0.191311           0.200            -0.008689

# sorted by revenue. 
>>> fr.display_large_divergence_multi_exchange(display_num=5, sorted_by='revenue')
                binance   bybit       okx  bitget    gate    coinex  Divergence [%]  Commission [%]  Revenue [/100 USDT]
FIL/USDT:USDT -0.004703 -0.0232 -0.334535 -0.0047 -0.0245 -0.737473        0.732773           0.202             0.530773
HNT/USDT:USDT -0.030722 -0.0141       NaN     NaN  0.0051  0.304442        0.335164           0.180             0.155164
OP/USDT:USDT  -0.057856 -0.0235 -0.206011 -0.0589 -0.0162 -0.148713        0.189811           0.200            -0.010189
MKR/USDT:USDT  0.010000  0.0100 -0.056437  0.0104  0.0100  0.075530        0.131967           0.200            -0.068033
TON/USDT:USDT       NaN     NaN -0.023741     NaN  0.0100 -0.116483        0.126483           0.200            -0.073517

# Display Top 5 large funding rate divergence between multi exchange.
>>> fr.display_one_by_one_multi_exchanges(display_num=5)
------------------------------------------------
Revenue: 0.2184 USDT / 100USDT
SELL: coinex IOTA/USDT:USDT Perp (Funding Rate 0.3478 %)
BUY: okx IOTA/USDT:USDT Perp (Funding Rate -0.0706 %)
Divergence: 0.4184 %
Commission: 0.2000 %
------------------------------------------------
Revenue: 0.1191 USDT / 100USDT
SELL: coinex DASH/USDT:USDT Perp (Funding Rate 0.4267 %)
BUY: okx DASH/USDT:USDT Spot
Divergence: 0.4191 %
Commission: 0.3000 %
------------------------------------------------
Revenue: 0.1080 USDT / 100USDT
SELL: okx TON/USDT:USDT Perp (Funding Rate 0.0482 %)
BUY: coinex TON/USDT:USDT Perp (Funding Rate -0.2598 %)
Divergence: 0.3080 %
Commission: 0.2000 %
------------------------------------------------
Revenue: 0.0842 USDT / 100USDT
SELL: binance GMX/USDT:USDT Perp (Funding Rate 0.0100 %)
BUY: coinex GMX/USDT:USDT Perp (Funding Rate -0.2542 %)
Divergence: 0.2642 %
Commission: 0.1800 %
------------------------------------------------
Revenue: 0.0447 USDT / 100USDT
SELL: okx FIL/USDT:USDT Perp (Funding Rate 0.2416 %)
BUY: gate FIL/USDT:USDT Perp (Funding Rate -0.0031 %)
Divergence: 0.2447 %
Commission: 0.2000 %
```

### Fetch price divergence
```python
# fetch price divergence on binance.
>>> fr.fetch_price_divergence_single_exchange(exchange='binance')
# {'ALPHA/USDT': 0.1108033240997313, 'CTK/USDT': 0.06443298969071455, 'SKL/USDT': 0.04746084480305203, 'ZRX/USDT': 0.04393673110721298, 'AUDIO/USDT': 0.03880481179665852,...}

# fetch price divergence between multi CEXs futures.
>>> print(fr.fetch_price_divergence_multi_exchanges(display_num=5))
               binance    bybit           okx  bitget          gate        coinex  Divergence [USDT]  Divergence [%]
GPT/USDT:USDT      NaN  0.12230           NaN     NaN  1.180000e-01           NaN       4.300000e-03        3.644068
HNT/USDT:USDT   1.6460  1.66400           NaN     NaN  1.670000e+00  1.649900e+00       2.400000e-02        1.458080
BSW/USDT:USDT      NaN  0.18890           NaN     NaN  1.866000e-01           NaN       2.300000e-03        1.232583
IMX/USDT:USDT   1.3411  1.34060  1.327000e+00  1.3404  1.341000e+00  1.341000e+00       1.410000e-02        1.062547
NFT/USDT:USDT      NaN      NaN  4.148000e-07     NaN  4.190000e-07  4.148000e-07       4.200000e-09        1.012536
```

## Future works
- Get trading volume in 24 hours and filter outputs. (1.3.0)
- Get price divergence between spot and perpetual contract and filter outputs. (1.3.0)
- Support KuCoin, MEXC. (1.X.X)
- Notify discord, slack by webhook. (1.X.X)
- Implement unittest. (1.X.X)
- Perform automatic funding rate arbitrage. (2.X.X)
- Predict funding rate by open interest, etc. (2.X.X)
- Support DEXs. (2.X.X)

## Disclaimer
This project is for educational purposes only. You should not construe any such information or other material as legal,
tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation,
endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial
instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the
securities laws of such jurisdiction.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs,
or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.
