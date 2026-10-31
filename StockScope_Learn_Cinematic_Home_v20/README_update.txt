StockScope Learn — Duplicate Indicator Section Cleanup

What changed / verified:
- The redundant section titled “核心指标逐个学” is absent from app.py.
- The older duplicated tab group for trend, momentum, volatility/volume, price levels and advanced preview is absent from the technical-indicators chapter.
- The single-indicator workflow remains: choose one indicator, view its chart, then read the corresponding full lesson and calculation exercise directly below.
- The compact “指标分类速览” remains collapsed as a brief orientation panel; it is not the duplicate lesson wall. Remove it too only if you prefer no overview at all.

Validation:
- Verified the duplicate heading and old tab labels are not present in app.py.
- Verified the indicator lab and selected-indicator lesson renderer remain present.
- Python syntax compilation passed.
- This is a static source check; it does not replace a full browser run against live Yahoo Finance data.

Installation:
1. Back up your current project.
2. Extract the ZIP into the StockScope Learn project folder and overwrite app.py and start_windows.bat when prompted.
3. Stop any old Streamlit session with Ctrl+C in its terminal, then run start_windows.bat from this same folder.
