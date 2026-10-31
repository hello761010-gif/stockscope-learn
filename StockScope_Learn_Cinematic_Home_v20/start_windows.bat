@echo off
setlocal
cd /d "%~dp0"
title StockScope Learn

echo ================================================
echo StockScope Learn - Technical Indicator Learning
echo ================================================

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11 or newer and try again.
  pause
  exit /b 1
)

REM Streamlit 1.66+ requires Python 3.11+; verify the interpreter before installing packages.
python -c "import sys; assert sys.version_info >= (3, 11)" >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 or newer is required by the current Streamlit release.
  pause
  exit /b 1
)

REM Only install/upgrade packages if imports or required Streamlit APIs are missing.
python -c "import numpy, pandas, plotly, streamlit, yfinance, inspect; apis=(streamlit.button, streamlit.plotly_chart, streamlit.download_button, streamlit.dataframe, streamlit.form_submit_button); assert tuple(int(x) for x in streamlit.__version__.split('.')[:2]) >= (1, 66); assert all('width' in inspect.signature(api).parameters for api in apis)" >nul 2>nul
if errorlevel 1 (
  echo Required libraries are missing or Streamlit is too old. Installing/updating dependencies...
  python -m pip install --upgrade -r requirements.txt
  if errorlevel 1 (
    echo Package installation failed. Check your internet connection and Python environment.
    pause
    exit /b 1
  )
) else (
  echo Dependencies are ready.
)

echo Starting StockScope Learn...
python -m streamlit run app.py
if errorlevel 1 (
  echo Streamlit stopped with an error. Read the message above for details.
  pause
  exit /b 1
)
endlocal
