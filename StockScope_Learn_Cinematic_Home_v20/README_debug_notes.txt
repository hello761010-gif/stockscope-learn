StockScope Learn — UI / Interaction Debug Update

What was fixed
1. Streamlit expander headers (including “MA / EMA｜移动平均线”) now explicitly style the native details/summary header, its open/hover/focus states, its text/icons, and the body. This addresses the root cause where only the outer expander wrapper had been styled and the header could still inherit a light background.
2. Dropdown/popover options use a dark background with high-contrast text for normal, hover, selected and keyboard-focus states.
3. The custom sidebar expand control is now rendered whenever the sidebar is collapsed, including on the home page. Previously, a condition hid the control when the selected page was “学习首页”, making the menu appear impossible to reopen.
4. The clickable chart iframe now uses the app's dark background instead of transparency. The transparent Plotly background previously exposed the iframe's default white canvas and made the axes difficult to read.
5. Clicking a legend item now only opens the corresponding lesson explanation; it no longer hides the line unexpectedly. Display options remain controlled by the Streamlit selectors above the chart.
6. The MACD zero line is now a real trace, so it can be clicked and has its own explanation instead of being an unclickable decorative shape.
7. ADX / DI calculations now treat a zero-directional-movement window as zero after the normal warm-up, rather than leaving the whole ADX series blank due to division by zero.
8. Removed custom wheel/touch forwarding to the host page. That can double-scroll in some Chromium layouts; native browser scroll chaining is used instead.
9. The Windows launcher no longer reinstalls packages every launch. It checks imports and required Streamlit API arguments first, upgrading dependencies only when they are missing or too old.

Tests performed
- Python syntax compile: passed.
- Synthetic flat, rising and falling price series: RSI / stochastic bounds checked; flat-market ADX and DI now resolve to zero after warm-up.
- Plotly figure creation checked for RSI, MACD, Stochastic, ADX, OBV and no-lower-panel modes, with overlays, high/low reference lines and Fibonacci lines enabled.
- Checked that every named trace in these tested configurations has a matching clickable learning guide; MACD zero line is included.
- Chromium test of the generated chart HTML: real Plotly rendering succeeded with no browser JavaScript errors; a legend click updated the guide while the trace remained visible. The visible chart background rendered dark after the fix.
- Chromium CSS test: expander closed, hover, selected/open and popover hover states use dark backgrounds and readable text.

Known verification limit
The execution environment did not have Streamlit or yfinance installed and network access prevented installing them. Therefore the full Streamlit app was not launched end-to-end here. The chart HTML and CSS were tested separately in Chromium, and the Python calculation / figure functions were tested with synthetic data. After replacing the files locally, launch with start_windows.bat to verify live Yahoo Finance loading in your own environment.
