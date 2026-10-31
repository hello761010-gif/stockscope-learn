# StockScope Learn V17 — UI cleanup and chart spacing

## Changes in this build

- Removed the homepage tagline “用数据、纪律和复盘支持判断” and its Pexels / Coverr source-link paragraph.
- Removed raw technical exception panels from the UI; data-fetch failures now show a plain user-facing warning rather than a code-style error box.
- Removed the separate candlestick anatomy explainer, including body / upper-wick / lower-wick cards and the color/direction comparison cards and diagrams. The pattern library and chart-reading lesson remain available.
- Added vertical spacing below “价格与成交量要一起看” and increased the volume chart's top margin to reduce crowding between the section heading and Plotly chart title.
- Kept the homepage video cuts and existing lessons / navigation.

## Validation

- Python syntax compilation passed.
- Confirmed the removed homepage text is absent.
- Confirmed no `st.code(...)` calls remain in `app.py`.
- Confirmed the anatomy explainer labels and unused illustration helper functions are removed.
- ZIP integrity is checked when packaging.
- No real-browser visual test was run in this environment.
