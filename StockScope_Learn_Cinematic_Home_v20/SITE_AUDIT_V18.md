# StockScope Learn V18 — Change and QA Notes

## Homepage challenges
1. **01 Price & volume:** fixed NVDA daily window, 2024-11-01 to 2024-12-02 (end date exclusive), retrieved from Yahoo Finance via yfinance. The chart only displays bars on or before 2024-11-21 until the learner submits. It then reveals the following five sessions and calculates the cumulative close-to-close change from the cutoff close to the fifth hidden session close. No synthetic OHLC bars are used for this question.
2. **02 Company & financial statements:** uses NVIDIA's official FY2025 Q3 results released on 2024-11-20. It asks why strong year-over-year results do not prove the stock must rise. Source link is included in the UI.
3. **03 Return & risk:** uses actual one-year adjusted prices from Yahoo Finance / yfinance for NVDA, AAPL and SPY. Table calculates interval return, annualized volatility from daily returns and maximum drawdown from closing prices.

## Comprehensive quiz
- Replaced the 20 questions with scenario-oriented questions based on content taught in the current curriculum: ownership, index/ETF, market cap, OHLC, volume, candlestick context, order types, spread, three statements, cash conversion, P/E, expectations, volatility, max drawdown, diversification, time horizon and investor protection.
- Each item contains four plausible distractors linked to common confusions in these concepts; no off-topic distractors were added.
- No answer is pre-selected; all 20 must be answered before submission.
- Correct-option positions are balanced across A/B/C/D (five each), avoiding a predictable answer-position pattern.
- Results render green whole-question cards for correct answers and red cards for incorrect answers; answer rows mark correct responses green and incorrect selections red.
- Retake resets stored answers and current result.

## Static checks
- `python -m py_compile app.py`: passed.
- Confirmed all final-quiz questions have 4 options and valid answer indices.
- Confirmed final quiz result renderer applies correct/wrong CSS classes.
- Confirmed V18 ZIP contains `app.py`, requirements, Windows launch script, README and audit notes.

## Runtime limitation
Streamlit/Yahoo Finance could not be launched from the authoring environment because the current environment lacks the yfinance dependency. The runtime scenario is wired to the same yfinance history service already used by the rest of the app. Browser-level visual QA and live quote retrieval still need confirmation on the user's machine.
