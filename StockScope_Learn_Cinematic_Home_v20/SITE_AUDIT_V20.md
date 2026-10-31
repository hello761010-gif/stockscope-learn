# StockScope Learn V20 — Change and QA Notes

## Requested UX refinements
- Improved chart legend contrast with a nearly opaque dark background, light outline, white 13px text, stronger indicator line colors, brighter axis tick labels, and larger hover text.
- Added visible legend guidance: candles and volume use green for rising / red for falling; the MACD histogram uses green / red for positive / negative histogram values, not as a direct encoding of price direction.
- Applied a hard historical cutoff at 2026-10-06 before the crossover finder selects a candidate. The selected post-event 20-session window must come from data on or before this cutoff.
- Before submission, display only the observed lead-in on the left and place answer choices in a separate bordered panel on the right, occupying the space reserved for the still-hidden future segment. No crossover labels, event dates, vertical markers, or explicit golden-cross terminology are shown before answering.
- After submission, the answer panel disappears and the same chart renders full width with the real 20-session future section immediately to the right of the visible history. The result and explanation remain below the chart.
- Only after submission are MA5-over-MA20 and DIF-over-DEA dates labeled on their respective chart panels with stronger markers, high-contrast callouts, and full-height vertical date lines.

## Checks performed
- `python -m py_compile app.py`: passed.
- Plotly chart-state test with a synthetic 46-row fixture: before submission the candle trace contains only the 26-bar lead-in; after submission it contains all 46 bars.
- Annotation visibility test: crossover callout labels absent in hidden state and present only after reveal.
- Legend contrast test: white text, size >= 13, dark plot theme; passed.
- Date-cutoff test: data later than 2026-10-06 excluded.
- Pre-answer copy test: no “金叉”, “上穿 MA20”, or “DIF 上穿 DEA” text in the pre-answer UI branch.
- ZIP CRC integrity is checked when packaging.

## Limits
- This container does not have Streamlit or yfinance installed and cannot provide a real browser launch or live Yahoo Finance fetch. The historic candidate and full user interaction must be confirmed on the user's computer with internet access. The app returns a clear warning if it cannot find a qualifying real-data sample instead of synthesizing one.
