# StockScope Learn V19 — Change and QA Notes

## Homepage challenge 01: MA + MACD historical signal
- Replaced the former fixed NVDA price-only prediction challenge with a live historical case finder that reads five years of Yahoo Finance adjusted daily OHLCV via the existing `load_prices` data path.
- Candidate tickers: NVDA, AAPL, MSFT, AMD, SPY and QQQ. The finder calculates MA5 / MA20 and standard MACD (12,26,9), then selects a historical sample in which MA5 crosses above MA20 and DIF crosses above DEA within three trading sessions, while retaining 20 subsequent trading sessions for reveal.
- A 3-row Plotly view shows candles + MA5/MA20, volume, and MACD histogram + DIF/DEA. The two crossover dates are highlighted.
- Explicit color key: green up / red down for candles and volume. The legend separately explains that MACD histogram green/red denotes DIF above/below DEA.
- Before submit, chart contains only history through the later crossover date. It reserves a masked right-hand future area over the 20 later sessions. After submit, the same chart component and x-axis directly render all real subsequent candles, MAs, volume and MACD; the question is removed and the result interpretation appears below the chart.
- The selected ticker/date is dynamic because it is calculated from real fetched market data. If the provider fails or no eligible sample is found, the application shows a warning rather than inserting synthetic prices.

## Regression protection
- Retained V18 comprehensive quiz and its green/red review cards.
- Kept existing page navigation, lesson pages and the other two homepage challenges unchanged.

## Automated/static checks
- `python -m py_compile app.py`: passed.
- Helper test builds both hidden and revealed Plotly states from a 46-bar synthetic test fixture (used only for testing): hidden state includes 26 candles; revealed state includes all 46; x-axis ranges match and the mask is removed on reveal.
- Finder logic successfully selected a dual-cross event from synthetic test data and returned a complete 20-session post-signal window; this is a logic test, not the market example shown to users.
- Empty-data route in the signal finder returns `None` cleanly.
- ZIP contents and CRC integrity checked after packaging.

## Limits
- The authoring container cannot reach Yahoo Finance and does not have yfinance installed, so the real stock/date selected by the runtime case finder and live download were not executed here.
- No real-browser visual test of Streamlit was possible in this environment. The interaction is verified by source checks and Plotly figure construction tests, but first local launch should be checked while connected to the internet.
