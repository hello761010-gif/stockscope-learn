from __future__ import annotations

from typing import Iterable
from html import escape
import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf


# ============================================================
# Page setup and visual system
# ============================================================
st.set_page_config(
    page_title="StockScope Learn｜股票入门学院",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root {
        --ink: #e9f0fb;
        --muted: #a7b6cc;
        --panel: #141f32;
        --panel-2: #192940;
        --line: rgba(180, 204, 232, .15);
        --mint: #60e2bd;
        --blue: #75b7ff;
        --amber: #ffc777;
        --rose: #ff8f9b;
      }
      .stApp, [data-testid="stAppViewContainer"] {
        background:
          radial-gradient(circle at 78% 0%, rgba(45, 104, 145, .22), transparent 30%),
          radial-gradient(circle at 0% 30%, rgba(41, 112, 102, .12), transparent 28%),
          #0b1220;
        color: var(--ink);
      }
      [data-testid="stHeader"] { background: rgba(11, 18, 32, .78); }
      [data-testid="stMain"] { color: var(--ink); }
      [data-testid="stMarkdownContainer"] { color: var(--ink); }
      [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
      [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
        color: #d4deeb !important;
      }
      /* Force Streamlit expander headers and bodies to stay dark in both open and closed states.
         Styling only the outer wrapper is not enough: Streamlit renders the clickable title as
         a native details/summary region that can otherwise inherit a white theme background. */
      [data-testid="stExpander"] {
        background: rgba(20, 31, 50, .56) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
        overflow: hidden;
      }
      [data-testid="stExpander"] details,
      [data-testid="stExpander"] details > div,
      [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: rgba(15, 26, 43, .96) !important;
        color: #e9f0fb !important;
      }
      [data-testid="stExpander"] details > summary,
      [data-testid="stExpander"] summary {
        background: rgba(20, 31, 50, .98) !important;
        color: #e9f0fb !important;
        border-radius: 11px !important;
        transition: background-color .15s ease, color .15s ease;
      }
      [data-testid="stExpander"] details[open] > summary,
      [data-testid="stExpander"] summary[aria-expanded="true"] {
        background: linear-gradient(100deg, rgba(35, 58, 82, .98), rgba(22, 42, 63, .98)) !important;
        color: #60e2bd !important;
      }
      [data-testid="stExpander"] details > summary:hover,
      [data-testid="stExpander"] summary:hover,
      [data-testid="stExpander"] details > summary:focus-visible,
      [data-testid="stExpander"] details[open] > summary:focus-visible {
        background: #29425f !important;
        color: #ffffff !important;
      }
      [data-testid="stExpander"] details > summary:focus-visible {
        outline: 2px solid #60e2bd !important; outline-offset: -2px;
      }
      [data-testid="stExpander"] summary * {
        color: inherit !important;
        background-color: transparent !important;
      }
      [data-testid="stExpander"] summary svg,
      [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] svg {
        color: inherit !important;
        fill: currentColor !important;
        stroke: currentColor !important;
      }
      [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        background: transparent !important;
        color: #d4deeb !important;
      }
      [data-testid="stTabs"] [data-baseweb="tab-list"] {
        flex-wrap: wrap; gap: .35rem; border-bottom-color: var(--line);
      }
      [data-testid="stTabs"] button[role="tab"] {
        color: #aebed1; border-radius: 10px 10px 0 0;
      }
      [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #60e2bd; border-bottom-color: #60e2bd;
      }
      [data-testid="stDataFrame"], [data-testid="stTable"] { max-width: 100%; }
      [data-testid="stPlotlyChart"] { width:100% !important; max-width:100% !important; min-width:0 !important; }
      [data-testid="stPlotlyChart"] > div { min-width:0 !important; max-width:100% !important; }
      /* Keep every opened select/menu readable on the dark interface, including hover/focus states. */
      [data-baseweb="popover"], [data-baseweb="menu"],
      [role="listbox"], [data-baseweb="popover"] ul {
        background: #111d2e !important; color: #e9f0fb !important;
      }
      [data-baseweb="menu"] li, [role="option"],
      [data-baseweb="popover"] [role="option"],
      [data-baseweb="menu"] [role="menuitem"] {
        background-color: #111d2e !important; color: #e9f0fb !important;
      }
      [role="option"] *, [data-baseweb="menu"] li *,
      [data-baseweb="menu"] [role="menuitem"] * {
        color: inherit !important;
      }
      [role="option"]:hover, [role="option"]:focus,
      [role="option"][aria-selected="true"], [role="option"][data-highlighted="true"],
      [data-baseweb="popover"] [role="option"][aria-selected="true"],
      [data-baseweb="popover"] [role="option"][data-highlighted="true"],
      [data-baseweb="menu"] li:hover, [data-baseweb="menu"] li[aria-selected="true"],
      [data-baseweb="menu"] [role="menuitem"]:hover,
      [data-baseweb="menu"] [role="menuitem"][aria-selected="true"] {
        background-color: #29425f !important; color: #ffffff !important;
      }
      [data-baseweb="popover"] [role="option"]:focus-visible,
      [data-baseweb="menu"] [role="menuitem"]:focus-visible {
        outline: 2px solid #60e2bd !important; outline-offset: -2px;
      }
      [data-baseweb="select"] > div:focus-within,
      [data-baseweb="input"] > div:focus-within {
        background: #111d2e !important; border-color: #60e2bd !important;
        box-shadow: 0 0 0 1px rgba(96,226,189,.32) !important;
      }
      div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(96,226,189,.17), rgba(117,183,255,.13)) !important;
        border-color: rgba(96,226,189,.72) !important; color: #f4f7fc !important;
      }
      div[role="radiogroup"] label > div { background: transparent !important; color: inherit !important; }
      div[role="radiogroup"] label:hover { background: #1b2d45 !important; }
      div[role="radiogroup"] label:has(input:checked) * { color: #f4f7fc !important; background: transparent !important; }
      [data-testid="stTabs"] button[role="tab"] {
        background: rgba(24,39,59,.76) !important; color: #c5d5e8 !important;
      }
      [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: rgba(96,226,189,.12) !important; color: #60e2bd !important;
      }
      [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101a2b 0%, #0d1524 100%);
        border-right: 1px solid var(--line);
      }
      [data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
      .block-container { max-width: 1480px; padding-top: 1.7rem; padding-bottom: 3rem; }
      h1, h2, h3, h4 { letter-spacing: -0.025em; color: #f4f7fc; }
      p, li, label { color: #d4deeb; }
      [data-testid="stCaptionContainer"] p { color: #91a4bd; }
      [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(28, 43, 65, .92), rgba(17, 29, 47, .96));
        border: 1px solid var(--line); border-radius: 16px;
        padding: 1rem 1.1rem; min-height: 112px;
      }
      [data-testid="stMetricLabel"] { color: #9fb2ca !important; }
      [data-testid="stMetricValue"] { color: #f3f7fc !important; font-weight: 700; }
      div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(20, 31, 50, .70); border-color: var(--line) !important; border-radius: 18px;
      }
      div.stButton > button, div.stDownloadButton > button, [data-testid="stFormSubmitButton"] button {
        border-radius: 11px; border: 1px solid rgba(96, 226, 189, .45);
        background: linear-gradient(135deg, #62e2be, #66c9d9); color: #08201f;
        font-weight: 750; min-height: 2.65rem; transition: all .18s ease;
      }
      div.stButton > button:hover, div.stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        border-color: #a9f7df; color: #041b1b; filter: brightness(1.06); transform: translateY(-1px);
      }
      [data-testid="stBaseButton-secondary"] { background: rgba(35, 52, 76, .85) !important; color: #e9f0fb !important; }
      div[data-baseweb="select"] > div, div[data-baseweb="input"] > div,
      div[data-baseweb="textarea"] > div { background: #111d2e; border-color: #31435d; border-radius: 10px; }
      div[role="radiogroup"] { gap: .55rem; flex-wrap: wrap; }
      div[role="radiogroup"] label { background: rgba(24, 39, 59, .78); border: 1px solid var(--line); padding: .68rem .82rem; border-radius: 12px; color:#d4deeb !important; line-height:1.45; }
      div[role="radiogroup"] label:hover { border-color:rgba(96,226,189,.55); }
      div[role="radiogroup"] label:focus-within { outline:2px solid rgba(96,226,189,.75); outline-offset:2px; }
      /* Sidebar navigation selection uses a filled green radio, never Streamlit's default red. */
      [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { accent-color:#22c55e !important; }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        border-color:rgba(34,197,94,.88) !important;
        background:linear-gradient(100deg,rgba(34,197,94,.18),rgba(34,197,94,.08)) !important;
        color:#f4fff7 !important;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child {
        border-color:#22c55e !important;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) [data-baseweb="radio"] > div:first-child > div {
        background:#22c55e !important; background-color:#22c55e !important;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) [role="radio"][aria-checked="true"] svg circle,
      [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) svg circle {
        fill:#22c55e !important; stroke:#22c55e !important;
      }
      /* The financial-statement selector is a prominent three-card navigation area. */
      .statement-nav-card { min-height:156px; padding:1.05rem 1rem; border:1px solid rgba(158,184,214,.25); border-radius:16px; background:linear-gradient(150deg,rgba(24,40,61,.96),rgba(13,25,41,.98)); margin:.25rem 0 .65rem; }
      .statement-nav-card.is-active { border:1px solid rgba(96,226,189,.85); background:linear-gradient(145deg,rgba(96,226,189,.14),rgba(117,183,255,.10)); box-shadow:inset 0 0 0 1px rgba(96,226,189,.12),0 10px 26px rgba(0,0,0,.10); }
      .statement-nav-number { font-size:.72rem; font-weight:600; letter-spacing:.06em; color:#aab8ca; margin-bottom:.5rem; }
      .statement-nav-title { font-size:1.12rem; font-weight:850; color:#f2f6fb; margin-bottom:.45rem; }
      .statement-nav-question { color:#e0ebf8; font-size:.98rem; font-weight:750; margin-bottom:.55rem; line-height:1.45; }
      .statement-nav-copy { color:#aebed1; font-size:.86rem; line-height:1.55; }
      @media (max-width: 760px) { .statement-nav-card { min-height:unset; } }
      [data-testid="stCheckbox"] label:focus-within { outline:2px solid rgba(96,226,189,.75); outline-offset:2px; border-radius:6px; }
      [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #60e2bd, #75b7ff); }
      .brand-row { display:flex; gap:12px; align-items:center; padding: 0 .25rem 1.1rem .25rem; }
      .brand-mark { width:42px;height:42px;display:flex;align-items:center;justify-content:center;border-radius:14px;
        background:linear-gradient(145deg,#62e2be,#75b7ff); color:#09202c;font-size:22px;font-weight:900;box-shadow:0 8px 26px rgba(88,211,195,.16); }
      .brand-name { font-weight:850; font-size:1.13rem; color:#f5f8fc; line-height:1.1; }
      .brand-sub { font-size:.72rem; color:#91a4bd; margin-top:4px; letter-spacing:.11em; text-transform:uppercase; }
      .eyebrow { color:var(--mint); letter-spacing:.16em; text-transform:uppercase; font-size:.72rem; font-weight:800; margin-bottom:.55rem; }
      .hero { position:relative; isolation:isolate; overflow:hidden; padding:2.2rem 2.25rem; border-radius:26px;
        border:1px solid rgba(164,204,232,.18); background:linear-gradient(118deg,rgba(27,55,78,.98) 0%,rgba(20,38,62,.98) 47%,rgba(31,55,78,.95) 100%);
        box-shadow:0 22px 60px rgba(0,0,0,.16); }
      .hero:after { content:""; position:absolute; z-index:0; pointer-events:none; width:360px;height:360px;right:-80px;top:-170px;border-radius:50%;
        border:1px solid rgba(96,226,189,.19); box-shadow:0 0 0 32px rgba(96,226,189,.035),0 0 0 70px rgba(117,183,255,.025); }
      .hero > * { position:relative; z-index:1; }
      .hero h1 { font-size:clamp(2.15rem,4vw,3.55rem); line-height:1.08; margin:0 0 1rem 0; max-width:820px; }
      .hero p { color:#c5d5e8; font-size:1.02rem; max-width:760px; line-height:1.7; margin-bottom:1.15rem; }
      .section-kicker { color:var(--mint);font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.3rem; }
      .section-title { color:#f2f6fb;font-size:1.55rem;font-weight:800;letter-spacing:-.03em;margin-bottom:.35rem; }
      .section-desc { color:#9fb2ca;line-height:1.6;margin-bottom:1.2rem; }
      .lesson-card { height:100%; background:linear-gradient(150deg,rgba(27,42,63,.94),rgba(16,27,44,.98));border:1px solid var(--line);border-radius:18px;padding:1.2rem 1.25rem; }
      .cycle-card { min-height: 148px; height:100%; padding: .9rem .95rem; border-radius: 14px; border: 1px solid var(--line); background: linear-gradient(150deg, rgba(27,42,63,.88), rgba(16,27,44,.95)); }
      .cycle-num { color: var(--mint); font-size: .72rem; letter-spacing: .12em; font-weight: 850; margin-bottom: .45rem; }
      .cycle-title { color: #f2f6fb; font-size: .85rem; font-weight: 800; margin-bottom: .45rem; }
      .cycle-body { color: #aebed1; font-size: .78rem; line-height: 1.5; }
      @media (max-width: 760px) { .cycle-card { min-height: unset; padding: .85rem; } }
      .lesson-top { display:flex;align-items:center;justify-content:space-between;margin-bottom:.9rem; }
      .lesson-icon { width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:rgba(96,226,189,.11);border:1px solid rgba(96,226,189,.16);border-radius:13px;font-size:1.25rem; }
      .lesson-no { color:#8298b4;font-size:.74rem;font-weight:800;letter-spacing:.12em; }
      .lesson-title { font-size:1.05rem;font-weight:800;color:#f2f6fb;margin-bottom:.45rem; }
      .lesson-text { font-size:.88rem;line-height:1.65;color:#aebed1;min-height:4.2rem; }
      .tag { display:inline-block;padding:5px 9px;border-radius:999px;background:rgba(117,183,255,.11);border:1px solid rgba(117,183,255,.17);color:#9ecbff;font-size:.72rem;font-weight:700; }
      .info-card { background:rgba(21,34,53,.88);border:1px solid var(--line);border-radius:16px;padding:1rem 1.1rem;height:100%; }
      .info-card h4 { margin:.35rem 0 .5rem;font-size:1rem; }
      .info-card p { color:#aebed1;font-size:.89rem;line-height:1.65;margin-bottom:0; }
      .ohlc-sample-card { gap:.35rem; }
      .ohlc-line { display:flex; flex-wrap:wrap; align-items:baseline; justify-content:space-between; gap:.25rem .65rem; padding:.52rem .6rem; margin-top:.18rem; background:rgba(117,183,255,.07); border:1px solid rgba(117,183,255,.14); border-radius:9px; font-size:.78rem; line-height:1.4; }
      .ohlc-line span { color:#b9c8da; }
      .ohlc-line b { color:#f3f7fc; font-size:.85rem; white-space:nowrap; }
      .callout { border-left:3px solid var(--mint);background:rgba(96,226,189,.07);padding:.85rem 1rem;border-radius:0 12px 12px 0;color:#c9d9e8;line-height:1.65; }
      .scenario-intro {display:flex;align-items:flex-start;gap:.85rem;margin-bottom:.8rem;}
      .scenario-index {flex:0 0 46px;width:46px;height:46px;display:grid;place-items:center;border-radius:14px;
        background:rgba(96,226,189,.11);border:1px solid rgba(96,226,189,.32);color:#75e8cd;font-weight:900;letter-spacing:.04em;}
      .scenario-title {font-size:1.12rem;font-weight:850;color:#f3f7fc;line-height:1.35;margin-bottom:.28rem;}
      .scenario-subtitle {font-size:.84rem;color:#aebed1;line-height:1.55;}
      .scenario-source {font-size:.76rem;color:#9eb1c7;line-height:1.6;margin-top:.6rem;}
      .scenario-source a {color:#8fdccf !important;}
      .scenario-indicator-legend {display:flex;gap:.8rem;flex-wrap:wrap;margin:.25rem 0 .8rem;color:#b9c8da;font-size:.82rem;}
      .scenario-color-key {font-size:.92rem;line-height:1.9;color:#f1f5f9;}
      .color-pill {display:inline-block;padding:.14rem .55rem;border-radius:999px;font-weight:900;letter-spacing:.01em;white-space:nowrap;}
      .color-up {background:#14532d;color:#dcfce7;border:1px solid #4ade80;}
      .color-down {background:#7f1d1d;color:#ffe4e6;border:1px solid #fb7185;}
      .color-key-line {font-weight:900;text-shadow:0 1px 2px #020617;}
      .scenario-color-note {display:inline-block;margin-top:.25rem;color:#dbe6f4;font-size:.82rem;}
      .scenario-choice-panel h3 {color:#f8fafc;font-size:1.2rem;margin-top:.1rem;}
      .quiz-review-card {border:1px solid rgba(160,180,205,.2);border-radius:16px;padding:1rem 1.1rem;margin:.85rem 0;background:rgba(18,29,46,.75);}
      .quiz-review-card.quiz-correct {border-color:rgba(78,202,139,.78);background:linear-gradient(145deg,rgba(35,105,72,.24),rgba(18,39,43,.76));box-shadow:inset 4px 0 0 #4eca8b;}
      .quiz-review-card.quiz-incorrect {border-color:rgba(255,111,125,.78);background:linear-gradient(145deg,rgba(130,45,58,.25),rgba(41,27,42,.76));box-shadow:inset 4px 0 0 #ff6f7d;}
      .quiz-review-head {display:flex;justify-content:space-between;align-items:flex-start;gap:.8rem;margin-bottom:.65rem;}
      .quiz-review-title {font-size:1rem;font-weight:800;color:#f4f7fb;line-height:1.5;}
      .quiz-review-status {flex:0 0 auto;border-radius:999px;font-size:.72rem;font-weight:850;padding:.3rem .55rem;}
      .quiz-review-card.quiz-correct .quiz-review-status {background:rgba(78,202,139,.16);color:#7be5ab;border:1px solid rgba(78,202,139,.42);}
      .quiz-review-card.quiz-incorrect .quiz-review-status {background:rgba(255,111,125,.15);color:#ff9aa5;border:1px solid rgba(255,111,125,.42);}
      .quiz-review-option {display:flex;align-items:flex-start;gap:.55rem;padding:.58rem .7rem;border:1px solid rgba(160,180,205,.12);border-radius:10px;margin:.42rem 0;color:#c8d5e5;font-size:.86rem;line-height:1.5;background:rgba(10,19,32,.22);}
      .quiz-review-option .option-marker {font-weight:900;flex:0 0 1.2rem;color:#aebed1;}
      .quiz-review-option.answer-correct {border-color:rgba(78,202,139,.65);background:rgba(44,140,91,.17);color:#c9f8dc;}
      .quiz-review-option.answer-correct .option-marker {color:#73e6a5;}
      .quiz-review-option.answer-wrong {border-color:rgba(255,111,125,.72);background:rgba(170,55,70,.18);color:#ffd1d5;}
      .quiz-review-option.answer-wrong .option-marker {color:#ff8f9a;}
      .quiz-review-explanation {margin-top:.75rem;color:#d5e0ed;font-size:.88rem;line-height:1.7;}
      @media (max-width: 760px) { .quiz-review-head {flex-direction:column;gap:.35rem;} .quiz-review-card {padding:.85rem;} }
      .warning-callout { border-left:3px solid var(--amber);background:rgba(255,199,119,.07);padding:.85rem 1rem;border-radius:0 12px 12px 0;color:#dfd3c0;line-height:1.65; }
      .step-line { display:flex;gap:12px;align-items:flex-start;margin:.4rem 0 1rem 0; }
      .step-num { flex:0 0 30px;width:30px;height:30px;border-radius:10px;background:rgba(96,226,189,.13);color:var(--mint);display:flex;align-items:center;justify-content:center;font-weight:850; }
      .step-body { color:#b9c8da;line-height:1.55; }
      .step-body b { color:#f3f7fc; }
      /* Lesson 4 data uses the same normal text hierarchy as the rest of the site. */
      [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:.45rem; }
      [data-testid="stTabs"] button[role="tab"] { padding:.6rem .9rem; white-space:normal; }
      hr { border-color:rgba(180,204,232,.13) !important; }
      footer { visibility:hidden; }
      @media (max-width: 760px) {
        .block-container { padding-top:1rem; padding-left:1rem; padding-right:1rem; }
        .hero { padding:1.35rem 1.2rem;border-radius:20px; }
        .hero h1 { font-size:2rem; }
        .hero p { font-size:.92rem; }
        [data-testid="stHorizontalBlock"] { flex-wrap:wrap; gap:.8rem; }
        [data-testid="column"] { min-width:100% !important; flex:1 1 100% !important; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Data and learning content
# ============================================================
TICKERS: dict[str, str] = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "AMD": "AMD",
    "TSLA": "Tesla",
    "JPM": "JPMorgan Chase",
    "WMT": "Walmart",
    "COST": "Costco",
    "KO": "Coca-Cola",
    "XOM": "Exxon Mobil",
    "LLY": "Eli Lilly",
    "SPY": "S&P 500 ETF 代理",
    "QQQ": "Nasdaq-100 ETF 代理",
    "EFA": "发达市场 ETF 代理",
    "EEM": "新兴市场 ETF 代理",
    "EWJ": "日本股票 ETF 代理",
    "FXI": "中国大型股 ETF 代理",
    "BND": "Vanguard Total Bond Market ETF（美国综合债券）",
    "SGOV": "iShares 0-3 Month Treasury Bond ETF（美国短期国债）",
}

PERIODS = {
    "5d": "最近 5 天",
    "1mo": "最近 1 个月",
    "3mo": "最近 3 个月",
    "6mo": "最近 6 个月",
    "1y": "最近 1 年",
    "5y": "近 5 年",
    "10y": "近 10 年",
    "max": "尽可能长的历史",
}

# Original StockScope lesson plan inspired by the public instructional structure of
# IBKR Traders' Academy (sequenced beginner courses, short lesson units, examples,
# practice checks, and progress tracking). Lesson text and exercises below are
# independently written for this student project.
LESSON_GUIDE = {
    "股票市场基础": {
        "time": "约 10–12 分钟",
        "objective": "解释股票的所有权含义，区分一级市场与二级市场，理解市场参与者、价格形成、投资回报和核心风险。",
        "learn": "从公司为什么发行股份开始，依次理解市场角色、股票与其他投资工具的差别。",
        "explore": "通过互动例子计算市值、持股比例与简单总回报，建立数字直觉。",
        "practice": "完成本课检查题，并用价格、股数和风险三个维度解释判断。",
        "reflect": "如果有人只看每股价格就说一家公司更贵，你会用什么信息纠正这个判断？",
    },
    "看懂行情": {
        "time": "约 8–10 分钟",
        "objective": "辨认 K 线的 OHLC 四个价格，解释成交量，并知道图表不能单独证明未来涨跌。",
        "learn": "先认识开盘、最高、最低、收盘和成交量的定义。",
        "explore": "选择一只证券，在 K 线和成交量柱中悬停，比较不同日期。",
        "practice": "判断成交量突然放大意味着什么；不确定时可重新尝试。",
        "reflect": "读一张 K 线图时，除了颜色，你还应该检查哪些信息？",
    },
    "蜡烛图形态学": {
        "time": "约 15–25 分钟",
        "objective": "辨认常见单根、双根、三根及持续形态，说明形态需要趋势背景、位置和后续确认，不能单独预测涨跌。",
        "learn": "先理解实体、上影线、下影线与比例，再按单根、组合和持续形态分类学习。",
        "explore": "切换形态查看合成示意 K 线，再到真实历史价格图中尝试辨认结构。",
        "practice": "完成形态与背景判断题，答错后查看对应解释并重新尝试。",
        "reflect": "看到一个熟悉的形态时，你还需要核实哪三类背景信息？",
    },
    "技术指标入门": {
        "time": "约 25–35 分钟",
        "objective": "理解 MA/SMA、EMA、RSI、MACD、随机指标、布林带、ADX 与 OBV 的用途和局限，并认识支撑阻力、斐波那契回撤、VWAP 与一目均衡表。",
        "learn": "先认识每种工具想回答的问题，再理解计算思路、常见参数、读法与误区。",
        "explore": "在真实历史 K 线中切换叠加线和副图，比较信号、趋势背景和可能失效的情况。",
        "practice": "用图表证据回答情境题，区分趋势方向、动能强弱、波动变化和量价线索。",
        "reflect": "这张图里哪些证据来自相同的价格数据？哪些仍需要独立核实？",
    },
    "交易如何执行": {
        "time": "约 8–10 分钟",
        "objective": "描述一笔交易的主要步骤，并区分市价单、限价单和止损单的取舍。",
        "learn": "按交易流程逐步学习证券、券商、订单、费用和成交记录。",
        "explore": "用虚构的买卖报价计算买卖价差，比较价格控制与成交优先级。",
        "practice": "选择适合情境的订单思路，并阅读关于成交不确定性的解析。",
        "reflect": "为什么限价单可以控制可接受价格，却不能保证成交？",
    },
    "研究一家公司": {
        "time": "约 15–20 分钟",
        "objective": "像侦探一样从商业模式、三张财报、关键指标和可靠来源拼出一家公司，而不是背诵一串数字。",
        "learn": "先用熟悉的生意理解收入、成本和利润，再逐张认识损益表、资产负债表与现金流量表。",
        "explore": "用虚构但数字一致的公司案例观察财报之间的联系，再调整指标输入看结果如何变化。",
        "practice": "侦查营收增长但现金流下降的案例，选择下一步最值得核实的证据。",
        "reflect": "哪项证据最改变你对这家公司的看法？还缺少什么信息？",
    },
    "股价为什么变化": {
        "time": "约 6–8 分钟",
        "objective": "区分公司、行业、宏观和市场层面的影响因素，并避免把同时发生误认为因果。",
        "learn": "学习业绩、利率、预期、竞争、流动性和突发事件等因素。",
        "explore": "观察案例中的实际业绩、原先预期和未来指引之间的差异。",
        "practice": "解释为什么利润增长时股价仍可能下跌。",
        "reflect": "如果股价在一则新闻后上涨，还需要哪些证据才能解释原因？",
    },
    "风险与投资者保护": {
        "time": "约 6–8 分钟",
        "objective": "识别常见市场风险、行为偏差和投资诈骗的警示信号，并知道在哪里核实信息。",
        "learn": "阅读风险地图、账户安全建议和常见骗局特征。",
        "explore": "使用投资前自查清单逐项检查一个假设情境。",
        "practice": "判断一个承诺高回报并催促转账的社交媒体投资群是否安全。",
        "reflect": "在做出一项投资前，你会核实哪三个信息？",
    },
}



def ticker_label(symbol: str) -> str:
    return f"{symbol} · {TICKERS.get(symbol, symbol)}"


@st.cache_data(ttl=1800, show_spinner=False)
def load_prices(tickers: tuple[str, ...], period: str) -> pd.DataFrame:
    """Download daily adjusted OHLCV history via yfinance for learning/analysis prototype."""
    cols = ["date", "ticker", "open", "high", "low", "close", "volume"]
    if not tickers:
        return pd.DataFrame(columns=cols)

    raw = yf.download(
        tickers=list(tickers),
        period=period,
        interval="1d",
        auto_adjust=True,
        group_by="ticker",
        progress=False,
        threads=True,
        timeout=20,
    )
    if raw is None or raw.empty:
        return pd.DataFrame(columns=cols)

    frames: list[pd.DataFrame] = []
    fields = {"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}
    for symbol in tickers:
        if isinstance(raw.columns, pd.MultiIndex):
            level0 = raw.columns.get_level_values(0)
            level1 = raw.columns.get_level_values(1)
            if symbol in level0:
                one = raw[symbol].copy()
            elif symbol in level1:
                one = raw.xs(symbol, axis=1, level=1).copy()
            else:
                continue
        elif len(tickers) == 1:
            one = raw.copy()
        else:
            continue

        rename: dict[str, str] = {}
        for original, target in fields.items():
            found = next((c for c in one.columns if str(c).lower() == original.lower()), None)
            if found is not None:
                rename[found] = target
        one = one.rename(columns=rename)
        if "close" not in one.columns:
            continue
        for col in ["open", "high", "low", "close", "volume"]:
            if col not in one.columns:
                one[col] = np.nan
        idx = pd.DatetimeIndex(one.index)
        if idx.tz is not None:
            idx = idx.tz_localize(None)
        one = one[["open", "high", "low", "close", "volume"]].copy()
        one["date"] = idx
        one["ticker"] = symbol
        frames.append(one.reset_index(drop=True))

    if not frames:
        return pd.DataFrame(columns=cols)
    result = pd.concat(frames, ignore_index=True)
    for c in ["open", "high", "low", "close", "volume"]:
        result[c] = pd.to_numeric(result[c], errors="coerce")
    result = result.dropna(subset=["close"]).sort_values(["ticker", "date"]).reset_index(drop=True)
    return result[cols]


def safe_prices(tickers: Iterable[str], period: str) -> tuple[pd.DataFrame, str | None]:
    try:
        data = load_prices(tuple(dict.fromkeys(tickers)), period)
        if data.empty:
            return data, "行情接口没有返回数据。请检查网络，或稍后刷新。"
        return data, None
    except Exception as exc:
        return pd.DataFrame(columns=["date", "ticker", "open", "high", "low", "close", "volume"]), str(exc)







def find_dual_golden_cross_case(data: pd.DataFrame, future_bars: int = 20, max_gap: int = 3) -> dict | None:
    """Find a real daily-price window where MA5 crosses above MA20 and MACD crosses above its signal line nearby.

    The source dataframe must contain Yahoo Finance adjusted daily OHLCV rows in the app's normalized schema.
    It selects a historical event with enough subsequent sessions for an honest reveal exercise.
    """
    if data is None or data.empty:
        return None

    candidates: list[dict] = []
    required_symbols = ("NVDA", "AAPL", "MSFT", "AMD", "SPY", "QQQ")
    for symbol in required_symbols:
        frame = data.loc[data["ticker"] == symbol].copy().sort_values("date").reset_index(drop=True)
        if len(frame) < 90:
            continue
        close = pd.to_numeric(frame["close"], errors="coerce")
        frame["ma5"] = close.rolling(5, min_periods=5).mean()
        frame["ma20"] = close.rolling(20, min_periods=20).mean()
        ema12 = close.ewm(span=12, adjust=False, min_periods=12).mean()
        ema26 = close.ewm(span=26, adjust=False, min_periods=26).mean()
        frame["macd"] = ema12 - ema26
        frame["macd_signal"] = frame["macd"].ewm(span=9, adjust=False, min_periods=9).mean()
        frame["macd_hist"] = frame["macd"] - frame["macd_signal"]

        ma_cross = (frame["ma5"] > frame["ma20"]) & (frame["ma5"].shift(1) <= frame["ma20"].shift(1))
        macd_cross = (frame["macd"] > frame["macd_signal"]) & (frame["macd"].shift(1) <= frame["macd_signal"].shift(1))
        ma_indices = np.flatnonzero(ma_cross.fillna(False).to_numpy())
        macd_indices = np.flatnonzero(macd_cross.fillna(False).to_numpy())

        for ma_idx in ma_indices:
            nearby_macd = [int(idx) for idx in macd_indices if abs(int(idx) - int(ma_idx)) <= max_gap]
            for macd_idx in nearby_macd:
                anchor_idx = max(int(ma_idx), int(macd_idx))
                # Reserve the full post-signal window; do not accidentally reveal partial/incomplete examples.
                if anchor_idx < 60 or anchor_idx + future_bars >= len(frame):
                    continue
                candidates.append({
                    "ticker": symbol,
                    "data": frame,
                    "anchor_idx": anchor_idx,
                    "ma_cross_idx": int(ma_idx),
                    "macd_cross_idx": int(macd_idx),
                    "gap": abs(int(ma_idx) - int(macd_idx)),
                    "date": pd.Timestamp(frame.iloc[anchor_idx]["date"]),
                })

    if not candidates:
        return None
    # Prefer the most recent usable historical example; when event dates tie, prefer the closest crossover pair.
    return max(candidates, key=lambda item: (item["date"], -item["gap"]))




@st.cache_data(ttl=86400, show_spinner=False)
def load_dual_golden_cross_case() -> dict | None:
    """Fetch five years of real Yahoo Finance daily history and select a double-bullish-crossover case."""
    symbols = ("NVDA", "AAPL", "MSFT", "AMD", "SPY", "QQQ")
    raw = load_prices(symbols, "5y")
    if raw is None or raw.empty:
        return None
    # Keep the exercise strictly historical and stop the visible/revealed window by 2026-10-06.
    cutoff = pd.Timestamp("2026-10-06")
    raw = raw.loc[pd.to_datetime(raw["date"]).dt.tz_localize(None) <= cutoff].copy()
    return find_dual_golden_cross_case(raw, future_bars=20, max_gap=3)


def dual_signal_figure(
    case_window: pd.DataFrame,
    x_end: pd.Timestamp,
    reveal_future: bool,
    ma_cross_date: pd.Timestamp,
    macd_cross_date: pd.Timestamp,
    height: int = 700,
) -> go.Figure:
    """Build a continuous 3-panel price/volume/MACD chart; reveal arrow-free signal labels after an answer."""
    data = case_window.copy().sort_values("date").reset_index(drop=True)
    visible_data = data.copy() if reveal_future else data.loc[data["is_future"] == False].copy()

    # Keep the panels clean: chart context is explained by the legend and axes, not duplicate titles.
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.035,
        row_heights=[0.61, 0.15, 0.24],
    )
    candle_up = "#22c55e"   # Green = up
    candle_down = "#ef4444" # Red = down
    fig.add_trace(go.Candlestick(
        x=visible_data["date"], open=visible_data["open"], high=visible_data["high"],
        low=visible_data["low"], close=visible_data["close"], name="K线（绿涨红跌）",
        increasing_line_color=candle_up, decreasing_line_color=candle_down,
        increasing_fillcolor=candle_up, decreasing_fillcolor=candle_down,
        whiskerwidth=0.55,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=visible_data["date"], y=visible_data["ma5"], mode="lines", name="MA5（5日移动均线）",
        line=dict(color="#ffbf47", width=2.7), connectgaps=False,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=visible_data["date"], y=visible_data["ma20"], mode="lines", name="MA20（20日移动均线）",
        line=dict(color="#55b8ff", width=2.7), connectgaps=False,
    ), row=1, col=1)

    volume_colors = [candle_up if float(c) >= float(o) else candle_down
                     for o, c in zip(visible_data["open"], visible_data["close"])]
    fig.add_trace(go.Bar(
        x=visible_data["date"], y=visible_data["volume"], name="成交量（绿涨红跌）",
        marker_color=volume_colors, opacity=0.9,
    ), row=2, col=1)

    macd_hist_colors = [candle_up if float(v) >= 0 else candle_down for v in visible_data["macd_hist"].fillna(0)]
    fig.add_trace(go.Bar(
        x=visible_data["date"], y=visible_data["macd_hist"], name="MACD柱（柱状图；正值绿／负值红）",
        marker_color=macd_hist_colors, opacity=0.88,
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=visible_data["date"], y=visible_data["macd"], mode="lines", name="DIF（差离值／快线）",
        line=dict(color="#d4c1ff", width=2.8), connectgaps=False,
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=visible_data["date"], y=visible_data["macd_signal"], mode="lines", name="DEA（信号线）",
        line=dict(color="#ffcf5a", width=2.4), connectgaps=False,
    ), row=3, col=1)

    first_date = pd.Timestamp(data.iloc[0]["date"])
    last_date = pd.Timestamp(x_end)
    # Before submit, show only the observed lead-in in the left column; the answer panel occupies
    # the space where the future section will appear. After submit, the same chart widens and
    # the real future candles append to the right without a placeholder or break.
    chart_end = last_date if reveal_future else pd.Timestamp(visible_data.iloc[-1]["date"])

    # Signal markers and labels deliberately appear only after the learner submits an answer.
    if reveal_future:
        for event_date, trace_name, row_no, y_key, color, symbol, label in [
            (pd.Timestamp(ma_cross_date), "MA5（5日移动均线）上穿 MA20（20日移动均线）", 1, "ma5", "#ffbf47", "triangle-up", "MA5（5日移动均线）上穿<br>MA20（20日移动均线）"),
            (pd.Timestamp(macd_cross_date), "DIF（差离值／快线）上穿 DEA（信号线）", 3, "macd", "#d4c1ff", "diamond", "DIF（差离值／快线）上穿 DEA（信号线）"),
        ]:
            event_row = data.loc[data["date"] == event_date]
            if event_row.empty:
                continue
            event_y = float(event_row.iloc[0][y_key])
            fig.add_trace(go.Scatter(
                x=event_row["date"], y=event_row[y_key], mode="markers", name=trace_name,
                marker=dict(color=color, size=16, symbol=symbol, line=dict(color="#07111f", width=2)),
                hovertemplate=f"%{{x|%Y-%m-%d}}<br>{trace_name}<extra></extra>",
            ), row=row_no, col=1)
            # Put a high-contrast label directly on the panel where the event occurs.
            fig.add_annotation(
                x=event_date, y=event_y, row=row_no, col=1, text=label,
                showarrow=False,
                xshift=28 if row_no == 1 else 20,
                yshift=78 if row_no == 1 else -46,
                bgcolor="rgba(7,17,31,.98)", bordercolor=color, borderwidth=1.5,
                borderpad=6, font=dict(size=13, color="#ffffff"), align="left",
            )
        for event_date, color, dash in [
            (pd.Timestamp(ma_cross_date), "#ffbf47", "dot"),
            (pd.Timestamp(macd_cross_date), "#c4b5fd", "dash"),
        ]:
            fig.add_shape(
                type="line", xref="x", yref="paper", x0=event_date, x1=event_date, y0=0, y1=1,
                line=dict(color=color, width=2, dash=dash), layer="above",
            )

    fig.update_layout(
        template="plotly_dark",
        title=None,
        height=height, hovermode="x unified", margin=dict(l=25, r=24, t=108, b=38),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.025, xanchor="left", x=0,
            font=dict(size=12, color="#ffffff"),
            bgcolor="rgba(5,12,24,.98)", bordercolor="#8ba2bd", borderwidth=1.5,
        ),
        barmode="overlay", xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f1f5f9", family="Microsoft YaHei, Noto Sans CJK SC, PingFang SC, Arial, sans-serif", size=13),
        hoverlabel=dict(bgcolor="#0f1c2e", font_color="#ffffff", font_size=13, bordercolor="#8ba2bd"),
    )
    fig.update_xaxes(
        range=[first_date - pd.Timedelta(days=1), chart_end + pd.Timedelta(days=2)],
        rangeslider_visible=False, showgrid=True, gridcolor="rgba(180,204,232,.15)",
        linecolor="rgba(180,204,232,.35)", tickfont=dict(color="#dce7f5", size=11),
    )
    fig.update_yaxes(title_text="价格（美元）", row=1, col=1, gridcolor="rgba(180,204,232,.15)", tickfont=dict(color="#dce7f5", size=11))
    fig.update_yaxes(title_text="成交量", tickformat="~s", row=2, col=1, gridcolor="rgba(180,204,232,.15)", tickfont=dict(color="#dce7f5", size=11))
    fig.update_yaxes(title_text="DIF / DEA", row=3, col=1, zeroline=True, zerolinecolor="rgba(180,204,232,.38)", gridcolor="rgba(180,204,232,.15)", tickfont=dict(color="#dce7f5", size=11))
    return fig


def render_technical_indicator_lesson(choice: str) -> None:
    """Render the concise explanation for one selected indicator."""
    lessons: dict[str, tuple[str, str]] = {
        "仅显示 K 线": (
            "先看价格，再选择需要回答的问题",
            r"""
K 线展示开盘、最高、最低和收盘价。先观察价格整体向上、向下还是横向移动，再决定是否需要指标；指标只是重新整理已有的价格或成交量信息。

| 想了解什么？ | 可选工具 |
|---|---|
| 平均价格方向 | MA、EMA |
| 涨跌动能 | RSI、MACD、随机指标 |
| 波动范围 | 布林带 |
| 趋势强弱 | ADX |
| 量价是否同步 | OBV |
| 重要价格区域 | 支撑阻力、斐波那契回撤 |
""",
        ),
        "MA｜简单移动平均线（MA5 / MA20）": (
            "MA / SMA｜移动平均线：观察平均价格的方向",
            r"""
**它能做什么？** MA（简单移动平均线）把最近若干根 K 线的收盘价平滑成一条线，帮助观察价格方向和当前价格相对平均水平的位置。

**怎么看？**
- **看斜率：** 向上表示平均价格在上移，向下表示下移，走平则表示变化较小。
- **看价格位置：** 价格在均线上方或下方只能作为参考，不代表一定会回到均线。
- **看两线关系：** MA5 比 MA20 反应快。短线向上穿过长线称为金叉，向下穿过称为死叉。
- **选对周期：** 周期短，反应快但噪声较多；周期长，较平滑但转向较慢。

""",
        ),
        "EMA｜指数移动平均线（EMA12 / EMA26）": (
            "EMA｜指数移动平均线：对近期价格反应更快",
            r"""
**它能做什么？** EMA 与 MA 一样用于观察趋势，但近期价格影响更大，因此同周期下通常比 MA 更贴近最新走势。

**怎么看？** 观察 EMA 的方向、价格位于线的哪一侧，以及 EMA12（较快）与 EMA26（较慢）之间的距离。两线分开表示差距扩大，逐渐靠近则表示差距缩小；交叉只是历史价格关系改变的提示。

**参数怎么选？** 周期越短，反应通常越快，也更容易受短期波动影响。EMA12、EMA26 也是 MACD 的常见默认设置。

""",
        ),
        "布林带（20, 2）": (
            "布林带｜观察价格位置和波动范围",
            r"""
**它能做什么？** 布林带由中轨、上轨和下轨组成。常见设置是 20 期中轨及上下各 2 倍标准差的范围，可同时观察价格位置与近期波动变化。

**怎么看？**
- **带宽扩大：** 近期波动范围变宽，但不说明方向一定向上。
- **带宽收窄：** 波动较平静，之后可能出现较大变化，但无法单凭带宽猜中突破方向。
- **靠近上轨 / 下轨：** 表示价格相对近期平均水平偏高 / 偏低；强趋势中价格可能沿轨道运行。
- **回到中轨：** 表示价格回到平均水平附近，不代表必然反转。

例如中轨为 100 美元、上下轨分别为 110 和 90 美元时，图上的范围是 90–110 美元。若波动增加，带子通常会变宽。

""",
        ),
        "RSI（14）": (
            "RSI｜相对强弱指标：观察近期涨跌动能",
            r"""
**它能做什么？** RSI 把近期上涨与下跌的幅度关系转换成 0–100 的读数。这里的“相对强弱”是同一只证券近期涨跌的比较，不是与其他股票的表现排名。

**怎么看？**
- **70 以上：** 常用作超买参考，表示近期上涨动能较强，不代表马上下跌。
- **30 以下：** 常用作超卖参考，表示近期下跌动能较强，不代表马上反弹。
- **50 附近：** 可辅助观察动能处于中间水平的哪一侧。
- **背离：** 价格创出新高 / 新低而 RSI 没有同步跟随，值得留意，但不能单凭背离认定反转。

""",
        ),
        "MACD（12, 26, 9）": (
            "MACD｜观察快慢均线关系与动能变化",
            r"""
**它能做什么？** MACD 通过比较快慢 EMA，并平滑两者差值，帮助观察趋势背景和动能变化。它依据价格计算，不是成交量指标。

**先认识三部分：**
- **DIF（MACD 线）：** 反映快慢 EMA 的差距。
- **DEA（信号线）：** 对 DIF 再做平滑，用来观察 DIF 的变化。
- **柱体：** 显示 DIF 与 DEA 的距离；本网站使用未乘以 2 的版本。

**怎么看？** DIF 上穿 DEA 是向上交叉，下穿是向下交叉；DIF 位于零轴上方时，快 EMA 高于慢 EMA。柱体变长表示两线距离扩大，缩短表示两线靠近。

""",
        ),
        "随机指标（Stochastic）": (
            "随机指标｜看收盘价在近期高低区间的位置",
            r"""
**它能做什么？** 随机指标关注收盘价在近期最高价与最低价区间中的相对位置，通常显示为 0–100 的 %K 与较平滑的 %D。

**怎么看？**
- **80 附近或以上：** 收盘价接近近期区间高端，常称为超买参考区。
- **20 附近或以下：** 收盘价接近近期区间低端，常称为超卖参考区。
- **%K 与 %D 交叉：** 可观察短期区间动能是否改变，还要检查趋势和发生位置。

RSI 比较近期涨跌幅度，随机指标则强调收盘价在高低区间的位置，两者相关但并不相同。

""",
        ),
        "ADX（趋势强度）": (
            "ADX｜判断趋势强弱，配合 +DI / −DI 看方向",
            r"""
**它能做什么？** ADX 衡量趋势强度，本身不区分上涨或下跌；+DI 与 −DI 用来比较向上和向下的方向性移动。

**怎么看？**
- **ADX 上升：** 趋势强度可能正在增强，无论价格上涨还是下跌。
- **ADX 下降：** 趋势强度可能减弱，但不等于马上反转。
- **+DI 高于 −DI：** 方向比较偏向上行；反过来则偏向下行。
- **20 / 25 附近：** 常见的经验参考，不是适用于所有市场的固定界线。

""",
        ),
        "OBV（能量潮）": (
            "OBV｜观察累计成交量方向是否配合价格",
            r"""
**它能做什么？** OBV 根据收盘价相对前一日的变化，把当日成交量计入上涨、下跌或不变的累计序列，用来观察量价是否同步。它无法识别交易者身份，也不能证明资金真实流入或流出。

**怎么看？**
- 价格与 OBV 同步走高 / 走低，可作为量价配合的线索。
- 价格创新高而 OBV 没有同步创新高，值得进一步观察。
- 价格横盘而 OBV 有明显方向变化，可以列为后续检查对象，但无法单凭它预测突破方向。

""",
        ),
        "支撑位与阻力位": (
            "支撑与阻力｜寻找价格曾反复停顿的区域",
            r"""
**它是什么？** 支撑是过去较常出现止跌或反弹的价格区域；阻力是过去较常出现受阻或回落的区域。它们来自价格行为观察，不是不可突破的墙。

**怎么找？**
1. 找摆动高点和低点，观察价格从哪里转向。
2. 留意相近价位是否多次出现反应，而不是只看一次触碰。
3. 优先画成一个区域，不必假定市场会精确到某一分钱。
4. 接近区域时，观察 K 线实体、影线、收盘位置和成交量；突破后再看是否站稳或回踩。

**本图的参考线：** 自动显示的是所选区间最高价和最低价，不是自动识别出的多次反应区域。

""",
        ),
        "VWAP（概念学习）": (
            "VWAP｜成交量加权平均价：成交量越大，影响越大",
            r"""
**它是什么？** VWAP 是一段交易时段内的成交量加权平均价，常用于日内走势观察和交易执行评估。与 MA / EMA 不同，它会让成交量更大的价格对平均值产生更大影响，通常在每个交易日重新累计。

**怎么读？** 价格高于当日 VWAP，表示价格高于截至当前时点的成交量加权平均水平；低于则相反。价格反复穿越 VWAP 时，单凭上下方较难判断持续方向。

**使用时要注意：** VWAP 的起算时点很重要；不同交易日或不同锚点的数值不宜直接混比。价格在 VWAP 上方也不代表买方人数更多，更不保证之后上涨。

**本网站的限制：** 当前使用日线 OHLCV，没有每笔成交价格与成交量的时间分布，因此本课只介绍 VWAP 的用途和读法，不绘制冒充精确日内 VWAP 的曲线。

""",
        ),
        "一目均衡表（概念学习）": (
            "一目均衡表｜用转换线、基准线和云观察趋势背景",
            r"""
**它是什么？** 一目均衡表把趋势、价格位置和潜在支撑阻力放在同一套图表中。常见参数为 9、26、52，五个组成部分各有不同用途：

- **转换线：** 较短周期的价格平衡参考。
- **基准线：** 较长周期的价格平衡参考。
- **先行带 A / B：** 组成云层，显示未来图表位置上的参考区域。
- **迟行线：** 把当前收盘价向过去位移，用来比较当前价格与过去走势。

**怎么读云？** 价格在云上方通常代表偏强背景，在云下方通常代表偏弱背景，位于云内则可能较不明确。转换线与基准线交叉可以作为观察线索，但要结合价格相对云的位置及后续走势。

**重要区别：** 云向前绘制并不代表它知道未来价格；它只是把当前已计算的数值按规则向前显示。参数和绘图位移也可能因平台实现略有差异。

""",
        ),
    }

    if choice not in lessons:
        st.info("该指标的详细课程暂不可用。请先选择上方已有指标。")
        return

    title, lesson_markdown = lessons[choice]
    st.markdown(f"#### {title}")
    st.markdown(lesson_markdown)


def render_final_answer_review(number: int, question: str, options: list[str], selected: int,
                               correct: int, explanation: str, lesson: str) -> None:
    """Render review cards with green correct results and red incorrect results."""
    is_correct = selected == correct
    card_class = "quiz-correct" if is_correct else "quiz-incorrect"
    status = "✓ 回答正确" if is_correct else "✕ 回答错误 · 建议复习"
    rows = []
    alphabet = "ABCD"
    for idx, option in enumerate(options):
        option_class = "quiz-review-option"
        marker = alphabet[idx]
        suffix = ""
        if idx == correct:
            option_class += " answer-correct"
            suffix = "（正确答案）"
        if idx == selected and selected != correct:
            option_class += " answer-wrong"
            suffix = "（你的选择）"
        elif idx == selected and selected == correct:
            suffix = "（你的选择）"
        rows.append(
            f'<div class="{option_class}"><span class="option-marker">{marker}</span>'
            f'<span>{escape(str(option))}<b>{escape(suffix)}</b></span></div>'
        )
    st.markdown(
        f'<div class="quiz-review-card {card_class}">'
        f'<div class="quiz-review-head"><div class="quiz-review-title">第 {number:02d} 题｜{escape(question)}</div>'
        f'<span class="quiz-review-status">{status}</span></div>'
        f'{"".join(rows)}'
        f'<div class="quiz-review-explanation"><b>解析：</b>{escape(explanation)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"对应课程：{lesson}")










def style_fig(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5edf7", family="Microsoft YaHei, Noto Sans CJK SC, PingFang SC, Arial, sans-serif", size=13),
        height=height,
        margin=dict(l=8, r=8, t=56, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#17263b", font_color="#eef5fc", font_size=13, font_family="Microsoft YaHei, Noto Sans CJK SC, PingFang SC, Arial, sans-serif"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(180,204,232,.16)")
    fig.update_yaxes(gridcolor="rgba(180,204,232,.09)", zeroline=False, linecolor="rgba(180,204,232,.16)")
    return fig


def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate a consistent, educational set of daily technical indicators."""
    frame = data.copy().sort_values("date").reset_index(drop=True)
    for field in ("open", "high", "low", "close", "volume"):
        frame[field] = pd.to_numeric(frame[field], errors="coerce")
    close = frame["close"]
    high = frame["high"]
    low = frame["low"]
    volume = frame["volume"].fillna(0.0)

    # Trend overlays: simple and exponential moving averages.
    frame["ma5"] = close.rolling(5, min_periods=5).mean()
    frame["ma20"] = close.rolling(20, min_periods=20).mean()
    frame["ma50"] = close.rolling(50, min_periods=50).mean()
    frame["ema12"] = close.ewm(span=12, adjust=False, min_periods=12).mean()
    frame["ema26"] = close.ewm(span=26, adjust=False, min_periods=26).mean()

    # RSI (14): Wilder-style exponential smoothing; platform seeds may differ slightly.
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    frame["rsi14"] = 100 - (100 / (1 + rs))
    frame.loc[(avg_loss == 0) & (avg_gain > 0), "rsi14"] = 100.0
    frame.loc[(avg_gain == 0) & (avg_loss > 0), "rsi14"] = 0.0
    frame.loc[(avg_gain == 0) & (avg_loss == 0), "rsi14"] = 50.0

    # MACD: DIF = EMA12 - EMA26; DEA = 9-period EMA of DIF; histogram = DIF - DEA.
    frame["dif"] = frame["ema12"] - frame["ema26"]
    frame["dea"] = frame["dif"].ewm(span=9, adjust=False, min_periods=9).mean()
    frame["macd_hist"] = frame["dif"] - frame["dea"]

    # Bollinger Bands (20, 2): a 20-session SMA and two standard deviations.
    frame["bb_mid"] = close.rolling(20, min_periods=20).mean()
    rolling_std = close.rolling(20, min_periods=20).std(ddof=0)
    frame["bb_upper"] = frame["bb_mid"] + 2.0 * rolling_std
    frame["bb_lower"] = frame["bb_mid"] - 2.0 * rolling_std

    # Stochastic (14, 3): closing price within the recent 14-session high-low range.
    rolling_low = low.rolling(14, min_periods=14).min()
    rolling_high = high.rolling(14, min_periods=14).max()
    denominator = (rolling_high - rolling_low).replace(0, np.nan)
    frame["stoch_k"] = 100 * (close - rolling_low) / denominator
    frame["stoch_d"] = frame["stoch_k"].rolling(3, min_periods=3).mean()

    # ADX / directional indicators. ATR is used internally in the calculation, but is not taught
    # or displayed as a separate indicator in this course.
    prev_close = close.shift(1)
    true_range = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=frame.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=frame.index)
    smoothed_tr_raw = true_range.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    zero_range = smoothed_tr_raw.eq(0) & smoothed_tr_raw.notna()
    smoothed_tr = smoothed_tr_raw.replace(0, np.nan)
    smoothed_plus = plus_dm.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    smoothed_minus = minus_dm.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    frame["plus_di"] = 100 * smoothed_plus / smoothed_tr
    frame["minus_di"] = 100 * smoothed_minus / smoothed_tr
    # A completely flat window has no directional movement. Define both DI and DX as zero
    # after their normal warm-up rather than letting the entire ADX line disappear as NaN.
    frame.loc[zero_range, ["plus_di", "minus_di"]] = 0.0
    dx_sum = frame["plus_di"] + frame["minus_di"]
    dx = 100 * (frame["plus_di"] - frame["minus_di"]).abs() / dx_sum.replace(0, np.nan)
    dx.loc[dx_sum.eq(0) & dx_sum.notna()] = 0.0
    frame["adx14"] = dx.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()

    # OBV: cumulative volume signed by whether the close rose or fell versus the prior close.
    signed_volume = np.sign(delta.fillna(0.0)) * volume
    frame["obv"] = signed_volume.cumsum()
    return frame


def technical_range_extrema(data: pd.DataFrame) -> dict[str, object] | None:
    """Return high/low and their dates for the entire currently selected chart range."""
    if data is None or data.empty or not {"date", "high", "low"}.issubset(data.columns):
        return None
    window = data.dropna(subset=["date", "high", "low"]).sort_values("date").reset_index(drop=True).copy()
    if window.empty:
        return None
    low_pos = int(np.argmin(window["low"].to_numpy(dtype=float)))
    high_pos = int(np.argmax(window["high"].to_numpy(dtype=float)))
    return {
        "data": window,
        "low_pos": low_pos,
        "high_pos": high_pos,
        "low_row": window.iloc[low_pos],
        "high_row": window.iloc[high_pos],
    }


def technical_indicator_figure(
    data: pd.DataFrame,
    overlays: list[str],
    lower_indicator: str,
    show_levels: bool = False,
    show_fibonacci: bool = False,
    height: int = 610,
) -> go.Figure:
    """Plot indicators and price levels against the full selected historical window."""
    frame = data.copy().sort_values("date").reset_index(drop=True)
    valid_lower_indicators = {"RSI", "MACD", "随机指标（Stochastic）", "ADX（趋势强度）", "OBV（能量潮）", "不显示副图"}
    if lower_indicator not in valid_lower_indicators:
        lower_indicator = "不显示副图"
    overlays = overlays or []
    has_lower = lower_indicator != "不显示副图"
    rows = 2 if has_lower else 1
    fig = make_subplots(
        rows=rows, cols=1, shared_xaxes=True,
        vertical_spacing=0.035 if has_lower else 0,
        row_heights=[0.73, 0.27] if has_lower else [1.0],
    )
    fig.add_trace(go.Candlestick(
        x=frame["date"], open=frame["open"], high=frame["high"],
        low=frame["low"], close=frame["close"], name="K线（绿涨红跌）",
        increasing_line_color="#60e2bd", decreasing_line_color="#ff8f9b",
        increasing_fillcolor="#60e2bd", decreasing_fillcolor="#ff8f9b",
        whiskerwidth=0.55,
    ), row=1, col=1)

    if "MA5 / MA20" in overlays:
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["ma5"], mode="lines", name="MA5（5日移动均线）",
            line=dict(color="#ffc777", width=2.0), connectgaps=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["ma20"], mode="lines", name="MA20（20日移动均线）",
            line=dict(color="#75b7ff", width=2.0), connectgaps=False,
        ), row=1, col=1)
    if "EMA12 / EMA26" in overlays:
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["ema12"], mode="lines", name="EMA12（12日指数移动均线）",
            line=dict(color="#d4c1ff", width=1.9), connectgaps=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["ema26"], mode="lines", name="EMA26（26日指数移动均线）",
            line=dict(color="#ff9f70", width=1.9), connectgaps=False,
        ), row=1, col=1)
    if "布林带（20, 2）" in overlays:
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["bb_upper"], mode="lines", name="布林带上轨",
            line=dict(color="rgba(117,183,255,.78)", width=1.3, dash="dot"), connectgaps=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["bb_lower"], mode="lines", name="布林带区间",
            line=dict(color="rgba(117,183,255,.78)", width=1.3, dash="dot"),
            fill="tonexty", fillcolor="rgba(117,183,255,.08)", connectgaps=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["bb_mid"], mode="lines", name="布林带中轨（20日均线）",
            line=dict(color="#9ecbff", width=1.4), connectgaps=False,
        ), row=1, col=1)

    extrema = technical_range_extrema(frame)
    range_frame = extrema["data"] if extrema else frame.iloc[0:0]
    if extrema and len(range_frame) >= 5:
        low_row = extrema["low_row"]
        high_row = extrema["high_row"]
        support_level = float(low_row["low"])
        resistance_level = float(high_row["high"])
        start_date = pd.Timestamp(range_frame["date"].iloc[0])
        end_date = pd.Timestamp(range_frame["date"].iloc[-1])
        if show_levels:
            fig.add_trace(go.Scatter(
                x=range_frame["date"].tolist(), y=[support_level] * len(range_frame), mode="lines",
                name="区间低位参考（教学支撑）", showlegend=False,
                line=dict(color="#60e2bd", width=1.5, dash="dash"),
                hovertemplate="区间低位参考（教学支撑）<br>%{y:.2f}<extra></extra>",
            ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=range_frame["date"].tolist(), y=[resistance_level] * len(range_frame), mode="lines",
                name="区间高位参考（教学阻力）", showlegend=False,
                line=dict(color="#ff8f9b", width=1.5, dash="dash"),
                hovertemplate="区间高位参考（教学阻力）<br>%{y:.2f}<extra></extra>",
            ), row=1, col=1)
            fig.add_annotation(
                x=end_date, y=support_level, text="区间低位参考", showarrow=False,
                xanchor="right", yshift=9, bgcolor="rgba(7,17,31,.88)",
                font=dict(size=10, color="#60e2bd"), row=1, col=1,
            )
            fig.add_annotation(
                x=end_date, y=resistance_level, text="区间高位参考", showarrow=False,
                xanchor="right", yshift=9, bgcolor="rgba(7,17,31,.88)",
                font=dict(size=10, color="#ff8f9b"), row=1, col=1,
            )
        if show_fibonacci:
            low_pos = int(extrema["low_pos"])
            high_pos = int(extrema["high_pos"])
            swing_low = float(low_row["low"])
            swing_high = float(high_row["high"])
            span = swing_high - swing_low
            # The extrema across the selected period are only a transparent teaching heuristic.
            # If both extrema occur on the same candle, direction cannot be inferred reliably.
            if span > 0 and low_pos != high_pos:
                if low_pos < high_pos:
                    levels = [(ratio, swing_high - span * ratio) for ratio in (0.236, 0.382, 0.500, 0.618, 0.786)]
                else:
                    levels = [(ratio, swing_low + span * ratio) for ratio in (0.236, 0.382, 0.500, 0.618, 0.786)]
                fib_colors = ["#ffc777", "#75b7ff", "#d4c1ff", "#60e2bd", "#ff9f70"]
                for (ratio, level), color in zip(levels, fib_colors):
                    fig.add_trace(go.Scatter(
                        x=range_frame["date"].tolist(), y=[level] * len(range_frame), mode="lines",
                        name=f"斐波那契 {ratio * 100:.1f}%", showlegend=False,
                        line=dict(color=color, width=1, dash="dot"),
                        hovertemplate=f"斐波那契 {ratio * 100:.1f}%<br>%{{y:.2f}}<extra></extra>",
                    ), row=1, col=1)
                    fig.add_annotation(
                        x=end_date, y=level, text=f"斐波那契 {ratio * 100:.1f}%",
                        showarrow=False, xanchor="right", yshift=1,
                        bgcolor="rgba(7,17,31,.78)", font=dict(size=9, color=color), row=1, col=1,
                    )

    if lower_indicator == "RSI":
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["rsi14"], mode="lines", name="RSI（14）",
            line=dict(color="#d4c1ff", width=2.2), connectgaps=False,
        ), row=2, col=1)
        rsi_x = frame["date"].tolist()
        for y_value, color, label in [(70, "#ff8f9b", "70参考线"), (50, "rgba(180,204,232,.55)", "50中线"), (30, "#60e2bd", "30参考线")]:
            if rsi_x:
                fig.add_trace(go.Scatter(x=rsi_x, y=[y_value] * len(rsi_x), mode="lines", name=label, showlegend=False,
                    line=dict(color=color, dash="dot", width=1), hovertemplate=f"RSI {label}<extra></extra>"), row=2, col=1)
        fig.update_yaxes(title_text="RSI（0–100）", range=[0, 100], row=2, col=1)
    elif lower_indicator == "MACD":
        histogram_colors = ["#60e2bd" if pd.notna(v) and v >= 0 else "#ff8f9b" for v in frame["macd_hist"]]
        fig.add_trace(go.Bar(
            x=frame["date"], y=frame["macd_hist"], name="柱体（DIF−DEA）",
            marker_color=histogram_colors, opacity=0.65,
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["dif"], mode="lines", name="DIF（快线）",
            line=dict(color="#d4c1ff", width=2), connectgaps=False,
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["dea"], mode="lines", name="DEA（信号线）",
            line=dict(color="#ffc777", width=2), connectgaps=False,
        ), row=2, col=1)
        macd_x = frame["date"].tolist()
        if macd_x:
            fig.add_trace(go.Scatter(
                x=macd_x, y=[0.0] * len(macd_x), mode="lines", name="MACD零轴参考线",
                showlegend=False, line=dict(color="rgba(180,204,232,.55)", dash="dot", width=1),
                hovertemplate="MACD 零轴参考线：0<extra></extra>",
            ), row=2, col=1)
        fig.update_yaxes(title_text="MACD 数值", row=2, col=1)
    elif lower_indicator == "随机指标（Stochastic）":
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["stoch_k"], mode="lines", name="%K（快线）",
            line=dict(color="#75b7ff", width=2), connectgaps=False,
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["stoch_d"], mode="lines", name="%D（平滑线）",
            line=dict(color="#ffc777", width=2), connectgaps=False,
        ), row=2, col=1)
        stoch_x = frame["date"].tolist()
        if stoch_x:
            fig.add_trace(go.Scatter(x=stoch_x, y=[80] * len(stoch_x), mode="lines", name="80参考线", showlegend=False,
                line=dict(color="#ff8f9b", dash="dot", width=1), hovertemplate="随机指标 80 参考线<extra></extra>"), row=2, col=1)
            fig.add_trace(go.Scatter(x=stoch_x, y=[20] * len(stoch_x), mode="lines", name="20参考线", showlegend=False,
                line=dict(color="#60e2bd", dash="dot", width=1), hovertemplate="随机指标 20 参考线<extra></extra>"), row=2, col=1)
        fig.update_yaxes(title_text="随机指标（0–100）", range=[0, 100], row=2, col=1)
    elif lower_indicator == "ADX（趋势强度）":
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["adx14"], mode="lines", name="ADX（趋势强度）",
            line=dict(color="#d4c1ff", width=2.2), connectgaps=False,
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["plus_di"], mode="lines", name="+DI（正向指标）",
            line=dict(color="#60e2bd", width=1.7), connectgaps=False,
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["minus_di"], mode="lines", name="−DI（负向指标）",
            line=dict(color="#ff8f9b", width=1.7), connectgaps=False,
        ), row=2, col=1)
        adx_x = frame["date"].tolist()
        if adx_x:
            fig.add_trace(go.Scatter(x=adx_x, y=[20] * len(adx_x), mode="lines", name="ADX 20参考线", showlegend=False,
                line=dict(color="rgba(180,204,232,.45)", dash="dot", width=1), hovertemplate="ADX 20 参考线<extra></extra>"), row=2, col=1)
            fig.add_trace(go.Scatter(x=adx_x, y=[25] * len(adx_x), mode="lines", name="ADX 25参考线", showlegend=False,
                line=dict(color="rgba(180,204,232,.45)", dash="dash", width=1), hovertemplate="ADX 25 参考线<extra></extra>"), row=2, col=1)
        fig.update_yaxes(title_text="ADX / DI（0–100）", range=[0, 100], row=2, col=1)
    elif lower_indicator == "OBV（能量潮）":
        fig.add_trace(go.Scatter(
            x=frame["date"], y=frame["obv"], mode="lines", name="OBV（能量潮）",
            line=dict(color="#60e2bd", width=2.1), connectgaps=False,
        ), row=2, col=1)
        fig.update_yaxes(title_text="累计成交量（相对值）", tickformat="~s", row=2, col=1)

    style_fig(fig, height)
    fig.update_layout(
        height=height, hovermode="x unified", xaxis_rangeslider_visible=False,
        # Reserve a generous top band for a multi-row legend on narrow screens.
        # Keeping the legend above the plot prevents it from covering candles or indicator lines.
        margin=dict(l=38, r=16, t=132, b=30),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            bgcolor="rgba(5,12,24,.78)", bordercolor="rgba(139,162,189,.35)", borderwidth=1,
            font=dict(size=11, color="#e9f0fb"),
        ),
    )
    fig.update_xaxes(
        rangeslider_visible=False, showgrid=True, gridcolor="rgba(180,204,232,.10)",
        tickfont=dict(color="#dce7f5", size=10),
        rangebreaks=[dict(bounds=["sat", "mon"])],
    )
    fig.update_yaxes(title_text="价格（美元）", row=1, col=1, gridcolor="rgba(180,204,232,.12)", tickfont=dict(color="#dce7f5", size=10))
    if has_lower:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(180,204,232,.10)", row=2, col=1)
        fig.update_yaxes(gridcolor="rgba(180,204,232,.10)", tickfont=dict(color="#dce7f5", size=10), row=2, col=1)
    return fig



def hero(title: str, subtitle: str, eyebrow: str = "STOCKSCOPE LEARN · BEGINNER STOCK ACADEMY") -> None:
    # Keep intentional title line breaks rather than letting HTML collapse them into spaces.
    title_html = title.replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">{eyebrow}</div>
          <h1>{title_html}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(kicker: str, title: str, desc: str | None = None) -> None:
    st.markdown(f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div>', unsafe_allow_html=True)
    if desc:
        st.markdown(f'<div class="section-desc">{desc}</div>', unsafe_allow_html=True)


def escape_markdown_dollars(content: str) -> str:
    """Keep dollar-denominated values literal instead of treating $ as LaTeX delimiters."""
    return str(content).replace("$", "&#36;")


def info_card(icon: str, title: str, body: str, tag: str | None = None) -> None:
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    st.markdown(
        f'''<div class="info-card"><div style="font-size:1.35rem">{icon}</div><h4>{title}</h4><p>{body}</p><div style="margin-top:.8rem">{tag_html}</div></div>''',
        unsafe_allow_html=True,
    )


def mark_complete(lesson: str) -> None:
    current = set(st.session_state.get("completed_lessons", []))
    current.add(lesson)
    st.session_state["completed_lessons"] = sorted(current)


def record_quiz_attempt(lesson: str, passed: bool) -> None:
    """Record quiz attempts while allowing learners to retake checks."""
    stats = st.session_state.setdefault("quiz_attempts", {})
    prior = stats.get(lesson, {"attempts": 0, "passed": False, "last_passed": False})
    stats[lesson] = {
        "attempts": int(prior.get("attempts", 0)) + 1,
        "passed": bool(prior.get("passed", False) or passed),
        "last_passed": bool(passed),
    }


def nav_to(page: str) -> None:
    st.session_state["main_nav"] = page


def reset_comprehensive_quiz() -> None:
    st.session_state.pop("comprehensive_quiz_result", None)
    for idx in range(24):
        st.session_state.pop(f"comprehensive_answer_{idx}", None)


def choose_company_statement(value: str) -> None:
    """Remember the selected financial statement before Streamlit reruns."""
    st.session_state["company_statement_choice"] = value


def scroll_main_to_top(trigger: str) -> None:
    """Scroll to the top once after a main-navigation page change only.

    Candle-pattern selection deliberately does not call this helper. Avoid retry
    loops because repeated calls can pull users back to the top during reading.
    """
    trigger_json = json.dumps(str(trigger), ensure_ascii=False)
    html = f"""
    <div style="font:1px sans-serif;color:transparent;height:1px;overflow:hidden">{escape(str(trigger))}</div>
    <script>
    (() => {{
      const trigger = {trigger_json};
      // One delayed action only. No polling/repeating timers.
      const jumpToTop = () => {{
        try {{
          const host = window.parent;
          const doc = host.document;
          const main = doc.querySelector('[data-testid="stMain"]')
            || doc.querySelector('section[data-testid="stMain"]')
            || doc.querySelector('section.main')
            || doc.querySelector('main');
          const target = doc.getElementById('stockscope-main-top');

          // Prefer scrolling the main Streamlit content container. Avoid resetting
          // every ancestor/document at once, which can create visible jumpiness.
          if (main && typeof main.scrollTo === 'function') {{
            main.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
          }} else if (target && typeof target.scrollIntoView === 'function') {{
            target.scrollIntoView({{ block: 'start', inline: 'nearest', behavior: 'instant' }});
          }} else if (typeof host.scrollTo === 'function') {{
            host.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
          }}
        }} catch (_) {{ /* Browser security restrictions should not break the app. */ }}
      }};
      // Trigger is referenced deliberately so each navigation event has distinct HTML.
      void trigger;
      window.requestAnimationFrame(() => window.setTimeout(jumpToTop, 120));
    }})();
    </script>
    """
    components.html(html, height=1, width=1, scrolling=False)


def show_data_warning(error: str | None) -> None:
    if error:
        st.warning("暂时无法加载股票数据。教学文字仍可阅读；需要使用行情图表时，请检查网络或稍后重试。")
        # Keep raw technical exceptions out of the visible UI to avoid a stray code-style panel.


def format_money(value: float) -> str:
    return "—" if pd.isna(value) else f"${value:,.2f}"


def format_pct(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:+.2f}%"


def lesson_completion_button(lesson: str, key: str) -> None:
    """Let learners mark a lesson complete without a separate reflection form."""
    completed = set(st.session_state.get("completed_lessons", []))
    already_done = lesson in completed
    label = "✓ 本课已完成" if already_done else "标记本课完成"
    if st.button(label, key=key, width="stretch", disabled=already_done):
        mark_complete(lesson)
        st.success("已将本课标记为完成。")


# ============================================================
# Candlestick pattern library and illustrative OHLC helper
# ============================================================
# These are common textbook-style descriptions. Exact pattern rules vary by source;
# none of these shapes is a standalone prediction or trading instruction.
CANDLE_PATTERNS = [
    {
        "group": "单根 K 线", "name": "大阳线（Long bullish candle）", "bias": "偏多的价格行为", "trend": "sideways",
        "bars": [(100, 112, 99, 111)], "structure": "实体明显较长，收盘显著高于开盘；上下影线相对实体较短。",
        "recognize": "- 收盘价明显高于开盘价。\n- 实体占整个高低区间较大部分。\n- “长”应与该证券近期 K 线的实体比较，而不是用固定美元值判断。",
        "meaning": "说明该周期价格从开盘到收盘出现较大上涨，常被解读为买方在该周期占优。它不是未来继续上涨的保证。",
        "context": "出现在下跌后可能提示卖压减弱；出现在大幅上涨末段也可能体现情绪过热或短期扩张。",
        "confirmation": "观察后续收盘价、关键价位、成交量及大盘环境；必要时与公司新闻或财报对照。",
        "pitfall": "把单根大阳线直接当成买入信号，或忽略价格已经短期大幅上涨。",
    },
    {
        "group": "单根 K 线", "name": "大阴线（Long bearish candle）", "bias": "偏空的价格行为", "trend": "sideways",
        "bars": [(112, 113, 99, 100)], "structure": "实体明显较长，收盘显著低于开盘；上下影线相对较短。",
        "recognize": "- 收盘价明显低于开盘价。\n- 实体相对近期 K 线较长。\n- 大阴线描述已经发生的下跌，不等于能确定下一根 K 线方向。",
        "meaning": "表示该周期从开盘到收盘出现较大下跌，常被解读为卖方占优。",
        "context": "在上涨后可能提示趋势转弱；在长期下跌末端，也可能伴随恐慌性抛售，不能机械追空。",
        "confirmation": "检查是否跌破重要价位、成交量是否异常、是否有财报或宏观事件，以及后续价格是否延续。",
        "pitfall": "看到大阴线就恐慌卖出，忽略投资期限、基本面和已制定的风险计划。",
    },
    {
        "group": "单根 K 线", "name": "光头光脚阳线（Bullish Marubozu）", "bias": "明显偏多的当期动能", "trend": "sideways",
        "bars": [(100, 112, 100, 112)], "structure": "开盘几乎等于最低价，收盘几乎等于最高价；实体长，影线极短或没有。",
        "recognize": "- 开盘附近是本周期低位。\n- 收盘附近是本周期高位。\n- 不同数据源可能存在小幅价格差，因此课堂识别不要求完全相等。",
        "meaning": "买方在该周期内较持续地占优势。",
        "context": "需要判断它是突破开始、趋势中段，还是一段快速上涨后的过度延伸。",
        "confirmation": "观察突破位置是否有效、后续是否守住该区间，并核实成交量和市场背景。",
        "pitfall": "把当期动能误认为长期趋势，忽略高位追涨的回撤风险。",
    },
    {
        "group": "单根 K 线", "name": "光头光脚阴线（Bearish Marubozu）", "bias": "明显偏空的当期动能", "trend": "sideways",
        "bars": [(112, 112, 100, 100)], "structure": "开盘几乎等于最高价，收盘几乎等于最低价；实体长，影线极短或没有。",
        "recognize": "- 开盘附近是本周期高位。\n- 收盘附近是本周期低位。\n- 表示价格整个周期大致向下推进。",
        "meaning": "卖方在该周期内较持续地占优势。",
        "context": "在支撑位附近需要观察是否继续破位；在大幅下跌后则应小心追跌和短期反弹风险。",
        "confirmation": "结合趋势、重要价位、成交量和之后的收盘表现，而不是只看单根实体。",
        "pitfall": "认为长阴线之后一定还有长阴线。",
    },
    {
        "group": "单根 K 线", "name": "十字星（Doji）", "bias": "中性／犹豫", "trend": "sideways",
        "bars": [(100, 106, 95, 100.1)], "structure": "开盘价与收盘价非常接近，实体极小；影线可以长也可以短。",
        "recognize": "- 核心是开盘和收盘接近，不是必须绝对相等。\n- 与该证券近期实体比较才有意义。\n- 上下影线长度决定它更接近哪一种十字星变体。",
        "meaning": "表示该周期内价格曾波动，但最终开收盘接近；常被解读为犹豫或暂时平衡。",
        "context": "在强趋势后可能提醒观察动能是否变化；在窄幅盘整中则可能只是普通噪声。",
        "confirmation": "观察随后一根或几根 K 线的方向、成交量和关键价位。",
        "pitfall": "认为每一个十字星都意味着反转。",
    },
    {
        "group": "单根 K 线", "name": "长腿十字星（Long-legged Doji）", "bias": "强烈犹豫／双向波动", "trend": "sideways",
        "bars": [(100, 110, 90, 100.1)], "structure": "开收盘接近，但上下影线都很长。",
        "recognize": "- 实体很小。\n- 最高价与最低价距实体较远。\n- 显示本周期上下波动都很明显，最终却没有远离开盘价。",
        "meaning": "反映价格曾大幅双向波动，买卖双方都曾推动价格，但收盘接近开盘。",
        "context": "若出现在重大消息或剧烈行情附近，要结合事件时间、成交量和之后的价格行为观察。",
        "confirmation": "等待后续方向和关键区间突破，不宜仅凭影线方向预测。",
        "pitfall": "把大幅波动误解为明确的多头或空头胜利。",
    },
    {
        "group": "单根 K 线", "name": "蜻蜓十字星（Dragonfly Doji）", "bias": "位置合适时可能偏多", "trend": "down",
        "bars": [(100, 101, 90, 100.1)], "structure": "开收盘接近且靠近最高价，下影线很长，上影线很短或几乎没有。",
        "recognize": "- 价格一度明显下探。\n- 收盘回到接近开盘的高位。\n- 形状像倒置的字母 T，但命名和比例可能因资料而异。",
        "meaning": "常被理解为低位卖压曾推动价格下行，但买盘把价格推回接近开盘处。",
        "context": "在下跌后或支撑区域更值得观察；出现在其他位置时未必有方向含义。",
        "confirmation": "看后续收盘是否走强、是否守住低点，并结合交易量及市场背景。",
        "pitfall": "把长下影线当成买家已经完全控制市场的证明。",
    },
    {
        "group": "单根 K 线", "name": "墓碑十字星（Gravestone Doji）", "bias": "位置合适时可能偏空", "trend": "up",
        "bars": [(100, 110, 99, 100.05)], "structure": "开收盘接近且靠近最低价，上影线很长，下影线很短或几乎没有。",
        "recognize": "- 价格曾显著上探。\n- 收盘回落到接近开盘／最低价的位置。\n- 与蜻蜓十字星的主要区别在长影线方向。",
        "meaning": "常被理解为高位买盘未能维持价格，卖方在收盘前将其压回。",
        "context": "在上涨后或阻力区域更值得观察；单独出现不意味着趋势必然反转。",
        "confirmation": "观察后续是否跌破形态低位、收盘走弱，并参考成交量与市场环境。",
        "pitfall": "忽略它可能在横盘或低流动性时段形成，缺乏趋势背景。",
    },
    {
        "group": "单根 K 线", "name": "纺锤线（Spinning Top）", "bias": "中性／犹豫", "trend": "sideways",
        "bars": [(100, 106, 94, 101.5)], "structure": "实体较小，上下影线均较明显；开收盘之间的变化较小。",
        "recognize": "- 实体较小。\n- 上下影线都存在，说明价格曾向两个方向波动。\n- 与十字星区别在于纺锤线通常有较清楚的小实体。",
        "meaning": "显示本周期内多空都曾推动价格，但收盘与开盘差距有限。",
        "context": "趋势后的纺锤线可以提醒观察动能变化，盘整区间内则可能不特别重要。",
        "confirmation": "看后续走势是否给出方向，并考虑波动环境和重要价位。",
        "pitfall": "把犹豫形态误称为反转形态；它也可能只是暂停。",
    },
    {
        "group": "单根 K 线", "name": "锤头线（Hammer）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(100, 101.5, 91, 101)], "structure": "小实体位于区间上部，下影线通常明显长于实体，上影线较短。",
        "recognize": "- 常见教学规则是下影线至少约为实体的两倍，但比例并非全球统一标准。\n- 实体可以是阳线或阴线。\n- 必须先看此前是否有下跌趋势。",
        "meaning": "下探后价格回升，提示低位出现承接；传统上被视为下跌后潜在转强的观察线索。",
        "context": "通常要求此前有一段下跌，并更关注它是否靠近支撑区域。",
        "confirmation": "后续价格走强、收盘越过锤头高位或其他明确的强势表现，可能提供额外证据；确认方式不是统一规则。",
        "pitfall": "同样的形状若出现在上涨后，通常不叫锤头线而更接近上吊线。",
    },
    {
        "group": "单根 K 线", "name": "上吊线（Hanging Man）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(100, 101.5, 91, 101)], "structure": "与锤头线形状相近：小实体在上部、长下影线、短上影线。",
        "recognize": "- 形状本身和锤头线近似。\n- 主要依靠出现前的上涨趋势区分。\n- 实体颜色不是唯一判断标准。",
        "meaning": "上涨过程中价格曾明显下探，虽然后来回升，但可能提示卖方开始活跃。",
        "context": "应位于已有上涨之后；如果没有此前上涨背景，不宜仅凭形状命名。",
        "confirmation": "观察下一根或后续价格是否转弱，例如收盘跌破其实体或低点；不同交易者规则会不同。",
        "pitfall": "看到长下影线就判断看涨；同一形状在上涨后有不同的传统解释。",
    },
    {
        "group": "单根 K 线", "name": "倒锤头（Inverted Hammer）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(100, 110, 99.8, 100.6)], "structure": "小实体靠近区间下部；上影线明显较长，下影线较短。具体比例只是一种常见的形态描述，不是普遍硬性阈值。",
        "recognize": "- 实体较小，且靠近本周期价格区间的下部。\n- 上影线明显长于实体，表示价格曾向上探出，但收盘没有维持在高位。\n- 下影线较短；与流星线的形状相近，需结合出现前的趋势背景区分。",
        "meaning": "可能提示买方开始尝试推高价格，但当期仍未能收在高位，因此通常需要后续确认。",
        "context": "传统解释更关注下跌后出现的倒锤头。",
        "confirmation": "观察后续是否出现较强阳线或突破形态高位；否则它可能只是短暂反弹。",
        "pitfall": "与流星线形状接近；二者主要靠此前趋势来区分。",
    },
    {
        "group": "单根 K 线", "name": "流星线（Shooting Star）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(100, 110, 99.8, 100.5)], "structure": "小实体靠近区间下部；上影线明显较长，下影线较短。具体比例会随市场波动和采用的定义而变化。",
        "recognize": "- 价格曾上探明显高位，但收盘退回。\n- 通常要求此前有上涨趋势。\n- 与倒锤头的主要区别是形态出现前的趋势。",
        "meaning": "高位未能维持，可能提示买盘动能减弱或上方存在抛压。",
        "context": "在一段上涨后或潜在阻力附近，比在无趋势区间更有讨论价值。",
        "confirmation": "留意后续走弱、关键支撑失守及成交量变化；没有确认时只能视为观察线索。",
        "pitfall": "把长上影线视为一定下跌，或忽略趋势仍可能延续。",
    },
    {
        "group": "双根组合", "name": "看涨吞没（Bullish Engulfing）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(103, 104, 97, 98), (97, 106, 96, 105)], "structure": "先出现偏空实体，随后出现更大的偏多实体，第二根实体覆盖第一根实体。",
        "recognize": "- 第一根通常为阴线实体，第二根为阳线实体。\n- 重点比较实体，不一定要求第二根覆盖第一根的全部影线。\n- 经典形态在有跳空的市场定义可能更严格。",
        "meaning": "传统解读认为第二周期收盘明显回到第一根实体上方，反映价格压力出现变化。",
        "context": "通常在下跌或回调后讨论；横盘区间中可能不如名字听起来有意义。",
        "confirmation": "检查后续是否继续走强、形态是否处于支撑附近，以及成交量是否有变化。",
        "pitfall": "只看实体覆盖，不看此前趋势和形态的实际位置。",
    },
    {
        "group": "双根组合", "name": "看跌吞没（Bearish Engulfing）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(97, 104, 96, 103), (105, 106, 94, 95)], "structure": "先出现偏多实体，随后较大的偏空实体覆盖第一根实体。",
        "recognize": "- 第一根通常为阳线实体，第二根为更大的阴线实体。\n- 重点是实体关系，形态定义的具体边界会因教材不同而变化。",
        "meaning": "传统解读认为第二周期从开盘到收盘的卖压覆盖了前一周期实体，提示可能转弱。",
        "context": "通常在一段上涨之后分析；如果此前已经大幅下跌，信号含义不同。",
        "confirmation": "观察后续价格是否跌破形态低点或关键支撑，并核查是否有新信息。",
        "pitfall": "不结合背景，把任何两根相反颜色的 K 线都叫吞没。",
    },
    {
        "group": "双根组合", "name": "刺透线（Piercing Line）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(105, 106, 94, 95), (92, 102, 91, 101)], "structure": "第一根是较长阴线，第二根向下开盘后回升，收盘进入第一根实体中点以上。",
        "recognize": "- 第二根应有明显回升。\n- 传统定义通常涉及低开或向下跳空；不同市场的数据结构会影响这种条件。\n- 第二根收盘超过前一根实体中点，但一般未超过前一根开盘价。",
        "meaning": "下跌后，后一周期显著收复前一阴线实体的一部分，可能提示卖压缓和。",
        "context": "常在下跌后讨论；若缺少经典跳空条件，可能只满足宽松版本定义。",
        "confirmation": "观察后续是否继续收复失地，同时检查成交量和支撑区域。",
        "pitfall": "把任何反弹阳线都认定为刺透线，忽略前一根实体中点标准。",
    },
    {
        "group": "双根组合", "name": "乌云盖顶（Dark Cloud Cover）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(95, 106, 94, 105), (108, 109, 97, 99)], "structure": "第一根是较长阳线，第二根高开后回落，收盘跌入第一根实体中点以下。",
        "recognize": "- 第二根通常为阴线。\n- 传统定义一般要求高开，且收盘进入前一阳线实体中点以下。\n- 不是仅凭出现阴线就成立。",
        "meaning": "后一周期未能维持高开优势，反而把价格压回先前阳线实体中段以下，可能提示转弱。",
        "context": "一般在上涨或潜在阻力附近更有讨论价值。",
        "confirmation": "看后续能否跌破形态低位或出现持续走弱，并核查是否发生新的信息变化。",
        "pitfall": "在没有明显此前上涨的情况下，也机械地赋予看跌含义。",
    },
    {
        "group": "双根组合", "name": "看涨孕线（Bullish Harami）", "bias": "下跌后可能转稳", "trend": "down",
        "bars": [(108, 109, 94, 96), (98, 101, 97, 100)], "structure": "第一根实体较大，第二根较小实体完全位于第一根实体内部。",
        "recognize": "- 第二根实体应明显较小。\n- 典型看涨孕线出现在下跌后，第二根可以是阳线或很小实体；命名细节因定义不同而异。",
        "meaning": "前一周期的强烈卖压之后，下一周期价格波动收窄，可能表示卖压暂时减弱，但方向仍需要确认。",
        "context": "关注此前是否下跌，以及第二根是否位于第一根实体内部。",
        "confirmation": "后续若向上突破孕线高位，可能增加转强证据；否则也可能只是短暂停顿。",
        "pitfall": "把孕线当成已完成的反转，而不是潜在停顿。",
    },
    {
        "group": "双根组合", "name": "看跌孕线（Bearish Harami）", "bias": "上涨后可能转弱", "trend": "up",
        "bars": [(94, 109, 93, 107), (105, 106, 102, 103)], "structure": "第一根实体较大，第二根较小实体位于第一根实体内部。",
        "recognize": "- 第二根实体较小且位于第一根实体范围内。\n- 传统解读通常要求此前有上涨趋势。",
        "meaning": "原先的上涨实体之后，价格区间与开收盘变化缩小，可能提示上行动能暂时减弱。",
        "context": "需结合此前上涨和阻力位置判断；横盘中可能只是普通的小实体。",
        "confirmation": "观察后续是否走弱、跌破第二根低点或重要支撑。",
        "pitfall": "忽略形态需要背景，单独将小实体解释为看跌。",
    },
    {
        "group": "双根组合", "name": "镊子底（Tweezer Bottom）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(103, 105, 95, 97), (97, 102, 95, 101)], "structure": "两根相邻 K 线的最低价大致相同，第二根出现回升。",
        "recognize": "- 两次低点接近，显示同一价位附近出现反应。\n- 相同低点的容许误差没有统一标准。",
        "meaning": "传统解读为同一低位被两次测试但未能明显跌破，可能提示支撑区域。",
        "context": "通常在下跌后或潜在支撑区域观察。",
        "confirmation": "观察价格是否随后走强，并结合更多触及该价格的历史信息。",
        "pitfall": "两次低点相同也可能只是暂时巧合，不能保证支撑有效。",
    },
    {
        "group": "双根组合", "name": "镊子顶（Tweezer Top）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(97, 105, 95, 103), (104, 105, 98, 99)], "structure": "两根相邻 K 线的最高价大致相同，第二根出现回落。",
        "recognize": "- 两次高点接近。\n- 第二根价格表现转弱。\n- 关键是共同高位是否真的形成阻力，而不是追求形状完美。",
        "meaning": "传统解读为同一高位两次未能突破，可能提示卖压或阻力。",
        "context": "通常在上涨后或潜在阻力附近观察。",
        "confirmation": "看后续价格是否下行，并确认高位区域是否多次出现反应。",
        "pitfall": "把两根高点相近的 K 线当成必然反转。",
    },
    {
        "group": "双根组合", "name": "内包线（Inside Bar）", "bias": "中性／波动收窄", "trend": "up",
        "bars": [(100, 110, 95, 107), (106, 108, 99, 104)], "structure": "第二根的最高价低于第一根最高价，最低价高于第一根最低价。",
        "recognize": "- 比较整根 K 线高低范围，不只是实体。\n- 第二根完全落在第一根范围内。",
        "meaning": "价格区间收窄，可能表示暂停或短期波动压缩；突破方向在发生前并不确定。",
        "context": "既可能出现在趋势中的整理，也可能出现在横盘阶段。",
        "confirmation": "等待价格向区间上方或下方突破，并检查突破是否持续。",
        "pitfall": "提前假定突破方向，或把震荡压缩当成方向确认。",
    },
    {
        "group": "三根组合", "name": "早晨之星（Morning Star）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(108, 110, 97, 98), (96, 99, 94, 97), (97, 106, 96, 105)], "structure": "第一根较强阴线，第二根小实体或犹豫 K 线，第三根较强阳线并显著收复第一根实体。",
        "recognize": "- 三根构成：明显卖压 → 犹豫／停顿 → 买方回升。\n- 经典定义会考虑第二根与前后实体的间隔；不同市场未必都出现跳空。\n- 第三根恢复幅度很重要。",
        "meaning": "传统上被视为下跌动能可能减弱、价格开始恢复的组合。",
        "context": "需要此前有下跌趋势；若第三根没有明显回升，形态质量较弱。",
        "confirmation": "关注第三根收盘是否越过第一根实体中段，随后是否继续走强。",
        "pitfall": "只数三根 K 线而不看第三根恢复幅度，也不看趋势背景。",
    },
    {
        "group": "三根组合", "name": "黄昏之星（Evening Star）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(98, 109, 97, 108), (109, 112, 108, 110), (110, 111, 101, 102)], "structure": "第一根较强阳线，第二根小实体或犹豫 K 线，第三根较强阴线并明显跌回第一根实体。",
        "recognize": "- 三根构成：上涨 → 犹豫／停顿 → 卖方回压。\n- 经典定义通常考虑中间实体与第三根回落幅度；跳空要求依市场与教材定义而异。",
        "meaning": "传统上被视为上涨动能可能减弱，价格开始回落的组合。",
        "context": "通常在此前上涨或阻力区域分析。",
        "confirmation": "看第三根是否跌入第一根实体中段以下，之后能否继续转弱。",
        "pitfall": "无视后续价格仍可能重新走强；三根组合也会失败。",
    },
    {
        "group": "三根组合", "name": "早晨十字星（Morning Doji Star）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(108, 110, 97, 98), (96, 99, 93, 96.05), (97, 106, 96, 105)], "structure": "早晨之星的中间一根是十字星：开盘和收盘非常接近。",
        "recognize": "- 第一根卖压明显。\n- 中间出现开收盘接近的十字星。\n- 第三根应表现出较明确的回升。",
        "meaning": "中间十字星强化了‘停顿／犹豫’的视觉描述，但并不自动令反转更可靠。",
        "context": "通常在下跌后观察，并要比较此前实体是否明显。",
        "confirmation": "第三根强势收盘及后续走势提供额外信息；不能只凭十字星判断。",
        "pitfall": "把十字星本身当成方向信号。",
    },
    {
        "group": "三根组合", "name": "黄昏十字星（Evening Doji Star）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(98, 109, 97, 108), (110, 114, 107, 110.05), (110, 111, 101, 102)], "structure": "黄昏之星的中间一根是开收盘接近的十字星。",
        "recognize": "- 第一根为明显上涨。\n- 中间为十字星。\n- 第三根出现较强回落。",
        "meaning": "传统解读将其视为上涨后动能暂停、随后卖压增加的组合。",
        "context": "一般在此前上涨或阻力区域关注。",
        "confirmation": "观察第三根收盘与后续价格能否持续转弱。",
        "pitfall": "把中间的十字星误认为一定见顶。",
    },
    {
        "group": "三根组合", "name": "三白兵（Three White Soldiers）", "bias": "连续偏多的价格行为", "trend": "down",
        "bars": [(95, 102, 94, 101), (100, 106, 99, 105), (104, 110, 103, 109)], "structure": "三根较强阳线连续出现，收盘价逐步抬高，实体通常较明显。",
        "recognize": "- 三根均呈上涨收盘。\n- 收盘逐步走高，实体不宜过小。\n- 理想版本的开盘通常位于前一实体附近，具体定义会有差异。",
        "meaning": "显示连续多个周期买方占优，传统上被视为转强或趋势延续的表现。",
        "context": "出现在下跌后可讨论恢复；若上涨已经延伸很多，也可能代表短期过热。",
        "confirmation": "看后续是否稳住、是否靠近阻力，以及成交量与市场背景。",
        "pitfall": "在连续大涨后追逐图形，忽略风险收益比和过度延伸。",
    },
    {
        "group": "三根组合", "name": "三只乌鸦（Three Black Crows）", "bias": "连续偏空的价格行为", "trend": "up",
        "bars": [(109, 110, 102, 103), (104, 105, 98, 99), (100, 101, 94, 95)], "structure": "三根较强阴线连续出现，收盘价逐步降低。",
        "recognize": "- 三根均为下跌收盘。\n- 收盘逐步走低，实体通常较明显。\n- 需检查是否发生在上涨后，还是已经大幅下跌之后。",
        "meaning": "表现为连续卖压，传统上被视为转弱或下跌延续的价格行为。",
        "context": "在一段上涨后值得观察；在过度下跌后追空则可能面临反弹风险。",
        "confirmation": "检查支撑位置、后续是否继续下行，以及是否有新基本面信息。",
        "pitfall": "把已经发生的连续下跌当成未来仍会下跌的保证。",
    },
    {
        "group": "三根组合", "name": "看涨三内升（Three Inside Up）", "bias": "下跌后可能偏多", "trend": "down",
        "bars": [(110, 111, 99, 100), (101, 105, 100, 104), (104, 112, 103, 111)], "structure": "先出现长阴线，第二根较小实体位于第一根实体内部，第三根上涨并收在第一根开盘价上方。",
        "recognize": "- 由孕线式的两根组合再加第三根向上确认构成。\n- 第三根应明显越过第一根实体开盘附近。",
        "meaning": "传统解读为下跌后先出现犹豫，再有买方回升。",
        "context": "需有下跌背景，且第三根必须提供更明确的方向信息。",
        "confirmation": "观察后续能否维持在突破位置上方。",
        "pitfall": "只凭前两根的内包结构就预判已经反转。",
    },
    {
        "group": "三根组合", "name": "看跌三内降（Three Inside Down）", "bias": "上涨后可能偏空", "trend": "up",
        "bars": [(100, 111, 99, 110), (109, 110, 105, 106), (106, 107, 98, 99)], "structure": "先出现长阳线，第二根较小实体位于第一根实体内部，第三根下跌并收在第一根开盘价下方。",
        "recognize": "- 由孕线式两根组合加第三根向下确认构成。\n- 第三根收盘应越过第一根开盘附近，显示更明确的转弱。",
        "meaning": "传统解读为上涨后出现犹豫，随后卖方进一步压低价格。",
        "context": "需结合此前上涨、阻力区域和第三根的回落幅度。",
        "confirmation": "检查后续是否继续走弱，或很快重新收复失地。",
        "pitfall": "把第三根的短期下跌当成长期熊市的确定证据。",
    },
    {
        "group": "多根持续形态", "name": "上升三法（Rising Three Methods）", "bias": "上升趋势中的潜在整理延续", "trend": "up",
        "bars": [(100, 111, 99, 110), (109, 110, 105, 106), (108, 109, 104, 105), (106, 108, 103, 104), (105, 115, 104, 114)], "structure": "先有较强阳线，中间出现数根较小的逆势整理 K 线且大致留在第一根范围内，最后一根向上突破。",
        "recognize": "- 经典版本通常是五根左右的组合。\n- 中间整理幅度相对有限。\n- 最后一根恢复上涨并越过前面整理区间。",
        "meaning": "传统上被视为强势趋势中的暂时休息，随后可能延续原方向。",
        "context": "必须先有明确上升动能；若中间跌破关键结构，解释会改变。",
        "confirmation": "观察最后一根能否有效突破，后续是否守住，并评估成交量与整体趋势。",
        "pitfall": "任何上涨后横盘都叫上升三法，忽略中间 K 线的位置与最终突破。",
    },
    {
        "group": "多根持续形态", "name": "下降三法（Falling Three Methods）", "bias": "下降趋势中的潜在整理延续", "trend": "down",
        "bars": [(110, 111, 99, 100), (101, 106, 100, 105), (103, 108, 102, 107), (105, 109, 103, 108), (109, 110, 95, 96)], "structure": "先有较强阴线，中间出现数根较小的逆势反弹 K 线且大致位于第一根范围内，最后一根向下突破。",
        "recognize": "- 经典版本通常包含数根小幅反弹的 K 线。\n- 中间反弹没有改变更大的下降结构。\n- 最后一根出现新的下跌推进。",
        "meaning": "传统上被视为下跌趋势中的暂时反弹，随后可能延续原方向。",
        "context": "要有此前下降动能；中间反弹若改变了结构，就不应强行命名为下降三法。",
        "confirmation": "检查最后一根是否跌破整理区间，后续是否持续，以及支撑和消息背景。",
        "pitfall": "把任何小反弹都当作下跌延续形态，忽略趋势可能已经改变。",
    },
]


def build_candle_pattern_figure(pattern: dict) -> go.Figure:
    """Create a schematic OHLC chart with a synthetic trend prefix and selected pattern."""
    bars = pattern["bars"]
    first_open = float(bars[0][0])
    trend = pattern.get("trend", "sideways")
    if trend == "down":
        closes = [first_open + 8, first_open + 6, first_open + 3.5, first_open + 1.2]
        prefix = []
        prev = closes[0] + 1.2
        for close in closes:
            open_ = prev
            high = max(open_, close) + 0.7
            low = min(open_, close) - 0.6
            prefix.append((open_, high, low, close))
            prev = close
    elif trend == "up":
        closes = [first_open - 8, first_open - 6, first_open - 3.5, first_open - 1.2]
        prefix = []
        prev = closes[0] - 1.2
        for close in closes:
            open_ = prev
            high = max(open_, close) + 0.6
            low = min(open_, close) - 0.7
            prefix.append((open_, high, low, close))
            prev = close
    else:
        offsets = [-1.4, 0.8, -0.7, 0.5]
        prefix = []
        prev = first_open - 0.2
        for offset in offsets:
            close = first_open + offset
            open_ = prev
            high = max(open_, close) + 1.0
            low = min(open_, close) - 1.0
            prefix.append((open_, high, low, close))
            prev = close

    labels = [f"背景 {i+1}" for i in range(len(prefix))] + [f"形态 {i+1}" for i in range(len(bars))]
    all_bars = prefix + [tuple(map(float, bar)) for bar in bars]
    prefix_bars, pattern_bars = all_bars[:len(prefix)], all_bars[len(prefix):]
    fig = go.Figure()
    if prefix_bars:
        fig.add_trace(go.Candlestick(
            x=labels[:len(prefix_bars)],
            open=[b[0] for b in prefix_bars], high=[b[1] for b in prefix_bars],
            low=[b[2] for b in prefix_bars], close=[b[3] for b in prefix_bars],
            name="背景走势", increasing_line_color="#8ea5bf", decreasing_line_color="#64758d",
            increasing_fillcolor="#8ea5bf", decreasing_fillcolor="#64758d",
        ))
    fig.add_trace(go.Candlestick(
        x=labels[len(prefix):],
        open=[b[0] for b in pattern_bars], high=[b[1] for b in pattern_bars],
        low=[b[2] for b in pattern_bars], close=[b[3] for b in pattern_bars],
        name="所选形态", increasing_line_color="#60e2bd", decreasing_line_color="#ff8f9b",
        increasing_fillcolor="#60e2bd", decreasing_fillcolor="#ff8f9b",
    ))
    fig.update_layout(
        title=dict(text=f"{pattern['name']} · 合成示意图", x=0.02, xanchor="left"),
        xaxis_title="先看背景，再看形态本身",
        yaxis_title="示意价格（非真实行情）",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        # Keep the legend outside the plot area, below the x-axis labels.
        # Extra bottom margin prevents the legend from colliding with the chart.
        legend=dict(orientation="h", yanchor="top", y=-0.24, xanchor="left", x=0),
        margin=dict(l=30, r=28, t=82, b=112),
        height=490,
    )
    return fig


# ============================================================
# Sidebar navigation
# ============================================================
if "completed_lessons" not in st.session_state:
    st.session_state["completed_lessons"] = []
if "quiz_attempts" not in st.session_state:
    st.session_state["quiz_attempts"] = {}
if "main_sidebar_collapsed" not in st.session_state:
    st.session_state["main_sidebar_collapsed"] = False

# Legacy navigation keys for the retired risk/allocation course return to the learning home.
if st.session_state.get("main_nav") in {"06 收益与风险", "07 资产配置与模拟练习", "06 收益、风险与资产配置"}:
    st.session_state["main_nav"] = "学习首页"
if st.session_state.get("main_nav") in {"07 风险与投资者保护", "08 风险与投资者保护"}:
    st.session_state["main_nav"] = "06 风险与投资者保护"

PAGES = [
    "学习首页",
    "01 股票市场基础",
    "02 看懂行情",
    "02A 蜡烛图形态学",
    "02B 技术指标入门",
    "03 交易如何执行",
    "04 研究一家公司",
    "05 股价为什么变化",
    "06 风险与投资者保护",
    "综合测验",
    "数据与方法",
]

if not st.session_state["main_sidebar_collapsed"]:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-row">
              <div class="brand-mark">S</div>
              <div><div class="brand-name">StockScope</div><div class="brand-sub">Learn · Market Basics</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("← 收起主菜单", key="collapse_main_sidebar", width="stretch"):
            st.session_state["main_sidebar_collapsed"] = True
            st.rerun()
        st.markdown("**你的学习路线**")
        chosen_page = st.radio("导航", PAGES, key="main_nav", label_visibility="collapsed")
        _previous_page = st.session_state.get("_last_main_nav_for_scroll")
        _page_changed = _previous_page is not None and _previous_page != chosen_page
        if "_scroll_sequence" not in st.session_state:
            st.session_state["_scroll_sequence"] = 0
        if _page_changed:
            st.session_state["_scroll_sequence"] += 1
        st.session_state["_last_main_nav_for_scroll"] = chosen_page
        st.markdown("---")
        completed = set(st.session_state["completed_lessons"])
        progress = len(completed.intersection(set(LESSON_GUIDE.keys()))) / len(LESSON_GUIDE)
        st.caption("课程完成进度")
        st.progress(progress, text=f"已完成 {round(progress * 100)}%")
        quiz_stats = st.session_state.get("quiz_attempts", {})
        mastered_count = sum(bool(quiz_stats.get(name, {}).get("passed")) for name in LESSON_GUIDE)
        st.caption("练习掌握度（通过至少一次课内检查）")
        st.progress(mastered_count / len(LESSON_GUIDE), text=f"{mastered_count}/{len(LESSON_GUIDE)} 课已通过检查")
        st.markdown("---")
        st.caption("数据来源")
        st.caption("Yahoo Finance / yfinance（原型用途）")
        st.caption("各图表在对应页面单独设置历史范围。")
        st.caption("本网站用于学习，不构成投资建议。")
else:
    # The floating control remains available after the sidebar contents are hidden.
    st.markdown(
        """<style>
        [data-testid="stSidebar"] { display: none !important; }
        div.st-key-expand_main_sidebar {
          position: fixed !important; left: .55rem !important; top: 3.65rem !important;
          z-index: 100000 !important; width: 154px !important; max-width: calc(100vw - 1rem) !important;
        }
        div.st-key-expand_main_sidebar button {
          min-height: 2.2rem !important; padding: .35rem .65rem !important;
          background: rgba(15,29,46,.97) !important; color: #e9f0fb !important;
          border: 1px solid rgba(96,226,189,.55) !important; box-shadow: 0 5px 18px rgba(0,0,0,.25);
        }
        </style>""",
        unsafe_allow_html=True,
    )
    if st.button("☰ 展开主菜单", key="expand_main_sidebar"):
        st.session_state["main_sidebar_collapsed"] = False
        st.rerun()
    chosen_page = st.session_state.get("main_nav", "学习首页")
    _previous_page = st.session_state.get("_last_main_nav_for_scroll")
    _page_changed = _previous_page is not None and _previous_page != chosen_page
    if "_scroll_sequence" not in st.session_state:
        st.session_state["_scroll_sequence"] = 0
    if _page_changed:
        st.session_state["_scroll_sequence"] += 1
    st.session_state["_last_main_nav_for_scroll"] = chosen_page


# Stable top target. The actual scroll script is emitted at EOF after the page
# contents have been written, which avoids running before Streamlit's DOM exists.
st.markdown('<div id="stockscope-main-top" style="height:1px;scroll-margin-top:0" aria-hidden="true"></div>', unsafe_allow_html=True)

# ============================================================
# Home
# ============================================================
if chosen_page == "学习首页":
    # Cinematic homepage: 7 selected finance/trading clips with directional scroll reveals.
    # The sidebar is hidden only while the homepage is active; lesson navigation remains
    # available in the course hub below and returns to the regular sidebar on lesson pages.
    st.markdown(
        """
        <style>
          .stApp:has(.cinematic-bg) [data-testid="stSidebar"],
          .stApp:has(.cinematic-bg) [data-testid="stHeader"] { display:none !important; }
          /* Keep Streamlit's main pane as the vertical scroll container.
             Setting overflow:visible on stMain disables wheel/touch scrolling. */
          .stApp:has(.cinematic-bg) [data-testid="stAppViewContainer"] {
            background: transparent !important; overflow: hidden !important;
          }
          .stApp:has(.cinematic-bg) [data-testid="stMainBlockContainer"] {
            background: transparent !important; overflow: visible !important;
          }
          .stApp:has(.cinematic-bg) [data-testid="stMain"] {
            margin-left:0 !important; width:100% !important; max-width:none !important;
            background: transparent !important; min-height: 0 !important;
            overflow-y: auto !important; overflow-x: hidden !important;
            overscroll-behavior-y: auto; scroll-behavior: smooth;
          }
          .stApp:has(.cinematic-bg) .block-container,
          .stApp:has(.cinematic-bg) [data-testid="stMainBlockContainer"] {
            max-width: 1480px !important; padding-top: 0 !important;
          }
          .stApp:has(.cinematic-bg) .block-container { padding-bottom: 4rem !important; }
          .stApp:has(.cinematic-bg) [data-testid="stMarkdownContainer"] { overflow: visible; }
          .stApp:has(.cinematic-bg) [data-testid="stMainBlockContainer"] > div { position:relative; z-index:1; }
          .cinematic-bg {
            position:fixed; inset:0; width:100vw; height:100vh; height:100svh;
            z-index:0; overflow:hidden; pointer-events:none; isolation:isolate;
            background:
              radial-gradient(ellipse at 78% 30%, rgba(34,91,120,.42), transparent 42%),
              radial-gradient(ellipse at 18% 72%, rgba(20,91,85,.3), transparent 38%),
              linear-gradient(120deg,#06101d 0%,#091a29 52%,#08111f 100%);
          }
          .cinematic-bg video {
            position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
            opacity:0; transition:none !important;
            /* Hard cuts avoid rendering overlapping video layers during transitions. */
            filter:brightness(.88) saturate(.84) contrast(1.03);
            transform:scale(1.015); will-change:auto;
          }
          .cinematic-bg video.is-visible { opacity:.58; }
          .cinematic-bg.video-fallback video { display:none !important; }
          .cinematic-bg::before {
            content:""; position:absolute; z-index:1; inset:0;
            background:linear-gradient(90deg,rgba(3,9,17,.82) 0%,rgba(3,9,17,.58) 40%,rgba(3,9,17,.16) 74%,rgba(3,9,17,.46) 100%),
                       linear-gradient(0deg,rgba(3,9,17,.78),transparent 45%,rgba(3,9,17,.16));
          }
          .cinematic-bg::after {
            content:""; position:absolute; z-index:2; inset:0; opacity:.18;
            background-image:linear-gradient(rgba(192,218,242,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(192,218,242,.07) 1px,transparent 1px);
            background-size:88px 88px; mask-image:linear-gradient(90deg,black,transparent 82%);
          }
          .cinematic-home {
            position:relative; z-index:1; width:100vw; margin-left:calc(50% - 50vw);
            color:#f5f8fc; overflow:clip; background:transparent;
          }
          .cinematic-header {
            position:absolute; z-index:4; top:0; left:0; width:100%; box-sizing:border-box;
            display:flex; align-items:center; justify-content:space-between; gap:1rem;
            padding:1.45rem clamp(1.25rem,5.5vw,6rem);
            border-bottom:1px solid rgba(222,237,250,.13);
          }
          .cinematic-brand { display:flex; gap:.8rem; align-items:center; color:#f3f7fc; text-decoration:none; }
          .cinematic-brand-mark { display:grid; place-items:center; width:38px;height:38px;border-radius:12px;
            color:#06151e;font-weight:950;background:linear-gradient(140deg,#80edd0,#80baff); }
          .cinematic-brand-name {font-size:1rem;font-weight:850;letter-spacing:.02em;line-height:1.1;}
          .cinematic-brand-sub {font-size:.65rem;letter-spacing:.18em;color:#9ab1c8;text-transform:uppercase;margin-top:4px;}
          .cinematic-top-link { color:#e7f3fb !important;text-decoration:none !important;font-size:.82rem;font-weight:750;
            border:1px solid rgba(222,237,250,.32);border-radius:999px;padding:.72rem 1rem;transition:background .2s,border-color .2s; }
          .cinematic-top-link:hover {background:rgba(255,255,255,.11);border-color:rgba(155,237,219,.7);}
          .cinematic-scene {
            box-sizing:border-box; width:100%; min-height:100vh; min-height:100svh;
            padding:clamp(7rem,12vh,10rem) clamp(1.25rem,9vw,10rem) clamp(4.5rem,9vh,7rem);
            display:flex; flex-direction:column; justify-content:center; position:relative;
            border-bottom:1px solid rgba(203,226,244,.12); scroll-margin-top:0;
          }
          .cinematic-scene::after {content:"";position:absolute;left:clamp(1.25rem,9vw,10rem);bottom:2rem;width:clamp(56px,8vw,120px);height:1px;background:linear-gradient(90deg,#7fe7cc,rgba(127,231,204,0));}
          .cinematic-hero-scene {min-height:100vh;min-height:100svh;padding-top:9rem;}
          .cinematic-eyebrow {font-size:.72rem;font-weight:850;letter-spacing:.22em;color:#90ead5;text-transform:uppercase;margin-bottom:1.5rem;}
          .cinematic-h1 {max-width:1000px;font-size:clamp(3rem,7.6vw,7.7rem);letter-spacing:-.065em;line-height:.99;font-weight:820;margin:0 0 1.5rem;color:#f5f8fc;}
          .cinematic-h1 span {display:block;color:#a7c9ef;}
          .cinematic-lead {font-size:clamp(1rem,1.4vw,1.2rem);line-height:1.8;max-width:650px;color:#c2d1df;margin:0 0 2rem;}
          .cinematic-actions {display:flex;align-items:center;gap:1rem;flex-wrap:wrap;}
          .cinematic-cta {display:inline-flex;align-items:center;gap:.8rem;padding:.94rem 1.2rem;border-radius:999px;
            background:#e7f7f2;color:#08221f !important;text-decoration:none !important;font-weight:850;font-size:.88rem;}
          .cinematic-cta:hover {background:#a7efd9;}
          .cinematic-quiet-link {color:#d8e4f0 !important;text-decoration:none !important;font-size:.87rem;border-bottom:1px solid rgba(216,228,240,.5);padding:.45rem 0;}
          .cinematic-scroll-note {position:absolute;z-index:5;right:clamp(1.25rem,5.5vw,6rem);bottom:2.3rem;display:flex;align-items:center;gap:.85rem;
            color:#b4c5d7 !important;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;writing-mode:vertical-rl;
            text-decoration:none !important;cursor:pointer;opacity:.92;}
          .cinematic-scroll-note:hover {color:#9cf0db !important;opacity:1;}
          .cinematic-scroll-note i {display:block;width:1px;height:56px;background:linear-gradient(#86e9d1,rgba(134,233,209,0));}
          .cinematic-bottom-meta {display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:clamp(3rem,9vh,6.5rem);color:#90a8be;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;}
          .cinematic-bottom-meta span::before {content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:#85e7ce;margin:0 .55rem .12rem 0;}
          .cinematic-story-grid {display:grid;grid-template-columns:minmax(140px,.65fr) minmax(0,1.8fr);gap:clamp(2rem,7vw,8rem);width:100%;max-width:1300px;margin:0 auto;align-items:start;}
          .cinematic-chapter {color:#8aabc3;font-size:.72rem;letter-spacing:.17em;text-transform:uppercase;padding-top:.55rem;}
          .cinematic-chapter b {display:block;color:#85e7ce;font-size:1.2rem;letter-spacing:.03em;margin-bottom:.55rem;}
          .cinematic-story-kicker {font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:#93ead5;font-weight:850;margin-bottom:1.25rem;}
          .cinematic-story-title {font-size:clamp(2.3rem,5.4vw,5.4rem);line-height:1.04;letter-spacing:-.055em;font-weight:800;max-width:930px;margin:0 0 1.4rem;color:#f4f7fb;}
          .cinematic-story-title em {font-style:normal;color:#a4c9ee;}
          /* Featured chapter title: first phrase enters from the left, the emphasis follows. */
          .signal-title .signal-title-first,
          .signal-title .signal-title-second {display:inline-block;}
          .signal-title-rule {
            width:clamp(120px,25vw,360px);height:1px;margin:-.45rem 0 1.35rem;
            transform:scaleX(1);transform-origin:left center;opacity:.85;
            background:linear-gradient(90deg,#82e7d0 0%,rgba(130,231,208,.42) 68%,rgba(130,231,208,0) 100%);
          }
          .cinematic-home.reveal-ready .signal-title[data-title-reveal] .signal-title-first,
          .cinematic-home.reveal-ready .signal-title[data-title-reveal] .signal-title-second {
            opacity:0;transform:translate3d(-38px,0,0);
          }
          .cinematic-home.reveal-ready .signal-title[data-title-reveal].is-inview .signal-title-first {
            animation:signal-title-slide-in .72s cubic-bezier(.2,.72,.2,1) both;
          }
          .cinematic-home.reveal-ready .signal-title[data-title-reveal].is-inview .signal-title-second {
            animation:signal-title-slide-in .72s cubic-bezier(.2,.72,.2,1) .2s both;
          }
          .cinematic-home.reveal-ready .signal-title-rule {transform:scaleX(0);}
          .cinematic-home.reveal-ready .signal-title[data-title-reveal].is-inview + .signal-title-rule {
            animation:signal-title-rule-grow .68s ease-out .43s both;
          }
          @keyframes signal-title-slide-in {
            from {opacity:0;transform:translate3d(-38px,0,0);}
            to {opacity:1;transform:translate3d(0,0,0);}
          }
          @keyframes signal-title-rule-grow {
            from {transform:scaleX(0);opacity:.2;}
            to {transform:scaleX(1);opacity:.85;}
          }
          .cinematic-story-copy {font-size:clamp(1rem,1.3vw,1.16rem);line-height:1.85;max-width:720px;color:#bdccdc;margin:0;}
          .cinematic-story-foot {margin-top:2rem;display:flex;align-items:center;gap:.7rem;color:#95aabe;font-size:.77rem;letter-spacing:.04em;}
          .cinematic-story-foot span {width:34px;height:1px;background:#80e6ce;display:inline-block;}
          /* Keep content visible by default. Directional scroll reveals activate only
             after the controller is ready, so a script failure never hides page copy. */
          .cinematic-home [data-reveal] {opacity:1;transform:none;}
          .cinematic-home.reveal-ready [data-reveal] {
            opacity:0; transform:translate3d(0,28px,0);
            transition:opacity .78s cubic-bezier(.2,.7,.2,1), transform .88s cubic-bezier(.2,.7,.2,1);
            will-change:opacity,transform;
          }
          .cinematic-home.reveal-ready [data-reveal="left"] {transform:translate3d(-64px,0,0);}
          .cinematic-home.reveal-ready [data-reveal="right"] {transform:translate3d(64px,0,0);}
          .cinematic-home.reveal-ready [data-reveal="up"] {transform:translate3d(0,28px,0);}
          .cinematic-home.reveal-ready [data-reveal].is-inview {opacity:1;transform:translate3d(0,0,0);}
          .cinematic-source {font-size:.68rem;line-height:1.5;color:#8298ad;margin:1rem 0 0;}
          .cinematic-source a {color:#9fbed4 !important;}
          .home-path-anchor {height:1px;scroll-margin-top:0;}
          @media (max-width:760px) {
            .cinematic-header {padding:1rem 1.1rem;}
            .cinematic-brand-mark {width:34px;height:34px;}
            .cinematic-brand-name {font-size:.9rem;}
            .cinematic-brand-sub {font-size:.56rem;}
            .cinematic-top-link {font-size:.75rem;padding:.65rem .8rem;}
            .cinematic-scene {padding:7rem 1.35rem 5rem;min-height:90vh;min-height:90svh;}
            .cinematic-hero-scene {min-height:100vh;min-height:100svh;padding-top:8rem;}
            .cinematic-h1 {font-size:clamp(2.8rem,13vw,4.6rem);}
            .cinematic-scroll-note {right:1rem;bottom:1.4rem;font-size:.6rem;}
            .cinematic-story-grid {grid-template-columns:1fr;gap:1.15rem;}
            .cinematic-chapter {padding-top:0;}
            .cinematic-chapter b {display:inline;margin-right:.75rem;}
            .cinematic-story-title {font-size:clamp(2.3rem,10.5vw,3.8rem);}
            .cinematic-bottom-meta {margin-top:2.4rem;gap:.8rem;}
          }
          @media (prefers-reduced-motion: reduce) {
            .cinematic-bg video {display:none !important;}
            .cinematic-home *, .cinematic-home *::before, .cinematic-home *::after {animation:none !important;transition:none !important;scroll-behavior:auto !important;}
            .cinematic-home.reveal-ready [data-reveal] {opacity:1 !important;transform:none !important;}
            .cinematic-home.reveal-ready .signal-title [class^="signal-title-"] {opacity:1 !important;transform:none !important;animation:none !important;}
            .cinematic-home.reveal-ready .signal-title-rule {transform:scaleX(1) !important;animation:none !important;}
          }
        </style>
        <div class="cinematic-bg" aria-hidden="true">
          <video id="cinematic-video-a" class="is-visible" muted playsinline preload="metadata" aria-label="金融市场主题视频背景第一段"></video>
          <video id="cinematic-video-b" muted playsinline preload="metadata" aria-label="金融市场主题视频背景交替片段"></video>
        </div>
        <div class="cinematic-home">
          <header class="cinematic-header">
            <a class="cinematic-brand" href="#stockscope-main-top" aria-label="StockScope Learn 首页">
              <span class="cinematic-brand-mark">S</span>
              <span><span class="cinematic-brand-name">StockScope</span><span class="cinematic-brand-sub" style="display:block">Learn · Market Basics</span></span>
            </a>
            <a class="cinematic-top-link" href="#home-learning-path">探索学习路径 ↘</a>
          </header>

          <section class="cinematic-scene cinematic-hero-scene" id="cinematic-start">
            <div class="cinematic-eyebrow" data-reveal="left">STOCKSCOPE LEARN · FINANCIAL LITERACY</div>
            <h1 class="cinematic-h1" data-reveal="left">在噪音之中，<span>看见市场的逻辑。</span></h1>
            <p class="cinematic-lead" data-reveal="right">市场不只是一串不断变化的价格。它由公司、预期、资金与风险共同构成。StockScope 带你从基础开始，学会看懂数据，也学会追问数据背后的原因。</p>
            <div class="cinematic-actions" data-reveal="left">
              <a class="cinematic-cta" href="#home-learning-path">开始探索课程 <span aria-hidden="true">↘</span></a>
              <a class="cinematic-quiet-link" href="#cinematic-signal">向下滚动，了解市场</a>
            </div>
            <div class="cinematic-bottom-meta" data-reveal="right"><span>价格与成交量</span><span>公司与价值</span><span>收益与风险</span></div>
            <a class="cinematic-scroll-note" href="#cinematic-signal" aria-label="向下滚动或点击继续探索市场"><i></i>向下滚动 · 点击继续</a>
          </section>

          <section class="cinematic-scene" id="cinematic-signal">
            <div class="cinematic-story-grid">
              <div class="cinematic-chapter" data-reveal="left"><b>01 / SIGNAL</b>价格 · 成交量</div>
              <div>
                <div class="cinematic-story-kicker" data-reveal="right">Read the Market</div>
                <h2 class="cinematic-story-title signal-title" data-title-reveal="signal" aria-label="先看见变化，再理解变化。"><span class="signal-title-first">先看见变化，</span><em class="signal-title-second">再理解变化。</em></h2>
                <div class="signal-title-rule" aria-hidden="true"></div>
                <p class="cinematic-story-copy" data-reveal="right">价格告诉你市场在某个时点如何给资产定价，成交量则补充交易活跃程度。K 线、趋势与波动提供观察线索，但真正的分析始于比较：与过去相比发生了什么？变化出现在什么背景下？哪些信息仍然未知？</p>
                <div class="cinematic-story-foot" data-reveal="right"><span></span>从读懂行情开始建立市场语言</div>
              </div>
            </div>
          </section>

          <section class="cinematic-scene" id="cinematic-company">
            <div class="cinematic-story-grid">
              <div class="cinematic-chapter" data-reveal="left"><b>02 / BUSINESS</b>收入 · 利润 · 现金</div>
              <div data-reveal="right"><div class="cinematic-story-kicker">Understand the Business</div>
                <h2 class="cinematic-story-title">价格在屏幕上，<em>价值在生意里。</em></h2>
                <p class="cinematic-story-copy">研究一家公司，不是只看股价涨跌。你需要理解它如何赚钱、成本怎样变化、利润能否转化为现金，以及资产负债表能否支撑未来经营。财务报表不是一组孤立数字，而是同一门生意从不同角度留下的记录。</p>
                <div class="cinematic-story-foot"><span></span>从公司经营理解价格背后的基础</div>
              </div>
            </div>
          </section>

          <section class="cinematic-scene" id="cinematic-risk">
            <div class="cinematic-story-grid">
              <div class="cinematic-chapter" data-reveal="left"><b>03 / RISK</b>回报 · 不确定性</div>
              <div data-reveal="right"><div class="cinematic-story-kicker">Think in Risk and Return</div>
                <h2 class="cinematic-story-title">不是预测一切，<em>而是做好判断。</em></h2>
                <p class="cinematic-story-copy">投资中的收益总与不确定性相伴。理解风险、核实信息并避免过度自信，有助于建立更有依据的判断方法。</p>
              </div>
            </div>
          </section>
          <div class="home-path-anchor" id="home-learning-path"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Streamlit strips inline scripts from markdown, so this component controls a two-video
    # preload playlist with direct hard cuts (no opacity fade).
    components.html(
        """
        <script>
        (() => {
          let doc;
          try { doc = window.parent.document; } catch (_) { return; }
          const bg = doc.querySelector('.cinematic-bg');
          const a = doc.getElementById('cinematic-video-a');
          const b = doc.getElementById('cinematic-video-b');
          if (!bg || !a || !b) return;
          // Reinforce the main wheel/touch scroll container at runtime as well as in CSS.
          const mainPane = doc.querySelector('[data-testid="stMain"]');
          if (mainPane) {
            mainPane.style.setProperty('min-height', '0', 'important');
            mainPane.style.setProperty('overflow-y', 'auto', 'important');
            mainPane.style.setProperty('overflow-x', 'hidden', 'important');
            mainPane.style.setProperty('overscroll-behavior-y', 'auto', 'important');
          }
          try {
            if (window.parent.matchMedia('(prefers-reduced-motion: reduce)').matches) {
              bg.classList.add('video-fallback');
              return;
            }
          } catch (_) {}

          // V12 keeps seven finance/trading clips: remove old clips 2, 4 and 10, then swap old clips 6 and 7.
          // Direct hard cuts; no fade transition and no institutional video cards.
          // The final clip is the user-selected Coverr trader phone-call shot; the original page is retained as the source.
          const clips = [
            {src: 'https://videos.pexels.com/video-files/36418660/15442087_1920_1080_25fps.mp4', page: 'https://www.pexels.com/video/financial-analyst-monitors-trading-data-on-screen-36418660/', label: '金融分析师与多屏行情'},
            {src: 'https://videos.pexels.com/video-files/8124270/8124270-hd_1920_1080_30fps.mp4', page: 'https://www.pexels.com/video/a-business-man-studying-the-data-8124270/', label: '金融团队研究图表'},
            {src: 'https://videos.pexels.com/video-files/7693394/7693394-hd_1920_1080_25fps.mp4', page: 'https://www.pexels.com/video/working-on-trading-7693394/', label: '交易员分析市场数据'},
            {src: 'https://videos.pexels.com/video-files/32388701/13815639_1920_1080_25fps.mp4', page: 'https://www.pexels.com/video/analyzing-stock-market-data-on-digital-tablet-32388701/', label: '移动端行情分析'},
            {src: 'https://videos.pexels.com/video-files/7841873/7841873-hd_1920_1080_30fps.mp4', page: 'https://www.pexels.com/video/men-shaking-hands-7841873/', label: '商务谈判与交易达成'},
            {src: 'https://videos.pexels.com/video-files/7552486/7552486-hd_1920_1080_25fps.mp4', page: 'https://www.pexels.com/video/people-in-a-meeting-7552486/', label: '金融团队策略会议'},
            {src: 'https://cdn.coverr.co/videos/coverr-a-trader-making-a-call-with-his-smartphone-do8qjfv1ym/1080p.mp4', page: 'https://coverr.co/videos/a-trader-making-a-call-with-his-smartphone-do8qjfv1ym', label: '交易员使用手机通话'},
          ];
          const RATE = 1.3;
          const CLIP_MS = 3000;
          let currentIndex = 0;
          let nextIndex = 1;
          let active = a;
          let standby = b;
          let pending = false;
          let transitioning = false;
          let failed = new Set();
          let transitionTimer = null;

          // Directional scroll reveals: left column enters from the left, right column from the right.
          const home = doc.querySelector('.cinematic-home');
          let reduceMotion = false;
          try { reduceMotion = window.parent.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (_) {}
          if (home) {
            const revealItems = Array.from(home.querySelectorAll('[data-reveal], [data-title-reveal]'));
            if (reduceMotion) {
              revealItems.forEach(el => el.classList.add('is-inview'));
            } else {
              home.classList.add('reveal-ready');
              try {
                const ParentObserver = window.parent.IntersectionObserver;
                if (!ParentObserver) throw new Error('IntersectionObserver unavailable');
                const revealObserver = new ParentObserver(entries => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      entry.target.classList.add('is-inview');
                      revealObserver.unobserve(entry.target);
                    }
                  });
                }, {root: mainPane || null, threshold: 0.12, rootMargin: '0px 0px -7% 0px'});
                revealItems.forEach(el => revealObserver.observe(el));
              } catch (_) {
                revealItems.forEach(el => el.classList.add('is-inview'));
              }
            }
          }
          if (reduceMotion) {
            bg.classList.add('video-fallback');
            return;
          }

          function clearTransitionTimer() {
            if (transitionTimer !== null) {
              window.clearTimeout(transitionTimer);
              transitionTimer = null;
            }
          }
          function nextUsableIndex(start) {
            for (let step = 0; step < clips.length; step++) {
              const candidate = (start + step + clips.length) % clips.length;
              if (!failed.has(candidate) && candidate !== currentIndex) return candidate;
            }
            return -1;
          }
          function prepare(video, index) {
            if (index < 0 || index >= clips.length) return;
            video.pause();
            video.classList.remove('is-visible');
            video.muted = true;
            video.playsInline = true;
            video.preload = 'auto';
            video.playbackRate = RATE;
            video.src = clips[index].src;
            video.load();
          }
          function playVideo(video) {
            video.muted = true;
            video.playsInline = true;
            video.preload = 'auto';
            video.playbackRate = RATE;
            const result = video.play();
            if (result && typeof result.catch === 'function') result.catch(() => {});
          }
          function scheduleNextTransition() {
            clearTransitionTimer();
            // Hold each shot for about three seconds, then switch instantly.
            transitionTimer = window.setTimeout(() => {
              transitionTimer = null;
              beginTransition();
            }, CLIP_MS);
          }
          function beginTransition() {
            if (transitioning) return;
            if (nextIndex < 0) {
              bg.classList.add('video-fallback');
              return;
            }
            // Wait for a decodable frame before an instant hard cut.
            if (standby.readyState < 3) {
              pending = true;
              return;
            }
            transitioning = true;
            pending = false;
            standby.playbackRate = RATE;
            playVideo(standby);
            // Instant hard cut: toggle both classes in one task, with no opacity animation.
            const previous = active;
            previous.classList.remove('is-visible');
            standby.classList.add('is-visible');
            bg.classList.remove('video-fallback');
            previous.pause();
            active = standby;
            standby = previous;
            currentIndex = nextIndex;
            nextIndex = nextUsableIndex((currentIndex + 1) % clips.length);
            transitioning = false;
            if (nextIndex < 0) return;
            prepare(standby, nextIndex);
            scheduleNextTransition();
          }
          function handleVideoError(video) {
            const badIndex = clips.findIndex(clip => clip.src === video.currentSrc || clip.src === video.src);
            if (badIndex >= 0) failed.add(badIndex);
            if (video === standby) {
              const next = nextUsableIndex((Math.max(0, badIndex) + 1) % clips.length);
              nextIndex = next;
              if (next >= 0) prepare(standby, next);
              else bg.classList.add('video-fallback');
              return;
            }
            if (video === active) {
              clearTransitionTimer();
              bg.classList.add('video-fallback');
              const next = nextUsableIndex((Math.max(0, badIndex) + 1) % clips.length);
              nextIndex = next;
              if (next >= 0) {
                if (standby.src !== clips[next].src) prepare(standby, next);
                if (standby.readyState >= 3) beginTransition();
                else pending = true;
              }
            }
          }
          [a, b].forEach(video => {
            video.addEventListener('canplay', () => {
              if (video === standby && pending) beginTransition();
            });
            video.addEventListener('error', () => handleVideoError(video));
          });
          a.addEventListener('playing', () => {
            if (active === a && !transitioning) scheduleNextTransition();
          }, {once: true});
          a.addEventListener('playing', () => bg.classList.remove('video-fallback'), {once: true});
          a.muted = true;
          a.playbackRate = RATE;
          a.src = clips[0].src;
          a.load();
          prepare(b, nextIndex);
          playVideo(a);
        })();
        </script>
        """,
        height=1,
        width=1,
        scrolling=False,
    )
    st.write("")
    completed = set(st.session_state["completed_lessons"])
    n_complete = len(completed.intersection(set(LESSON_GUIDE.keys())))
    m1, m2, m3 = st.columns(3)
    m1.metric("学习单元", f"{len(LESSON_GUIDE)} 个", "从概念到投资者保护")
    m2.metric("互动图表", "3+ 种", "折线图 · 柱状图 · 散点图")
    m3.metric("你的进度", f"{n_complete}/{len(LESSON_GUIDE)}", "已完成的课程")
    mastered = sum(bool(st.session_state.get("quiz_attempts", {}).get(name, {}).get("passed")) for name in LESSON_GUIDE)
    st.caption(f"知识检查：{mastered}/{len(LESSON_GUIDE)} 课至少通过一次。答错可以重试；通过测验与标记课程完成是两件不同的事。")

    st.write("")
    section_heading("REAL-WORLD CHALLENGE", "真实行情挑战", "观察真实历史行情，先独立判断，再揭晓后续走势。练习用于观察历史走势，不代表指标可以可靠预测未来。")

    # 01 — A real historical case, with no explicit signal clue until after submission.
    with st.container(border=True):
        st.markdown(
            '<div class="scenario-intro"><div class="scenario-index">01</div><div>'
            '<div class="scenario-title">读图挑战｜这段行情接下来会怎样？</div>'
            '<div class="scenario-subtitle">观察真实历史 K 线、成交量、MA5（5日移动均线）／MA20（20日移动均线）与 MACD（指数平滑异同移动平均线；12、26、9）。先独立判断，再揭晓后续 20 个交易日；提交前不会标出关键信号。</div>'
            '</div></div>', unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="callout scenario-color-key">'
            '<b>图表颜色：</b>'
            '<span class="color-pill color-up">绿色＝上涨</span> '
            '<span class="color-pill color-down">红色＝下跌</span>　'
            '<span class="color-key-line" style="color:#ffbf47">橙黄色线＝MA5（5日移动均线）</span>　'
            '<span class="color-key-line" style="color:#55b8ff">蓝色线＝MA20（20日移动均线）</span><br>'
            '<span class="scenario-color-note">成交量沿用当日涨跌颜色；MACD 柱的绿／红分别表示柱体正值／负值，不要把它直接当作股价涨跌。</span>'
            '</div>', unsafe_allow_html=True,
        )
        try:
            signal_case = load_dual_golden_cross_case()
        except Exception:
            signal_case = None

        if signal_case is None:
            st.warning("暂时无法从截至 2026-10-06 的真实历史行情中找到可完整揭晓的案例。请检查网络后刷新；本题不会用虚构行情代替真实数据。")
        else:
            full_data = signal_case["data"].copy().sort_values("date").reset_index(drop=True)
            anchor_idx = int(signal_case["anchor_idx"])
            history_start = max(0, anchor_idx - 25)
            future_end_idx = min(anchor_idx + 20, len(full_data) - 1)
            case_data = full_data.iloc[history_start:future_end_idx + 1].copy().reset_index(drop=True)
            case_data["is_future"] = case_data.index >= (anchor_idx - history_start + 1)
            signal_date = pd.Timestamp(full_data.iloc[anchor_idx]["date"])
            ma_cross_date = pd.Timestamp(full_data.iloc[int(signal_case["ma_cross_idx"])]["date"])
            macd_cross_date = pd.Timestamp(full_data.iloc[int(signal_case["macd_cross_idx"])]["date"])
            future_data = full_data.iloc[anchor_idx + 1:future_end_idx + 1].copy()
            if future_data.empty:
                st.warning("这个历史样本缺少完整的后续 20 个交易日，请刷新并重新选择样本。")
            else:
                start_close = float(full_data.iloc[anchor_idx]["close"])
                end_close = float(future_data.iloc[-1]["close"])
                outcome_pct = (end_close / start_close - 1.0) * 100.0
                # Treat very small changes as "unchanged" so the three choices are meaningful.
                neutral_band_pct = 1.0
                actual_class = 0 if outcome_pct > neutral_band_pct else (1 if outcome_pct < -neutral_band_pct else 2)
                answer_options = ["会上涨", "会下跌", "不变"]
                if st.session_state.get("home_scenario_01_result") not in answer_options:
                    st.session_state.pop("home_scenario_01_result", None)
                if st.session_state.get("home_scenario_01_answer") not in answer_options:
                    st.session_state.pop("home_scenario_01_answer", None)
                result_01 = st.session_state.get("home_scenario_01_result")
                fig = dual_signal_figure(
                    case_data, pd.Timestamp(future_data.iloc[-1]["date"]),
                    reveal_future=result_01 is not None,
                    ma_cross_date=ma_cross_date, macd_cross_date=macd_cross_date, height=710,
                )
                if result_01 is None:
                    chart_col, answer_col = st.columns([1.52, 1], gap="large", vertical_alignment="top")
                    with chart_col:
                        st.plotly_chart(fig, width="stretch", key="home_scenario_01_continuous_chart", config={"displaylogo": False})
                        st.caption(
                            f"真实历史样本：{signal_case['ticker']}（{TICKERS.get(signal_case['ticker'], signal_case['ticker'])}）｜"
                            f"数据截止日期为 2026-10-06。提交后，后续 20 个交易日会直接接在当前走势右侧。数据来源：Yahoo Finance 调整后日线。"
                        )
                    with answer_col:
                        with st.container(border=True):
                            st.markdown("### 你的判断")
                            st.markdown(
                                f"请观察左侧截至 **{signal_date:%Y-%m-%d}** 的走势。不要只看某一条线："
                                "同时考虑价格相对均线的位置、成交量是否配合，以及 MACD 两条线和柱体的变化。"
                            )
                            st.markdown("**问题：** 从信号日收盘开始，未来 20 个交易日后，收盘价相对现在会怎样变化？")
                            st.caption("判定口径：累计涨幅超过 +1% 视为上涨；跌幅超过 1% 视为下跌；−1% 至 +1% 之间视为不变。")
                            with st.form("home_scenario_01_form"):
                                scenario_01_answer = st.radio(
                                    "选择最合理的判断：", answer_options, index=None,
                                    key="home_scenario_01_answer",
                                )
                                scenario_01_submit = st.form_submit_button("揭晓后续走势", width="stretch")
                            if scenario_01_submit:
                                if scenario_01_answer is None:
                                    st.warning("请先选择一个判断，再揭晓后续走势。")
                                else:
                                    st.session_state["home_scenario_01_result"] = scenario_01_answer
                                    st.rerun()
                else:
                    # After submission, the question/choices disappear and the same chart expands to full width.
                    st.plotly_chart(fig, width="stretch", key="home_scenario_01_continuous_chart", config={"displaylogo": False})
                    chosen_class = answer_options.index(result_01) if result_01 in answer_options else -1
                    if chosen_class == actual_class:
                        st.success(escape_markdown_dollars(f"判断命中历史结果：信号日收盘价 ${start_close:.2f} → 第 20 个交易日收盘价 ${end_close:.2f}，累计 {outcome_pct:+.2f}%。"))
                    else:
                        st.error(escape_markdown_dollars(f"这次没有命中历史结果。真实变化为 {outcome_pct:+.2f}%；信号日收盘价 ${start_close:.2f}，第 20 个交易日收盘价 ${end_close:.2f}。"))
                    gap = int(signal_case["gap"])
                    gap_description = "同一交易日出现" if gap == 0 else f"相隔 {gap} 个交易日先后出现"
                    st.markdown(
                        f"**为什么这些位置值得注意？** MA5（5日移动均线）在 **{ma_cross_date:%Y-%m-%d}** 上穿 MA20（20日移动均线），"
                        f"DIF（差离值／快线）在 **{macd_cross_date:%Y-%m-%d}** 上穿 DEA（信号线；两者{gap_description}）。"
                        "图中用橙黄色三角形与垂直虚线标出均线交叉位置，并用紫色菱形与另一条虚线标出 MACD 交叉位置。"
                        "短期均线上穿长期均线，代表近期平均价格相对走强；DIF（差离值／快线）上穿 DEA（信号线），代表 MACD 动能线相对信号线转强。"
                        "这两类信号接近同时出现，可作为观察价格动能的线索，但它们都基于历史价格，可能滞后并产生假信号，不能保证后市上涨。"
                    )
                    st.caption(
                        f"样本：{signal_case['ticker']}｜观察日期：{signal_date:%Y-%m-%d}｜揭晓区间结束：{pd.Timestamp(future_data.iloc[-1]['date']):%Y-%m-%d}。"
                        "图表使用真实 Yahoo Finance 调整后日线；绿涨红跌适用于 K 线与成交量。MACD 柱的颜色表示柱体正负值。"
                    )
                    if st.button("重新挑战 01", key="home_scenario_01_reset"):
                        st.session_state.pop("home_scenario_01_result", None)
                        st.session_state.pop("home_scenario_01_answer", None)
                        st.rerun()

                st.markdown(
                    '<div class="scenario-source">行情数据来源及使用口径请见「数据与方法」。'
                    '样本数据截止日期为 2026-10-06；本练习用于观察历史走势，不是投资建议，也不代表指标可以可靠预测未来。</div>',
                    unsafe_allow_html=True,
                )

    st.write("")
    section_heading("YOUR LEARNING PATH", f"从零开始的 {len(LESSON_GUIDE)} 个学习单元", "每课包含关键概念、示例、互动探索或练习；可以按顺序学习，也可以按需复习。")
    cards_data = [
        ("01", "📘", "股票市场基础", "了解股票、债券、指数、ETF、交易所与市值。", "基础概念", "01 股票市场基础"),
        ("02", "📊", "看懂行情", "理解 K 线、成交量、报价和不同时间周期。", "互动图表", "02 看懂行情"),
        ("02A", "🕯️", "蜡烛图形态学", "从单根、双根到多根组合，结合趋势背景和确认信号学习常见形态。", "形态专题", "02A 蜡烛图形态学"),
        ("02B", "📈", "技术指标入门", "把均线、动能、波动与成交量指标放回 K 线走势中理解。", "第二课扩展", "02B 技术指标入门"),
        ("03", "🧾", "交易如何执行", "认识券商、订单类型、买卖价差、费用与成交。", "交易流程", "03 交易如何执行"),
        ("04", "🔎", "研究一家公司", "学习财务报表、关键指标与可靠资料来源。", "公司研究", "04 研究一家公司"),
        ("05", "🧩", "股价为什么变化", "从公司业绩、利率、预期与市场因素理解价格。", "案例学习", "05 股价为什么变化"),
        ("06", "🛡️", "风险与投资者保护", "识别骗局、过度自信、杠杆风险与信息陷阱。", "安全与纪律", "06 风险与投资者保护"),
    ]
    for row_start in range(0, len(cards_data), 2):
        row_cards = st.columns(2)
        for col, d in zip(row_cards, cards_data[row_start:row_start + 2]):
            with col:
                status = "✓ 已完成" if d[5].split(" ", 1)[-1] in completed else d[4]
                st.markdown(
                    f'<div class="lesson-card"><div class="lesson-top"><div class="lesson-icon">{d[1]}</div><div class="lesson-no">LESSON {d[0]}</div></div><div class="lesson-title">{d[2]}</div><div class="lesson-text">{d[3]}</div><span class="tag">{status}</span></div>',
                    unsafe_allow_html=True,
                )
                st.button("进入课程 →", key=f"home_{d[0]}", width="stretch", on_click=nav_to, args=(d[5],))

    st.write("")
    section_heading("TOOLS FOR LEARNING", "课程测验与数据工具", "完成课程后可用综合测验复习全部重点，也可以下载整理后的历史行情数据。")
    quick_a, quick_b = st.columns(2)
    with quick_a:
        info_card("✓", "综合测验", "用混合题检查你对股票基础、图表、公司研究、收益与风险的理解。")
        st.button("开始综合测验 →", key="home_open_comprehensive_quiz", width="stretch", on_click=nav_to, args=("综合测验",))
    with quick_b:
        info_card("↗", "数据与方法", "查看行情数据来源、口径和使用限制，并导出用于学习的数据集。")
        st.button("打开数据与方法 →", key="home_open_data_methods", width="stretch", on_click=nav_to, args=("数据与方法",))

    st.write("")
    section_heading("START HERE", "第一次学习，先记住这三件事")
    c1, c2, c3 = st.columns(3)
    with c1:
        info_card("🧩", "价格不等于价值", "每股价格只说明一股的市场报价。判断公司不能只比较股价高低。")
    with c2:
        info_card("📉", "收益和风险要一起看", "历史涨幅高不代表未来必然上涨。要同时观察波动、回撤和时间范围。")
    with c3:
        info_card("🔎", "数据需要背景", "图表可以告诉我们发生了什么，但单靠一条曲线通常无法证明为什么发生。")
    st.markdown('<div class="callout">学习目标：学会提出更好的问题，而不是背下一个“必涨信号”。</div>', unsafe_allow_html=True)



# ============================================================
# Lesson 1: Stock basics
# ============================================================
elif chosen_page == "01 股票市场基础":
    hero(
        "第一课｜认识股票市场",
        "从一股股票背后的所有权，走到市场如何发行、交易和定价；建立投资工具、市场参与者、回报与风险的基础框架。",
        "LESSON 01 · THE BASICS",
    )

    section_heading(
        "THE BIG PICTURE",
        "先建立一张市场地图",
        "股票入门课程通常先解释所有权与融资，再介绍交易市场和投资工具，最后讨论回报、风险与投资前准备。本课沿着这条学习路径展开。",
    )
    overview_cols = st.columns(3)
    with overview_cols[0]:
        info_card("🏢", "公司与股份", "公司把所有权划分为股份。买入股票，意味着持有公司股权的一部分，而不是把钱借给公司。", "所有权")
    with overview_cols[1]:
        info_card("🔄", "发行与交易", "公司发行证券可以募集资金；投资者在二级市场交易已发行股票，交易价格由买卖订单与市场预期共同形成。", "市场机制")
    with overview_cols[2]:
        info_card("⚖️", "回报与风险", "收益可能来自价格上涨和股息，风险则包括价格下跌、公司经营恶化、流动性不足与持仓过度集中。", "投资判断")

    lesson_tabs = st.tabs([
        "01 股票代表什么",
        "02 市场如何运作",
        "03 常见投资工具",
        "04 价格与回报",
        "05 风险与起步",
    ])

    with lesson_tabs[0]:
        section_heading("OWNERSHIP", "股票是公司所有权的一部分", "这不是债权承诺，也不是固定收益产品。")
        st.markdown(
            """
            持有股票意味着拥有公司的一部分股权。普通股股东通常可能享有投票权，并可能获得公司分配的股息；具体权利取决于股份类别、公司章程及适用法律。公司不一定派息，股价也不保证上涨。

            股票的回报和风险与公司的经营表现、财务状况、竞争环境、未来预期以及整个市场的变化有关。若公司进入破产清算，普通股股东通常在债权人等优先权利人之后分配剩余资产，最终可能没有剩余价值。
            """
        )
        with st.container(border=True):
            section_heading("TRY THE NUMBERS", "用一个假设公司理解市值", "调整股价和股份数量，观察“每股价格”与“公司整体股权估值”为什么不同。")
            calc_a, calc_b, calc_c = st.columns(3)
            with calc_a:
                market_price = st.slider(
                    "假设每股价格（美元）", min_value=5, max_value=200, value=20, step=5,
                    key="lesson1_market_price",
                )
            with calc_b:
                shares_outstanding_m = st.slider(
                    "已发行在外股份（百万股）", min_value=1, max_value=1000, value=100, step=1,
                    key="lesson1_shares_outstanding_m",
                )
            with calc_c:
                held_shares = st.number_input(
                    "假设持有股数", min_value=1, max_value=100000, value=100, step=100,
                    key="lesson1_held_shares",
                )
            outstanding_shares = int(shares_outstanding_m) * 1_000_000
            market_cap = float(market_price) * outstanding_shares
            holding_value = float(market_price) * int(held_shares)
            ownership_pct = int(held_shares) / outstanding_shares * 100
            result_a, result_b, result_c = st.columns(3)
            with result_a:
                st.markdown(escape_markdown_dollars(f"**假设股权市值**\n\n## ${market_cap:,.0f}"))
                st.caption("每股价格 × 已发行在外股份数")
            with result_b:
                st.markdown(escape_markdown_dollars(f"**这笔持仓的市值**\n\n## ${holding_value:,.2f}"))
                st.caption("当前假设价格 × 持有股数")
            with result_c:
                st.markdown(f"**持股比例**\n\n## {ownership_pct:.6f}%")
                st.caption("持有股数 ÷ 已发行在外股份数")
            st.caption("这是教学用的简化计算。真实市值应核对股份口径；市值代表市场给股权的估值，不等于公司账面资产、现金或企业价值。")

        with st.expander("再区分两个容易混淆的概念：股价与价值"):
            st.markdown(
                """
                - **股价**是特定时点或最近一笔成交中，每股股票的交易价格。
                - **市值**通常以每股价格乘以已发行在外股份数估算。
                - **价值判断**还需要研究公司可能创造的未来现金流、增长、竞争优势、财务状况和风险；市值本身并不直接告诉你股票是否便宜。
                """
            )

    with lesson_tabs[1]:
        section_heading("MARKET STRUCTURE", "股票从发行到成交，会经过哪些环节？", "把发行人、投资者、券商、交易场所和监管体系分开理解。")
        st.markdown(
            """
            **一级市场：发行证券以募集资金。** 例如首次公开募股（IPO）或后续发行，公司通过发行新股等方式获得资金。IPO 的具体安排会因市场、发行结构和交易规则而不同。

            **二级市场：投资者交易已发行的证券。** 投资者经常通过券商买卖股票。多数普通二级市场交易的资金在买卖双方之间转移，公司不会因为每一次股票转手而直接收到交易款；但公司后续融资、回购等公司行动另当别论。
            """
        )
        participants = st.columns(3)
        with participants[0]:
            info_card("🏭", "发行人", "公司通过证券发行筹集资金，并按适用规则披露重要经营与财务信息。")
        with participants[1]:
            info_card("👥", "投资者", "个人、基金、养老金及其他机构根据各自目标、限制和判断提交买卖需求。")
        with participants[2]:
            info_card("🔗", "券商与交易场所", "券商接收并转送客户订单；交易所或其他交易场所提供订单匹配与交易机制。")
        with st.expander("一笔普通股票交易的大致路径"):
            st.markdown(
                """
                **投资者决定买卖 → 向券商提交订单 → 券商按适用规则路由订单 → 交易场所或流动性提供者完成撮合/成交 → 清算与结算完成证券和资金交收。**

                具体路由和成交方式取决于券商、市场结构、订单类型和证券流动性。点击买入并不代表一定能以屏幕上的最近成交价成交；订单类型、市场波动和价差都会影响实际结果。
                """
            )
        with st.expander("公开上市公司为什么需要披露信息？"):
            st.markdown(
                """
                公开市场投资者需要依靠可验证的信息评估公司。美国上市公司常见披露包括年度报告（10-K）、季度报告（10-Q）和重大事项报告（8-K）；其他市场有各自的披露规则与文件制度。阅读财报、公告和风险因素，是从市场故事走向公司研究的重要一步。
                """
            )

    with lesson_tabs[2]:
        section_heading("INVESTMENT VEHICLES", "股票、债券、指数和 ETF 不是同一种东西", "先弄清你买到的是什么，再讨论它的价格与风险。")
        tool_table = pd.DataFrame([
            {"工具": "股票", "买到的是什么": "公司股权的一部分", "可能回报": "股价变化、可能的股息", "需要认识的风险": "公司经营、估值与市场价格下跌"},
            {"工具": "债券", "买到的是什么": "通常是对发行人的债权", "可能回报": "利息与到期偿付，取决于债券条款和发行人的偿付能力", "需要认识的风险": "信用、利率、通胀与流动性风险"},
            {"工具": "股票指数", "买到的是什么": "按一套规则衡量一组证券的指标", "可能回报": "指数本身是衡量指标，通常不能直接像股票一样买卖", "需要认识的风险": "成分、权重、计算和调整规则会影响代表性"},
            {"工具": "ETF", "买到的是什么": "在交易所交易的基金份额", "可能回报": "取决于基金持有的资产、费用和市场价格", "需要认识的风险": "市场风险、费用、跟踪误差与流动性"},
            {"工具": "共同基金", "买到的是什么": "由基金集合资金，按其投资目标持有资产", "可能回报": "取决于基金资产、策略和费用", "需要认识的风险": "市场、策略、管理费用与赎回规则"},
        ])
        st.dataframe(tool_table, width="stretch", hide_index=True)
        st.markdown(
            """
            **一个关键区别：指数不等于指数基金。** 指数是一种衡量市场或一篮子证券表现的方法；指数基金（可能采用 ETF 或共同基金结构）则是尝试跟踪该指数的投资产品。持有更广泛的一篮子证券可以降低单一公司的集中风险，但无法消除整体市场下跌风险。
            """
        )
        with st.expander("普通股、优先股与不同投资风格"):
            st.markdown(
                """
                - **普通股与优先股：** 两者在投票权、股息安排、清偿顺序等方面可能不同，应查看具体条款。
                - **成长风格与价值风格：** 成长投资更关注未来增长预期；价值投资常比较市场价格与对公司价值的估计。这些风格标签并不保证回报。
                - **大盘、中盘和小盘：** 通常按市值规模分类，具体分界因市场和指数规则而异。
                - **牛市与熊市：** 用来描述较广泛的市场趋势，不能仅凭某一天涨跌就下结论。
                """
            )

    with lesson_tabs[3]:
        section_heading("PRICE & RETURN", "价格是交易结果，回报来自不止一个部分", "市场价格反映买卖双方在某一时点的交易与预期；它不是公司内在价值的直接读数。")
        st.markdown(
            """
            - **买价（Bid）：** 买方愿意支付的报价；市场中常关注当前最高买价。
            - **卖价（Ask）：** 卖方愿意接受的报价；市场中常关注当前最低卖价。
            - **买卖价差（Bid–Ask Spread）：** 卖价与买价的差额，是交易成本的重要组成部分之一。
            - **最近成交价（Last Price）：** 已经发生的成交价格，不保证你下一笔订单仍能以这个价格成交。

            市场价格会随订单供求、公司信息、行业变化、利率、宏观经济、市场情绪和流动性等因素变化。即使公司经营表现不错，若市场此前预期更高，股价也可能下跌；反之亦然。
            """
        )
        with st.container(border=True):
            section_heading("TRY A RETURN EXAMPLE", "互动计算：价格变化与股息一起看", "假设以每股 20 美元买入；修改当前价格和期间每股股息，看看简单总回报如何变化。")
            return_a, return_b, return_c = st.columns(3)
            with return_a:
                purchase_price = 20.0
                st.markdown(escape_markdown_dollars("**假设买入价格**\n\n## $20.00"))
                st.caption("每股买入成本，不含费用")
            with return_b:
                ending_price = st.slider(
                    "假设当前股价（美元）", min_value=5, max_value=35, value=22, step=1,
                    key="lesson1_ending_price",
                )
            with return_c:
                dividend_per_share = st.slider(
                    "期间每股股息（美元）", min_value=0.0, max_value=2.0, value=0.5, step=0.25,
                    key="lesson1_dividend_per_share",
                )
            return_shares = st.number_input(
                "假设持有股数", min_value=1, max_value=10000, value=100, step=10,
                key="lesson1_return_shares",
            )
            price_change_per_share = float(ending_price) - purchase_price
            total_return_cash = (price_change_per_share + float(dividend_per_share)) * int(return_shares)
            starting_value = purchase_price * int(return_shares)
            simple_total_return = total_return_cash / starting_value * 100
            st.markdown(escape_markdown_dollars(
                f"**价格变化：** ${price_change_per_share:,.2f}/股　　"
                f"**假设股息：** ${float(dividend_per_share):,.2f}/股　　"
                f"**总回报（税费前）：** ${total_return_cash:,.2f}（{simple_total_return:+.2f}%）"
            ))
            st.caption("示例假设股息已收到，且不考虑税费、交易费用、股息再投资和持有期限差异。若价格下跌，股息也可能不足以弥补价格损失。")
        with st.expander("股票买卖订单的基础概念"):
            st.markdown(
                """
                **市价单**优先寻求尽快成交，但成交价格不保证；**限价单**指定可接受的价格或更优价格，但可能无法成交。止损单触及触发价后，通常会转换成市价单，触发价不等于保证成交价。不同市场和券商对订单的具体支持与处理方式可能不同，下一课会进一步讲解执行过程。
                """
            )

    with lesson_tabs[4]:
        section_heading("RISK & READINESS", "入门投资先管理边界，再选择工具", "风险不只是股价波动，也包括资金何时需要使用、成本、流动性和决策方式。")
        readiness = st.columns(2)
        with readiness[0]:
            info_card("🎯", "目标与期限", "写清楚资金的用途和使用时间。短期必须支出的资金，不适合承担大幅波动。")
            info_card("🧯", "现金与负债", "先检查应急储备、日常支出和高利息债务，不要把必要开支押在高波动资产上。")
            info_card("📚", "理解产品", "说清楚自己买的是什么、如何产生回报、最坏情况下会发生什么。")
        with readiness[1]:
            info_card("🧺", "分散与集中", "分散到不同公司、行业和资产类别可以降低部分集中风险，但不能保证盈利或阻止市场整体下跌。")
            info_card("💸", "费用与流动性", "比较佣金、价差、基金费用、税项和换汇成本；低成交量证券可能难以在理想价格卖出。")
            info_card("🔎", "核实来源", "查看公司公告、财务披露、基金文件和中介机构资质；对保证高回报、催促转账或秘密消息保持警惕。")
        with st.expander("初学者容易犯的 5 个错误"):
            st.markdown(
                """
                1. **只比较每股价格：** 忽略股份数量、市值、盈利、增长与风险。
                2. **把过去上涨当成未来保证：** 历史表现不保证未来回报。
                3. **把股息当成免费收益：** 总回报要同时看价格变化、分配和成本。
                4. **把 ETF 当成无风险：** ETF 仍会受其持有资产、集中度、费用和跟踪误差影响。
                5. **忽略目标和时间：** 投资选择要与资金用途、期限和实际承受损失的能力相符。
                """
            )

    section_heading("KEY TERMS", "本课词汇速查")
    glossary = pd.DataFrame([
        {"术语": "股票 / Share", "入门解释": "代表公司股权的一部分。"},
        {"术语": "IPO / 首次公开募股", "入门解释": "公司首次向公众发行股票的过程之一，具体发行结构因市场而异。"},
        {"术语": "二级市场", "入门解释": "投资者交易已发行证券的市场；普通二级市场转手通常不直接给发行公司带来资金。"},
        {"术语": "市值 / Market Cap", "入门解释": "股价乘以已发行在外股份数的常见估算。"},
        {"术语": "指数 / Index", "入门解释": "按照规则衡量一组证券表现的指标。"},
        {"术语": "流动性 / Liquidity", "入门解释": "能否较快交易而不承受很大价格让步。"},
        {"术语": "分散 / Diversification", "入门解释": "分布风险来源，降低单一资产或单一行业的集中风险，但不保证不亏损。"},
    ])
    st.dataframe(glossary, width="stretch", hide_index=True)

    st.write("")
    section_heading("QUICK CHECK", "理解一下，再继续")
    answer = st.radio(
        "如果 A 公司每股 20 美元，B 公司每股 200 美元，我们能直接判断哪家公司更贵吗？",
        ["可以，B 公司股价更高，所以更贵", "不能，还需要看股数、市值、盈利和其他信息", "可以，股价越高，投资风险一定越高"],
        key="basics_quiz",
    )
    if st.button("提交答案", key="basics_submit"):
        if answer.startswith("不能"):
            record_quiz_attempt("股票市场基础", True)
            st.success("答对了！每股价格只是一个单位价格；比较估值还需要看股份数量、市值、盈利、增长预期和风险。可以继续学习下一部分内容。")
        else:
            record_quiz_attempt("股票市场基础", False)
            st.error("再想一想：不同公司的股份数量可能完全不同。单看每股价格不足以比较公司整体市值，也不能直接判断估值高低。请阅读解析后重新作答。")
    lesson_completion_button("股票市场基础", "finish_basics")


# ============================================================
# Lesson 2: Read charts
# ============================================================
elif chosen_page == "02 看懂行情":
    hero("第二课｜读懂股票行情", "不要只盯着红绿价格。试着读懂一根 K 线背后的开盘价、最高价、最低价、收盘价与成交量。", "LESSON 02 · READ THE CHART")
    left, right = st.columns([1.05, 2.0])
    with left:
        symbol = st.selectbox("选择一只股票", list(TICKERS.keys()), index=list(TICKERS.keys()).index("NVDA"), format_func=ticker_label, key="chart_ticker")
        # Migrate a previously selected period that is no longer offered in this chart.
        if st.session_state.get("chart_period") == "5y":
            st.session_state["chart_period"] = "3mo"
        lesson_period = st.selectbox("查看历史范围", ["1mo", "3mo", "6mo", "1y"], index=1, format_func=lambda x: PERIODS[x], key="chart_period")
        st.markdown('<div class="callout">建议先选 3 个月的范围，移动鼠标悬停在 K 线上，逐一观察 OHLC 数据。</div>', unsafe_allow_html=True)
        st.markdown("#### K 线五个要素")
        st.markdown("**开盘价 Open**：该时间段开始时的价格。\n\n**最高价 High**：该时间段内到达的最高价格。\n\n**最低价 Low**：该时间段内到达的最低价格。\n\n**收盘价 Close**：该时间段结束时的价格。\n\n**成交量 Volume**：该时间段内报告的交易股数。")
    chart_data, chart_error = safe_prices([symbol], lesson_period)
    show_data_warning(chart_error)
    with right:
        if not chart_data.empty:
            one = chart_data[chart_data["ticker"] == symbol].sort_values("date").copy()
            latest = one.iloc[-1]
            previous = one.iloc[-2]["close"] if len(one) > 1 else np.nan
            daily_change = (latest["close"] / previous - 1) * 100 if pd.notna(previous) and previous else np.nan
            k1, k2, k3 = st.columns(3)
            k1.metric("最新可用收盘价", format_money(latest["close"]))
            k2.metric("较前一交易日", format_pct(daily_change))
            k3.metric("最新日成交量", f"{latest['volume']:,.0f}" if pd.notna(latest["volume"]) else "—")

            st.markdown(f"#### {symbol} · 日 K 线")
            candle = go.Figure(data=[go.Candlestick(
                x=one["date"], open=one["open"], high=one["high"], low=one["low"], close=one["close"], name=symbol,
                increasing_line_color="#60e2bd", decreasing_line_color="#ff8f9b",
                increasing_fillcolor="#60e2bd", decreasing_fillcolor="#ff8f9b",
            )])
            candle.update_layout(title=None, xaxis_title="日期", yaxis_title="价格（美元）", xaxis_rangeslider_visible=False, hovermode="x unified")
            style_fig(candle, 440)
            candle.update_layout(margin=dict(l=32, r=18, t=24, b=36))
            st.plotly_chart(candle, width="stretch", key="lesson_candle")

    if not chart_data.empty:
        section_heading("LOOK CLOSER", "价格与成交量要一起看")
        # Keep a visual gap between the section heading and the standalone chart caption.
        st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)
        one = chart_data[chart_data["ticker"] == symbol].sort_values("date").copy()
        one["成交量颜色"] = np.where(one["close"] >= one["open"], "收盘不低于开盘", "收盘低于开盘")
        st.markdown("#### 每日成交量")
        st.caption("柱子越高，表示该交易日报告的成交股数越多。绿色表示收盘价不低于开盘价，红色表示收盘价低于开盘价。")
        vol = px.bar(
            one, x="date", y="volume", color="成交量颜色",
            color_discrete_map={"收盘不低于开盘": "#60e2bd", "收盘低于开盘": "#ff8f9b"},
        )
        vol.update_layout(
            xaxis_title="日期", yaxis_title="成交量（股）", showlegend=False,
        )
        style_fig(vol, 350)
        vol.update_layout(margin=dict(l=34, r=18, t=22, b=42))
        st.plotly_chart(vol, width="stretch")
        st.markdown("成交量表示交易活跃程度；价格方向还要看价格行为和市场背景。")
        with st.expander("查看最近 12 个交易日的 OHLCV 数据"):
            show = one.tail(12)[["date", "open", "high", "low", "close", "volume"]].rename(columns={"date": "日期", "open": "开盘价", "high": "最高价", "low": "最低价", "close": "收盘价", "volume": "成交量"})
            st.dataframe(show.sort_values("日期", ascending=False), width="stretch", hide_index=True)
            st.download_button("下载本次股票数据 CSV", show.to_csv(index=False).encode("utf-8-sig"), file_name=f"{symbol}_OHLCV.csv", mime="text/csv")

        section_heading("QUICK CHECK", "试着判断图表告诉了你什么")
        pick = st.radio("某一天成交量明显放大，最稳妥的解释是什么？", ["股价下一天必定上涨", "当天交易比平时活跃，方向还需结合其他信息判断", "说明公司盈利已经增加"], key="volume_quiz")
        if st.button("检查理解", key="volume_submit"):
            if pick.startswith("当天交易"):
                record_quiz_attempt("看懂行情", True)
                st.success("答对了。成交量描述交易活动，不是预测未来价格的独立信号。继续写下你从图表中观察到的一点。")
            else:
                record_quiz_attempt("看懂行情", False)
                st.error("成交量不能保证未来方向，也不能直接说明公司盈利变化。阅读解析后可以重新尝试。")
        with st.expander("补充知识：时间周期、调整价格和图表误区"):
            st.markdown("""
            **时间周期**：一分钟 K 线聚焦很短的价格波动；日 K 线显示一个交易日内的 OHLC；周线或月线用于更长周期的观察。周期不同，看到的噪声和细节也不同。

            **原始收盘价与调整后价格**：历史数据可能因为拆股、股息等公司行动调整。调整价格适合某些历史比较，但必须查看数据源定义；不要把调整后的历史 OHLC 当作当时可直接成交的真实报价。

            **图表颜色**：不同市场或软件可能使用不同的涨跌颜色。要看图例或 OHLC 数值，不要只凭颜色判断。

            **图表能回答什么：** K 线与成交量描述过去的价格和交易活动；分析价格变化的原因，还需要事件、基本面和市场背景。
            """)

        lesson_completion_button("看懂行情", "finish_chart")


# ============================================================
# Lesson 2A: Candlestick patterns (single / multi-candle)
# ============================================================
elif chosen_page == "02A 蜡烛图形态学":
    st.markdown('<div id="candle-pattern-top"></div>', unsafe_allow_html=True)
    hero(
        "第二课扩展｜系统学习蜡烛图形态",
        "从单根 K 线到多根组合，学习它们的结构、常见背景和传统解读。图形是观察价格行为的语言，不是保证涨跌的信号。",
        "LESSON 02A · CANDLESTICK PATTERNS",
    )
    st.markdown('[↑ 回到本章顶部](#candle-pattern-top)', unsafe_allow_html=False)
    st.markdown("**形态解读：** 先看此前趋势、形态位置、成交量与后续价格行为，再判断传统形态是否适用。形态名称本身不是独立交易信号。")

    # The standalone candle anatomy/color explainer was removed at the user's request.

    group_names = list(dict.fromkeys(pattern["group"] for pattern in CANDLE_PATTERNS))
    selector_left, selector_right = st.columns([1, 1.5], gap="large")
    with selector_left:
        chosen_group = st.selectbox("第一步：选择形态类型", group_names, key="candle_pattern_group")
        candidates = [pattern for pattern in CANDLE_PATTERNS if pattern["group"] == chosen_group]
        available_pattern_names = [pattern["name"] for pattern in candidates]
        # When the category changes, reset an old pattern name that is no longer
        # available before Streamlit instantiates the dependent selectbox.
        if st.session_state.get("candle_pattern_name") not in available_pattern_names:
            st.session_state["candle_pattern_name"] = available_pattern_names[0]
        chosen_pattern_name = st.selectbox("第二步：选择具体形态", available_pattern_names, key="candle_pattern_name")
        # Selecting another candle pattern intentionally does NOT scroll the page.
        # Users often compare patterns while reading farther down this lesson; keep
        # their current reading position. Auto-scroll is reserved for main navigation.
        chosen_pattern = next(pattern for pattern in candidates if pattern["name"] == chosen_pattern_name)
        st.markdown(
            f'<div class="lesson-card"><div class="lesson-top"><div class="lesson-icon">🕯️</div><div class="lesson-no">{len(chosen_pattern["bars"])} 根 K 线</div></div>'
            f'<div class="lesson-title">{escape(chosen_pattern["name"])}</div>'
            f'<div class="lesson-text">{escape(chosen_pattern["structure"])}</div>'
            f'<div style="margin-top:.8rem"><span class="tag">传统解读：{escape(chosen_pattern["bias"])}</span></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("#### 识别要点")
        st.markdown(chosen_pattern["recognize"])
        st.markdown("#### 常见解读")
        st.markdown(chosen_pattern["meaning"])
    with selector_right:
        st.markdown("#### K 线结构示意")
        pattern_fig = build_candle_pattern_figure(chosen_pattern)
        style_fig(pattern_fig, 490)
        # The selected pattern name is already shown in the information card.
        # Keep the chart itself title-free so long names never collide with the plot.
        pattern_fig.update_layout(
            title=None,
            height=490,
            margin=dict(l=30, r=28, t=28, b=112),
            legend=dict(orientation="h", yanchor="top", y=-0.24, xanchor="left", x=0),
        )
        st.plotly_chart(pattern_fig, width="stretch", key="candle_pattern_diagram")
        st.caption("示意图使用合成 OHLC 数值绘制，只用于教学结构，不是真实证券的历史行情。绿色表示收盘高于开盘，红色表示收盘低于开盘。")

    context_cols = st.columns(2, gap="large")
    with context_cols[0]:
        info_card("📍", "出现背景", chosen_pattern["context"], "结合此前走势")
    with context_cols[1]:
        info_card("🔎", "后续确认", chosen_pattern["confirmation"], "不是自动买卖点")

    with st.expander("形态速查表：浏览本章涵盖的常见形态", expanded=False):
        pattern_table = pd.DataFrame([
            {
                "类型": p["group"],
                "形态": p["name"],
                "K线数量": len(p["bars"]),
                "传统解读": p["bias"],
                "关键背景": p["context"],
            }
            for p in CANDLE_PATTERNS
        ])
        filter_group = st.selectbox("按类型筛选", ["全部"] + group_names, key="candle_pattern_table_filter")
        if filter_group != "全部":
            pattern_table = pattern_table[pattern_table["类型"] == filter_group]
        st.dataframe(pattern_table, width="stretch", hide_index=True)

    st.write("")
    section_heading("STEP 2 · REAL MARKET", "在真实历史行情中练习观察", "示意图帮助你理解结构；真实图表用来练习观察。请先说明此前趋势，再判断形态是否清晰，不要把模糊形状硬套成某个名称。")
    real_left, real_right = st.columns([1, 2], gap="large")
    with real_left:
        real_symbol = st.selectbox("真实股票 / ETF", list(TICKERS.keys()), index=list(TICKERS.keys()).index("NVDA"), format_func=ticker_label, key="candle_real_symbol")
        real_period = st.selectbox("历史范围", ["5d", "1mo", "3mo", "6mo", "1y"], index=2, format_func=lambda x: PERIODS[x], key="candle_real_period")
        st.markdown('<div class="callout">练习顺序：①看此前走势；②看实体与影线比例；③看形态发生的位置；④再看下一根或后续几根 K 线是否确认。</div>', unsafe_allow_html=True)
    real_data, real_error = safe_prices([real_symbol], real_period)
    show_data_warning(real_error)
    with real_right:
        # load_prices already respects the selected period; don't truncate a one-year view to 90 candles.
        real_one = real_data[real_data["ticker"] == real_symbol].sort_values("date").copy() if not real_data.empty else pd.DataFrame()
        if not real_one.empty:
            st.markdown(f"#### {real_symbol} · 真实历史日 K 线（{PERIODS[real_period]}）")
            real_fig = go.Figure(data=[go.Candlestick(
                x=real_one["date"], open=real_one["open"], high=real_one["high"], low=real_one["low"], close=real_one["close"], name=real_symbol,
                increasing_line_color="#60e2bd", decreasing_line_color="#ff8f9b",
                increasing_fillcolor="#60e2bd", decreasing_fillcolor="#ff8f9b",
            )])
            real_fig.update_layout(title=None, xaxis_title="日期", yaxis_title="调整后价格（美元）", xaxis_rangeslider_visible=False, hovermode="x unified")
            style_fig(real_fig, 430)
            real_fig.update_layout(margin=dict(l=30, r=18, t=24, b=36))
            st.plotly_chart(real_fig, width="stretch", key="candle_patterns_real_chart")
        else:
            st.info("暂时没有可显示的历史数据。可以先学习上方的合成示意图，稍后再重试。")

    st.markdown("**蜡烛图形态的用途：** 描述价格结构并提出观察假设。研究结果因市场、样本、形态定义与交易成本而异；判断形态效果需要用历史数据检验。")
    section_heading("STEP 3 · PRACTICE", "形态识别与理解测验", "先回答问题，再查看每题解析。至少答对 5 题后，系统会记录你通过了本章检查；答错可以重做。")
    pattern_questions = [
        ("锤头线与上吊线的形状通常相似，主要根据什么区分？", ["蜡烛颜色", "形态出现前的趋势背景", "股票每股价格"], 1, "两者形状相近，锤头线通常讨论下跌后的潜在反转，上吊线通常讨论上涨后的潜在转弱。背景比颜色更重要。"),
        ("十字星最稳妥的基础解读是什么？", ["价格必然反转", "开盘与收盘接近，显示该周期内多空暂时僵持", "代表成交量最大"], 1, "十字星主要描述开盘与收盘接近。它本身不决定方向，需要结合此前趋势与后续价格。"),
        ("看涨吞没的典型结构是什么？", ["小阳线完全被前一根阴线实体覆盖", "后一根阳线实体覆盖前一根阴线实体", "连续三根收盘下跌的 K 线"], 1, "典型看涨吞没由前一根偏空实体与后一根较大的偏多实体构成；是否有意义仍取决于背景和确认。"),
        ("早晨之星的经典三根结构通常是？", ["长阴线、小实体、较强阳线", "长阳线、长阳线、长阳线", "十字星、十字星、十字星"], 0, "早晨之星常被视为下跌后潜在转强的三根组合：先有明显卖压，随后犹豫，第三根出现向上恢复。"),
        ("看到一根很长的上影线，最稳妥的结论是什么？", ["一定会下跌", "价格曾上探高位但未能维持；需结合趋势、位置与后续走势", "公司盈利一定下降"], 1, "上影线说明价格在该周期内曾经走得更高，收盘前回落；单凭它无法推断下一步一定下跌。"),
        ("为什么形态出现后还要关注后续确认？", ["因为形态名字决定不了未来，后续走势能提供额外证据", "为了让图表颜色更好看", "因为所有形态都会在两根 K 线内完成"], 0, "后续价格行为可以增强或削弱原先的解释，但仍不能保证结果。确认也可能使观察者错过部分行情。"),
        ("对蜡烛图形态最负责任的使用方式是什么？", ["看到看涨形态就立即买入", "把形态作为观察线索，结合趋势、关键价位、成交量、风险与其他证据", "只选历史上最漂亮的形态"], 1, "形态是描述价格行为的工具，不是单独的买卖指令。需要上下文、明确风险和独立核实。"),
    ]
    with st.form("candle_patterns_quiz_form"):
        quiz_answers = []
        for qi, (question, options, correct_idx, explanation) in enumerate(pattern_questions):
            quiz_answers.append(st.radio(f"{qi+1}. {question}", options, key=f"candle_pattern_quiz_{qi}", index=None))
        quiz_submit = st.form_submit_button("提交本章答案", width="stretch")
    if quiz_submit:
        score = sum(answer == question[1][question[2]] for answer, question in zip(quiz_answers, pattern_questions))
        all_answered = all(answer is not None for answer in quiz_answers)
        if not all_answered:
            st.warning("请先回答所有问题，再提交。")
        else:
            passed = score >= 5
            record_quiz_attempt("蜡烛图形态学", passed)
            st.session_state["candle_pattern_quiz_result"] = {"score": score, "passed": passed, "answers": quiz_answers}
    result = st.session_state.get("candle_pattern_quiz_result")
    if result:
        if result["passed"]:
            st.success(f"本次答对 {result['score']}/{len(pattern_questions)} 题，已通过形态识别检查。")
        else:
            st.warning(f"本次答对 {result['score']}/{len(pattern_questions)} 题。建议阅读解析后重做；系统会保留你曾经通过的记录。")
        for qi, (question, options, correct_idx, explanation) in enumerate(pattern_questions):
            chosen_answer = result["answers"][qi]
            with st.expander(f"{'✓' if chosen_answer == options[correct_idx] else '↻'} 第 {qi+1} 题解析"):
                st.markdown(f"**正确答案：** {options[correct_idx]}\n\n{explanation}")
    lesson_completion_button("蜡烛图形态学", "finish_candle_patterns")
    st.markdown('[↑ 回到本章顶部](#candle-pattern-top)', unsafe_allow_html=False)


# ============================================================
# Lesson 02B: Technical indicators
# ============================================================
elif chosen_page == "02B 技术指标入门":
    hero(
        "第二课扩展｜技术指标：从线条到判断",
        "先理解每个指标测量什么，再把它放回真实价格走势中。指标不是预测答案，而是帮助你有纪律地描述趋势、动能、波动与量价关系。",
        "LESSON 02B · TECHNICAL INDICATORS",
    )
    st.markdown(
        '<div class="callout"><b>先记住这条原则：</b>技术指标把已有价格或成交量数据整理成更容易观察的线条和读数。它们能帮助整理信息，但不能提前告诉我们未来。参数越敏感，反应可能越快，也可能产生更多假信号；多个指标若来自同一组价格数据，也不等于多份独立证据。</div>',
        unsafe_allow_html=True,
    )
    section_heading(
        "INTERACTIVE LAB", "指标实验室｜一次只学一个指标",
        "默认只显示 K 线。选择一种指标后，图表会显示对应线条或副图，教学内容紧接在图表下方；切换选择即可学习下一项。",
    )
    control_a, control_b, control_c = st.columns([1.05, 1.05, 1.7], gap="medium")
    with control_a:
        tech_symbol = st.selectbox(
            "选择股票 / ETF", list(TICKERS.keys()),
            index=list(TICKERS.keys()).index("NVDA"), format_func=ticker_label, key="tech_lab_symbol",
        )
    with control_b:
        # Migrate the old session value before the widget is created.
        if st.session_state.get("tech_lab_period") == "5y":
            st.session_state["tech_lab_period"] = "3mo"
        tech_period = st.selectbox(
            "历史范围", ["1mo", "3mo", "6mo", "1y"], index=1,
            format_func=lambda value: PERIODS[value], key="tech_lab_period",
        )
    with control_c:
        tech_indicator_choice = st.selectbox(
            "选择一个指标（同一时间只显示一种）",
            [
                "仅显示 K 线",
                "MA｜简单移动平均线（MA5 / MA20）",
                "EMA｜指数移动平均线（EMA12 / EMA26）",
                "布林带（20, 2）",
                "RSI（14）",
                "MACD（12, 26, 9）",
                "随机指标（Stochastic）",
                "ADX（趋势强度）",
                "OBV（能量潮）",
                "支撑位与阻力位",
                "斐波那契回撤",
                "VWAP（概念学习）",
                "一目均衡表（概念学习）",
            ],
            index=0,
            key="tech_lab_indicator_choice",
            help="每次只选择一种指标。MA、EMA、布林带、支撑阻力和斐波那契显示在价格主图；RSI、MACD、随机指标、ADX 和 OBV 显示为下方副图。",
        )

    # Enforce one indicator family at a time. This avoids stacked overlays hiding the candles.
    tech_overlays: list[str] = []
    tech_lower_indicator = "不显示副图"
    tech_show_levels = tech_indicator_choice == "支撑位与阻力位"
    tech_show_fibonacci = tech_indicator_choice == "斐波那契回撤"
    if tech_indicator_choice.startswith("MA｜"):
        tech_overlays = ["MA5 / MA20"]
    elif tech_indicator_choice.startswith("EMA｜"):
        tech_overlays = ["EMA12 / EMA26"]
    elif tech_indicator_choice == "布林带（20, 2）":
        tech_overlays = ["布林带（20, 2）"]
    elif tech_indicator_choice == "RSI（14）":
        tech_lower_indicator = "RSI"
    elif tech_indicator_choice == "MACD（12, 26, 9）":
        tech_lower_indicator = "MACD"
    elif tech_indicator_choice == "随机指标（Stochastic）":
        tech_lower_indicator = "随机指标（Stochastic）"
    elif tech_indicator_choice == "ADX（趋势强度）":
        tech_lower_indicator = "ADX（趋势强度）"
    elif tech_indicator_choice == "OBV（能量潮）":
        tech_lower_indicator = "OBV（能量潮）"

    # Calculate indicators on a longer history, then display only the requested range.
    tech_raw, tech_error = safe_prices([tech_symbol], "10y")
    show_data_warning(tech_error)
    tech_history = tech_raw.loc[tech_raw["ticker"] == tech_symbol].sort_values("date").copy() if not tech_raw.empty else pd.DataFrame()
    if not tech_history.empty:
        tech_history_frame = calculate_technical_indicators(tech_history)
        period_months = {"1mo": 1, "3mo": 3, "6mo": 6, "1y": 12}
        available_end = pd.Timestamp(tech_history_frame["date"].max())
        display_start = available_end - pd.DateOffset(months=period_months[tech_period])
        tech_frame = tech_history_frame.loc[pd.to_datetime(tech_history_frame["date"]) >= display_start].copy().reset_index(drop=True)
        # OBV's absolute origin is arbitrary; rebase it to the visible range.
        if not tech_frame.empty:
            tech_frame["obv"] = tech_frame["obv"] - float(tech_frame["obv"].iloc[0])
        if not tech_frame.empty:
            chart_height = 600 if tech_lower_indicator != "不显示副图" else 440
            tech_fig = technical_indicator_figure(
                tech_frame, tech_overlays, tech_lower_indicator,
                show_levels=tech_show_levels, show_fibonacci=tech_show_fibonacci,
                height=chart_height,
            )
            # Standard Streamlit Plotly rendering avoids custom iframe click/state bugs.
            st.plotly_chart(
                tech_fig, width="stretch", key="tech_indicator_chart",
                config={"displaylogo": False, "scrollZoom": False, "doubleClick": "reset"},
            )
            st.caption(
                f"数据：{tech_symbol} · {TICKERS.get(tech_symbol, tech_symbol)}｜{PERIODS[tech_period]}｜"
                f"{pd.Timestamp(tech_frame['date'].min()):%Y-%m-%d} 至 {pd.Timestamp(tech_frame['date'].max()):%Y-%m-%d}。"
                "数据来源：Yahoo Finance 调整后日线。"
            )
            if tech_show_levels or tech_show_fibonacci:
                extrema = technical_range_extrema(tech_frame)
                if extrema and len(extrema["data"]) >= 5:
                    low_row = extrema["low_row"]
                    high_row = extrema["high_row"]
                    range_summary = (
                        f"当前参考范围：{pd.Timestamp(extrema['data']['date'].iloc[0]):%Y-%m-%d} 至 "
                        f"{pd.Timestamp(extrema['data']['date'].iloc[-1]):%Y-%m-%d}。"
                        f"区间最低价 ${float(low_row['low']):,.2f}（{pd.Timestamp(low_row['date']):%Y-%m-%d}）；"
                        f"区间最高价 ${float(high_row['high']):,.2f}（{pd.Timestamp(high_row['date']):%Y-%m-%d}）。"
                    )
                    if tech_show_fibonacci and int(extrema["low_pos"]) == int(extrema["high_pos"]):
                        range_summary += "最高价与最低价出现在同一根 K 线上，无法可靠推断波段方向，因此暂不绘制斐波那契线；可以尝试缩短历史范围。"
                    elif tech_show_fibonacci:
                        range_summary += "斐波那契线按区间极值的先后顺序生成，仅为教学示意。"
                    range_summary += "这些线不等于程序已识别有效波段或真实供需区域，请勿将其视为必然支撑、阻力或买卖点。"
                    st.info(range_summary)
                else:
                    st.info("当前历史数据不足 5 根有效 K 线，无法可靠绘制该参考信息。")
        else:
            st.info("所选历史范围没有可显示的数据。请更换范围或检查行情接口。")
    else:
        st.info("目前没有可显示的历史数据。请检查网络后刷新，或先继续阅读下方课程内容。")

    # The explanation is directly below the chart and follows the single selected indicator.
    with st.container(border=True):
        if tech_indicator_choice == "斐波那契回撤":
            st.markdown("#### 斐波那契回撤｜把一段价格波动拆成可观察的比例")
            st.markdown(escape_markdown_dollars("""
**斐波那契回撤是什么？** 当价格完成一段上涨或下跌后，随后常会向相反方向移动一段距离。回撤线把原波段划分为几个常见比例，供观察价格可能停顿的位置。

| 比例 | 直观理解 | 100 美元涨至 150 美元后的回撤价 |
|---|---|---:|
| 23.6% | 浅回撤 | $138.20 |
| 38.2% | 较浅回撤 | $130.90 |
| 50.0% | 波段中点 | $125.00 |
| 61.8% | 常受关注的比例 | $119.10 |
| 78.6% | 较深回撤 | $110.70 |

**怎样使用？** 先找同一段走势中清晰的波段低点和高点，再选择上涨后回落或下跌后反弹的方向。价格接近线位时，回看 K 线形态、成交量和历史支撑阻力是否也提供线索。

**图上的线从哪里来？** 本实验室会按所选历史范围的高低点生成教学线，尚未自动识别最合适的局部波段。切换历史范围后，端点和对应参考价也会随之改变。

**记住两点：** 50% 是市场常用的中点参考，并非直接来自相邻斐波那契数列项的比值；这些比例不是价格必然反转的规律。只有结合具体价格行为，才能判断某一区域是否值得继续观察。

            """))

        else:
            render_technical_indicator_lesson(tech_indicator_choice)

    with st.expander("指标分类速览｜先问问题，再选工具", expanded=False):
        map_cols = st.columns(4, gap="small")
        map_cards = [
            ("🧭", "趋势与趋势强度", "MA / EMA、ADX", "价格平均方向如何？走势是否正在形成较强趋势？"),
            ("⚡", "动能", "RSI、MACD、随机指标", "上涨或下跌的动能和相对位置有什么变化？"),
            ("〰️", "波动范围", "布林带", "近期波动正在扩张还是收窄？"),
            ("📊", "量价关系", "OBV", "累计成交量方向是否与价格走势一致？"),
        ]
        for col, (icon_text, title_text, tags_text, body_text) in zip(map_cols, map_cards):
            with col:
                info_card(icon_text, title_text, body_text, tags_text)
    section_heading("A REPEATABLE METHOD", "一套可重复的读图流程", "每次分析都用相同的顺序，先描述证据，再提出假设，最后写下反例和风险。")
    flow_cols = st.columns(4, gap="medium")
    flow_steps = [
        ("01", "位置与趋势", "先看价格结构，以及 MA / EMA 的方向；不要只看刚刚出现的交叉。"),
        ("02", "动能状态", "再看 RSI、MACD 或随机指标。它们有信息重叠，不需要全选。"),
        ("03", "波动与量价", "用布林带判断波动范围变化，用成交量 / OBV 检查量价线索。"),
        ("04", "找反例并管理风险", "检查支撑阻力、事件背景与失效条件。并核对相反证据和风险。"),
    ]
    for col, (number, title_text, body_text) in zip(flow_cols, flow_steps):
        with col:
            st.markdown(
                f'<div class="cycle-card"><div class="cycle-num">{number}</div><div class="cycle-title">{title_text}</div><div class="cycle-body">{body_text}</div></div>',
                unsafe_allow_html=True,
            )

    section_heading("KNOWLEDGE CHECK", "本章检查｜先理解，再解释", "答对至少 6 题即可通过本章检查；提交后会显示答案与解析，答错可以重试。")
    tech_questions = [
        ("MA5 与 MA20 出现金叉，最稳妥的解读是什么？", ["短期平均价格相对长期平均价格转强，但信号可能滞后或在震荡中失效。", "之后 20 天股价必定上涨。", "成交量一定同步增加。"], 0, "均线交叉描述已经发生的平均价格关系，不保证未来方向；还要检查趋势、位置和风险。"),
        ("RSI 高于 70 时，哪项判断最合理？", ["股票已经涨过头，下一根 K 线必然下跌。", "近期上涨动能相对较强，可能处于常说的超买区，但强趋势可以维持高 RSI。", "公司估值低于同行。"], 1, "70 是常见参考水平，不是确定的反转线。RSI 只描述价格动能，不直接测量公司价值。"),
        ("MACD 的 DIF 和 DEA 主要来自什么？", ["公司的收入和净利润。", "成交量与流通股数量。", "不同周期的指数移动平均线及其平滑结果。"], 2, "DIF 是 EMA12 与 EMA26 的差；DEA 通常是 DIF 的 9 期 EMA。指标来自历史价格。"),
        ("布林带明显收窄，最准确的说法是什么？", ["市场一定马上向上突破。", "近期价格波动相对收敛，未来扩张方向仍未确定。", "股价已经被证明低估。"], 1, "收窄描述波动状态，不提前告诉突破方向。要观察后续价格与市场背景。"),
        ("随机指标与 RSI 的主要区别是什么？", ["随机指标比较收盘价在近期高低区间的位置；RSI 比较近期涨跌幅度的相对强弱。", "随机指标只看公司利润；RSI 只看成交量。", "两者都能准确预测反转日期。"], 0, "两者都属于动能振荡指标，但计算思路不同，信号也可能重叠。"),
        ("ADX 高于 25 时，哪项解释更合理？", ["一定是上涨趋势，因为 ADX 只在上涨时上升。", "通常提示趋势可能较强，但 ADX 本身不说明方向。", "代表 RSI 已经超过 70。"], 1, "ADX 衡量趋势强度；+DI 与 −DI 才提供方向性比较。20 / 25 是经验参考，不是硬性规则。"),
        ("当价格上涨但 OBV 没有同步走高，应该怎样处理？", ["认定股价一定会下跌并立即卖出。", "忽略成交量，因为它永远没有分析价值。", "把它当作量价不一致的观察线索，再检查价格结构、异常成交量和后续走势。"], 2, "OBV 背离或不确认值得进一步检查，但不能单独证明反转已经发生。"),
        ("为什么不应同时开启所有指标并把它们当成独立确认？", ["部分指标都从同一组价格数据推导，信息可能重叠；指标越灵敏也可能带来越多假信号。", "指标越多，结果在统计上就必定越准确。", "因为指标只适用于期权，不适用于股票。"], 0, "应先明确每个工具测量什么，避免重复计数同一信息，并主动寻找相反证据。"),
    ]
    with st.form("technical_indicator_quiz_form"):
        tech_answers = []
        for qi, (question, options, correct_idx, explanation) in enumerate(tech_questions):
            tech_answers.append(st.radio(f"{qi + 1}. {question}", options, index=None, key=f"technical_indicator_quiz_{qi}"))
        tech_submit = st.form_submit_button("提交本章答案", width="stretch")
    if tech_submit:
        if any(answer is None for answer in tech_answers):
            st.warning(f"还有 {sum(answer is None for answer in tech_answers)} 题未作答，请完成全部题目后再提交。")
        else:
            score = sum(answer == q[1][q[2]] for answer, q in zip(tech_answers, tech_questions))
            passed = score >= 6
            record_quiz_attempt("技术指标入门", passed)
            st.session_state["tech_indicator_quiz_result"] = {"score": score, "passed": passed, "answers": tech_answers}
    tech_result = st.session_state.get("tech_indicator_quiz_result")
    if tech_result:
        if tech_result["passed"]:
            st.success(f"本次答对 {tech_result['score']}/{len(tech_questions)} 题，已通过本章检查。")
        else:
            st.warning(f"本次答对 {tech_result['score']}/{len(tech_questions)} 题。请先查看解析，再重新尝试；系统会保留曾经通过的记录。")
        for qi, (question, options, correct_idx, explanation) in enumerate(tech_questions):
            selected_answer = tech_result["answers"][qi]
            with st.expander(f"{'✓' if selected_answer == options[correct_idx] else '↻'} 第 {qi + 1} 题解析"):
                st.markdown(f"**正确答案：** {options[correct_idx]}\n\n{explanation}")

    lesson_completion_button("技术指标入门", "finish_technical_indicators")


# ============================================================
# Lesson 3: How a trade works
# ============================================================
elif chosen_page == "03 交易如何执行":
    hero("第三课｜一笔股票交易是怎样完成的？", "从选择证券到订单成交，理解券商、报价、订单类型、费用与交易记录。这里使用模拟情境，不连接真实券商。", "LESSON 03 · HOW TRADING WORKS")
    section_heading("THE WORKFLOW", "一笔交易的 6 个基本步骤")
    workflow = [
        ("01", "明确计划", "先明确目标、投资期限、可承担损失和这笔资金是否会影响日常开支。"),
        ("02", "研究证券", "了解业务/产品、资产类型、风险、费用与可靠信息来源，不只听从他人荐股。"),
        ("03", "核实券商与账户", "核实券商或中介的监管身份、收费、客户资产安排、账户币种及当地适用规则。"),
        ("04", "选择订单", "确认代码、买卖方向、数量、订单类型、价格条件和有效期。"),
        ("05", "检查再提交", "确认预计金额、买卖价差、费用和订单摘要。模拟练习不提交真实订单。"),
        ("06", "检查成交与记录", "订单可能全部成交、部分成交、未成交、被拒绝或取消。成交后核对价格、数量、费用与对账单。"),
    ]
    for num, title, body in workflow:
        st.markdown(f'<div class="step-line"><div class="step-num">{num}</div><div class="step-body"><b>{title}</b><br>{body}</div></div>', unsafe_allow_html=True)

    section_heading("ORDER TYPES", "三种常见订单有什么区别？")
    order_tabs = st.tabs(["市价单 Market", "限价单 Limit", "止损单 Stop"])
    with order_tabs[0]:
        st.markdown("""
        **市价单**的目标是尽快以当前可获得的市场价格买入或卖出。它一般更强调成交，而不是价格确定性。

        **重要限制**：最后成交价不保证等于你的成交价；价格可能在提交至执行之间变化，流动性不足时也可能分多个价格成交。
        """)
    with order_tabs[1]:
        st.markdown("""
        **限价单**会设定可接受的最高买入价或最低卖出价。

        - 买入限价单：只能以限价或更低价格成交，但市场未到该价格时可能一直不成交。

        - 卖出限价单：只能以限价或更高价格成交，同样不保证一定成交。

        价格控制与成交保证通常不能同时获得。
        """)
    with order_tabs[2]:
        st.markdown("""
        **止损单（Stop Order）**通常在触及触发价后转为市价单；触发后的成交价格不一定等于止损价。

        有些券商提供止损限价单（Stop-Limit），但这类订单可能在快速波动时无法成交。名称、触发方式和可用性要以具体券商规则为准。
        """)

    section_heading("ACCOUNT BASICS", "现金账户、保证金账户与碎股")
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        info_card("💵", "现金账户 Cash Account", "一般要求使用账户可用资金完成买入。仍要了解结算、资金可用性和券商具体规则。", "账户基础")
    with ac2:
        info_card("⚠️", "保证金账户 Margin Account", "可能允许向券商借款或持有特定杠杆敞口；涉及利息、维护保证金、追加资金或强制平仓风险。不要把它当作普通现金账户。", "复杂度更高")
    with ac3:
        info_card("🧩", "碎股 Fractional Shares", "有些券商允许买入不足一整股的份额，有些证券或订单类型不支持；转仓、投票、执行方式也可能有差异。", "以券商条款为准")

    section_heading("TRY IT", "模拟报价：你更重视成交还是价格？", "以下数字是教学用的虚构报价，不是任何证券的当前市场报价。")
    bid_col, ask_col, last_col = st.columns(3)
    bid_col.metric("最佳买价 Bid", "$99.95")
    ask_col.metric("最佳卖价 Ask", "$100.05")
    last_col.metric("最近成交价 Last", "$100.00")
    st.markdown(escape_markdown_dollars('<div class="callout">买卖价差（Bid-Ask Spread）= 最佳卖价 − 最佳买价 = $0.10。价差是交易成本的一种表现；报价可能变化，且实际执行还受流动性和订单队列影响。</div>'), unsafe_allow_html=True)
    order_choice = st.radio("你想买入 10 股，最关心什么？", [
        "希望尽快成交，接受成交价可能变化：市价单更贴近这个目标",
        "只愿意以 $99.90 或更低买入：可以考虑买入限价单，但可能不成交",
        "无论哪种订单都能保证以 $100.00 成交",
    ], key="order_type_practice")
    if st.button("查看订单练习解析", key="order_type_submit"):
        passed = order_choice.startswith("希望尽快") or order_choice.startswith("只愿意")
        record_quiz_attempt("交易如何执行", passed)
        if passed:
            st.success("理解正确：订单类型反映不同的价格与成交取舍。选择哪种取决于目标、市场状态和券商规则。")
            st.session_state["order_practice_passed"] = True
        else:
            st.error("没有一种常见订单能保证在所有市场条件下都以最近成交价成交。市价单价格不确定，限价单可能无法成交。")
    with st.expander("交易前还必须理解的细节"):
        st.markdown("""
        - **数量与最小交易单位**：整股、碎股和最小下单数量取决于证券及券商。

        - **订单有效期**：例如当日有效、取消前有效等选项由券商支持情况决定。

        - **交易时段**：常规时段以外的交易可能流动性较低、价差较大、价格波动更明显，部分订单类型可能受限制。不同交易所与节假日安排不同。

        - **费用**：除显性佣金外，也要检查买卖价差、交易/监管费用、货币兑换成本、基金费用，以及适用的税费。费用按地区、产品和券商而不同。

        - **结算**：成交和资金/证券完成结算不是同一个概念；结算规则因市场、产品和司法辖区而异，应查看券商说明。

        - **高级交易**：保证金、卖空、期权和杠杆产品涉及额外机制与风险。入门学习应先理解普通现金买入/卖出的流程，再研究这些工具。
        """)
    st.markdown('<div class="warning-callout">本页面不连接券商、不提交真实订单，也不推荐特定交易方式。实际订单选项、执行规则和费用请以受监管券商的最新文件为准。</div>', unsafe_allow_html=True)
    lesson_completion_button("交易如何执行", "finish_trade_mechanics")


# ============================================================
# Lesson 4: Research a company — interactive beginner version
# ============================================================
elif chosen_page == "04 研究一家公司":
    hero(
        "第四课｜像侦探一样研究一家公司",
        "从三张财报入手，回答：公司赚到钱了吗？钱收回来了吗？资产和债务状况如何？",
        "LESSON 04 · COMPANY RESEARCH LAB",
    )
    st.markdown("**本课方法：先问商业问题，再找财务证据。**")
    st.write("本课使用虚构的橙果饮品公司示例，学习三张财报、财务指标、案例分析，并将方法用于真实公司研究。")

    # Use a stateful selector instead of st.tabs here. The chart controls below
    # trigger reruns; a keyed widget guarantees the selected lesson section persists.
    lesson_section = st.radio(
        "本课内容",
        ["01 · 三张财报", "02 · 指标翻译器", "03 · 案例侦探", "04 · 研究真实公司"],
        key="company_research_section",
        horizontal=True,
        label_visibility="collapsed",
    )

    # --- Tab 2: statements as three different views ---
    if lesson_section == "01 · 三张财报":
        section_heading("THREE STATEMENTS · ONE STORY", "三张报表回答三个不同的问题", "损益表看一段期间的利润；资产负债表看报告日的资产、负债与权益；现金流量表看一段期间的现金流。以下统一使用橙果饮品公司的教学数据。")
        st.markdown("#### 选择一张报表")
        st.markdown("先看图，再按步骤阅读计算过程和分析要点。")
        statement_cards = [
            {"prefix": "①", "label": "损益表", "question": "这段时间赚了多少？", "copy": "从营收开始，逐步扣掉直接成本、经营费用和利息税费，理解毛利、营业利润与净利润。", "value": "① 损益表"},
            {"prefix": "②", "label": "资产负债表", "question": "现在有什么、欠多少？", "copy": "把现金、应收账款、存货、设备与债务、股东权益放在一起看，理解公司的财务位置。", "value": "② 资产负债表"},
            {"prefix": "③", "label": "现金流量表", "question": "现金实际怎么流动？", "copy": "分清经营、投资与筹资现金流，理解公司是靠生意收钱、花钱扩张，还是通过融资增加现金。", "value": "③ 现金流量表"},
        ]
        statement_mode = st.session_state.get("company_statement_choice", "① 损益表")
        nav_cols = st.columns(3, gap="medium")
        for i, card in enumerate(statement_cards):
            active = statement_mode == card["value"]
            with nav_cols[i]:
                active_class = " is-active" if active else ""
                st.markdown(
                    f'<div class="statement-nav-card{active_class}"><div class="statement-nav-number">FINANCIAL STATEMENT {card["prefix"]}</div><div class="statement-nav-title">{card["label"]}</div><div class="statement-nav-question">{card["question"]}</div><div class="statement-nav-copy">{card["copy"]}</div></div>',
                    unsafe_allow_html=True,
                )
                button_label = "✓ 当前正在查看" if active else "查看图表 + 详细讲解 →"
                st.button(
                    button_label,
                    key=f"statement_nav_{i}",
                    width="stretch",
                    on_click=choose_company_statement,
                    args=(card["value"],),
                )
        statement_mode = st.session_state.get("company_statement_choice", "① 损益表")
        st.caption("教学案例：橙果饮品公司为虚构公司，金额单位为美元。数字经过简化，用于演示报表结构与计算。")
        if statement_mode.startswith("① 损益表"):
            income_fig = go.Figure(go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "total", "relative", "total", "relative", "total"],
                x=["营收", "直接成本", "毛利", "经营费用", "营业利润", "利息及税", "净利润"],
                y=[10000, -4000, 6000, -4000, 2000, -500, 1500],
                customdata=[["$10,000"], ["−$4,000"], ["$6,000"], ["−$4,000"], ["$2,000"], ["−$500"], ["$1,500"]],
                hovertemplate="<b>%{x}</b><br>金额：%{customdata[0]}<extra></extra>",
                connector={"line": {"color": "#71849d", "width": 1.2}},
                increasing={"marker": {"color": "#58d7b2"}},
                decreasing={"marker": {"color": "#ff8794"}},
                totals={"marker": {"color": "#80baff"}},
            ))
            st.markdown("#### 橙果饮品公司 · 损益桥")
            style_fig(income_fig, 455)
            income_fig.update_layout(
                showlegend=False, title=None,
                yaxis_title="金额（美元）", yaxis=dict(tickformat="$,.0f", rangemode="tozero", tickfont=dict(size=12)),
                # Angled category labels reduce collisions on phone-sized viewports.
                xaxis=dict(tickangle=-25, tickfont=dict(size=12), automargin=True),
                margin=dict(l=28, r=24, t=24, b=104), waterfallgap=0.28,
            )
            st.plotly_chart(income_fig, width="stretch", key="income_statement_waterfall")
            st.caption("横轴是项目，纵轴是金额。成本与费用从前一步结果中扣除，小计显示扣除后的金额。悬停在柱上可核对数值。")

            st.markdown("### 一步一步读懂这张损益表")
            st.markdown("**先抓住核心：营收不是利润。** 这张图是一条从销售收入出发、逐层扣除成本和费用的路径。它回答的是：在一个报告期间内，橙果饮品公司通过经营产生了多少会计利润？它不直接回答公司账上现在有多少现金，也不能直接告诉你股票是否便宜。")
            income_steps = [
                ("第 1 步｜营收 $10,000", "这是顾客购买果饮和轻食形成的销售收入，是整条计算的起点。它不是老板最终能拿走的钱，因为制作产品、支付员工和经营门店都需要花钱。分析真实公司时，还要看营收来自销量增加、提价、收购还是汇率变化，并检查收入确认政策。"),
                ("第 2 步｜扣直接成本 $4,000，得到毛利 $6,000", "直接成本指与提供产品或服务直接相关的成本；本例可理解为水果、饮料原料、杯子和食品等成本。$10,000 − $4,000 = $6,000。毛利率 = $6,000 ÷ $10,000 = 60%，意思是每做出 $1 销售收入，扣掉直接成本后还剩约 $0.60，用来支付租金、员工管理成本、营销等其他开支并形成利润。"),
                ("第 3 步｜扣经营费用 $4,000，得到营业利润 $2,000", "经营费用可包括门店租金、行政人员薪酬、市场推广、水电、软件和其他日常运营开支。本例 $6,000 − $4,000 = $2,000。营业利润率为 20%。它帮助我们观察主营经营在支付直接成本和经营费用后，剩余多少利润；但真实报表对成本和费用的分类会随行业与会计政策而异。"),
                ("第 4 步｜再扣利息及税等 $500，得到净利润 $1,500", "利息、所得税及其他相关项目在本例中合计 $500。净利润 = $2,000 − $500 = $1,500；净利润率 = $1,500 ÷ $10,000 = 15%，即每 $1 营收形成约 $0.15 的会计净利润。净利润与实际收到的现金不是同一概念。"),
            ]
            for step_title, step_copy in income_steps:
                st.markdown(escape_markdown_dollars(f"**{step_title}**\n\n{step_copy}"))
            st.markdown(escape_markdown_dollars("本例计算结果：毛利 $6,000（毛利率 60%）；营业利润 $2,000（营业利润率 20%）；净利润 $1,500（净利润率 15%）。三个利润率分别对应不同的成本扣除阶段。"))
            st.markdown("### 读完图后，还要追问什么？")
            st.markdown("- **利润率在改善还是恶化？** 将当前期间与过去数季/数年比较，看看成本涨得是否比收入快。单独看一期，难以判断趋势。\n- **增长是否可持续？** 营收增长可能来自销量、涨价或一次性因素；需要继续阅读管理层讨论、分部数据和附注。\n- **利润有没有变成现金？** 损益表通常按权责发生制记录收入和费用。顾客赊账购买，可能已经确认收入，却还没付款；因此下一步要对照现金流量表。")
            st.markdown("净利润反映指定期间的会计经营结果。现金余额和债务要查看资产负债表，现金收付要查看现金流量表，股票估值还要结合增长、风险与市场价格。")
        elif statement_mode.startswith("② 资产负债表"):
            balance_df = pd.DataFrame({
                "项目": ["现金", "应收账款", "存货", "设备等资产", "应付账款", "短期借款", "长期借款", "股东权益"],
                "金额（美元）": [1800, 2200, 1800, 6500, 1800, 1500, 4000, 5000],
            })
            # Distinguish what the company owns from what it owes; equity is shown separately.
            balance_colors = ["#58d7b2"] * 4 + ["#ff8794"] * 3 + ["#75b7ff"]
            balance = go.Figure(go.Bar(
                x=balance_df["金额（美元）"], y=balance_df["项目"], orientation="h",
                marker_color=balance_colors, text=[f"${v:,.0f}" for v in balance_df["金额（美元）"]],
                textposition="outside", cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>金额：$%{x:,.0f}<extra></extra>",
            ))
            st.markdown("#### 橙果饮品公司 · 资产与资金来源")
            style_fig(balance, 455)
            balance.update_layout(
                title=None,
                xaxis_title="金额（美元）", xaxis=dict(tickformat="$,.0f", range=[0, 7900], automargin=True, tickfont=dict(size=12)),
                yaxis=dict(title="", autorange="reversed", tickfont=dict(size=13), automargin=True),
                showlegend=False, margin=dict(l=36, r=112, t=24, b=38), bargap=0.3,
            )
            st.plotly_chart(balance, width="stretch", key="balance_sheet_components")
            st.caption("绿色表示公司拥有的资产；红色表示公司需要偿还或履行的负债；蓝色单独表示股东权益。横柱长度表示金额。")
            st.markdown(escape_markdown_dollars("资产 $12,300 = 负债 $7,300 + 股东权益 $5,000"))

            st.markdown("### 一步一步读懂这张资产负债表")
            st.markdown("**先记住：它像一张某个日期的快照。** 损益表描述一段期间，而资产负债表描述报告日当天公司拥有什么、承担什么义务，以及股东账面上剩余多少权益。这里的数字是某一时点的存量，不是过去一整年赚了多少钱。")
            st.markdown(escape_markdown_dollars("**第 1 步｜先看资产：公司控制哪些资源？** 本例资产合计 $12,300，由现金 $1,800、应收账款 $2,200、存货 $1,800、设备等资产 $6,500 组成。现金通常最容易直接用于支付账单；应收账款是客户尚未支付的款项，存在收款时间和坏账风险；存货需要卖出去后才能转成现金，也可能过期、损坏或需要打折；设备能支持经营，但通常不能像现金一样随时拿来付款。虽然这些项目都列作资产，变现速度和风险并不相同。"))
            st.markdown(escape_markdown_dollars("**第 2 步｜再看负债：公司有哪些需要偿还或履行的义务？** 本例应付账款 $1,800、短期借款 $1,500、长期借款 $4,000，负债合计 $7,300。应付账款通常来自尚未支付给供应商的采购款；短期借款的偿还期限较近；长期借款期限较长，但仍然有利息和还本义务。分析真实企业时，不能只看借款总额，还要看现金余额、到期时间、利率、利息支出和公司能否持续产生现金。"))
            st.markdown(escape_markdown_dollars("**第 3 步｜股东权益 $5,000：** 资产 − 负债 = 股东权益，即 $12,300 − $7,300 = $5,000。股东权益是按会计账面口径计算的剩余权益，不是现金余额，也不等于股票市值；股票市值通常按股价 × 流通股数计算。"))
            st.markdown("### 继续分析的三个重点")
            st.markdown("- **短期偿付能力：** 比较现金、流动资产与短期到期债务。\n- **营运资金质量：** 对比应收账款、存货与营收的多年变化。\n- **债务压力：** 查看借款利率、到期结构，以及经营现金流的偿债能力。")
        else:
            cash_flow = pd.DataFrame({"活动": ["经营活动现金流", "投资活动现金流", "筹资活动现金流", "现金净变化"], "现金流（美元）": [900, -1500, 1000, 400]})
            cf_colors = ["#58d7b2" if v >= 0 else "#ff8794" for v in cash_flow["现金流（美元）"]]
            cf_colors[-1] = "#75b7ff"  # Net change / ending cash summary is a distinct total color.
            cf_fig = go.Figure(go.Bar(
                x=cash_flow["现金流（美元）"], y=cash_flow["活动"], orientation="h",
                marker_color=cf_colors, text=[f"${v:+,.0f}" for v in cash_flow["现金流（美元）"]],
                textposition="outside", cliponaxis=False,
                hovertemplate="<b>%{y}</b><br>现金流：$%{x:,.0f}<extra></extra>",
            ))
            st.markdown("#### 橙果饮品公司 · 现金流方向")
            style_fig(cf_fig, 430)
            cf_fig.update_layout(
                title=None,
                xaxis_title="现金流（美元）", xaxis=dict(tickformat="$,.0f", zeroline=True, zerolinecolor="#aabbd0", range=[-2050, 1550], tickfont=dict(size=12)),
                yaxis_title="", yaxis=dict(autorange="reversed", tickfont=dict(size=13), automargin=True),
                showlegend=False, margin=dict(l=42, r=112, t=24, b=38), bargap=0.32,
            )
            st.plotly_chart(cf_fig, width="stretch", key="cashflow_statement_bars")
            st.caption("绿色表示现金流入，红色表示现金流出，蓝色单独标示现金净变化这一汇总结果。零线右侧为流入，左侧为流出。")
            st.markdown(escape_markdown_dollars("现金净变化 = $900 − $1,500 + $1,000 = +$400"))

            st.markdown("### 一步一步读懂这张现金流量表")
            st.markdown("**先抓住核心：利润和现金不是同一件事。** 损益表可以记录已经赚取但还没有收到的收入，也会记录暂时没有支付现金的费用；现金流量表则按现金实际收付来追踪资金变化。它帮助你判断公司经营有没有带来现金，以及现金被用在了哪里。")
            st.markdown(escape_markdown_dollars("**第 1 步｜经营活动现金流 +$900：** 客户收款扣除供应商货款、薪酬、租金和税费等经营支出后，净流入 $900。对比净利润和多年趋势，可以判断经营活动的现金创造能力。"))
            st.markdown(escape_markdown_dollars("**第 2 步｜投资活动现金流 −$1,500：** 投资活动包括购置或出售设备、装修门店、收购业务及投资资产交易。本例净流出 $1,500。查看现金流明细可确认资金用途，再比较后续收入、利润和现金流变化。"))
            st.markdown(escape_markdown_dollars("**第 3 步｜筹资活动现金流 +$1,000：** 筹资活动包括借款、偿还借款、发行股份和分红。本例净流入 $1,000，具体来源决定后续影响：借款增加偿债义务，发行股份会摊薄原股东持股比例。"))
            st.markdown(escape_markdown_dollars("**第 4 步｜现金净增加 $400：** 期末现金余额还需结合期初现金，并考虑汇率影响等报表项目。"))
            st.markdown("### 继续分析的四个重点")
            st.markdown("- **经营现金流趋势：** 查看多年数据与季节性。\n- **利润与现金差异：** 检查应收账款、存货、应付账款及折旧等项目。\n- **投资用途：** 确认资本开支、收购或其他投资的具体去向。\n- **筹资来源：** 区分经营现金、资产出售、借款和发行股票带来的现金。")
        st.markdown("#### 把三张报表连起来")
        st.markdown("""- **损益表：** 看一段期间的收入、成本、费用与利润。
- **资产负债表：** 看报告日的资产、负债与股东权益。
- **现金流量表：** 看一段期间现金从哪里来、用到哪里。

三张报表需要交叉阅读。应收账款、存货、折旧、资本开支与融资活动，都会影响利润、资产状况和现金变化之间的关系。""")

    # --- Tab 3: Metric translator with editable inputs ---
    elif lesson_section == "02 · 指标翻译器":
        section_heading("METRIC TRANSLATOR", "把财务术语翻译成日常问题", "先想这个指标在回答什么，再看公式。选择指标后，可以修改示例数字，观察结果会怎样变化。")
        metric_options = ["营收增长率", "毛利率", "净利润率", "每股收益 EPS", "市盈率 P/E", "有息债务 / 股东权益", "经营现金流 / 净利润", "自由现金流 FCF"]
        metric_choice = st.selectbox("你想搞懂哪个指标？", metric_options, key="company_metric_translator")
        mleft, mright = st.columns([1, 1], gap="large")
        with mleft:
            st.markdown("**修改示例数字**")
            if metric_choice == "营收增长率":
                old_value = st.number_input("上期营收（美元）", min_value=1.0, value=8000.0, step=500.0, key="metric_rev_old")
                new_value = st.number_input("本期营收（美元）", min_value=0.0, value=10000.0, step=500.0, key="metric_rev_new")
                metric_result = (new_value / old_value - 1) * 100 if old_value > 0 else np.nan
                result_text = f"{metric_result:+.1f}%" if pd.notna(metric_result) else "无法计算"
                formula = "（本期营收 − 上期营收）÷ 上期营收 × 100%"
                example = f"（${new_value:,.0f} − ${old_value:,.0f}）÷ ${old_value:,.0f} = {result_text}"
            elif metric_choice == "毛利率":
                revenue = st.number_input("营收（美元）", min_value=1.0, value=10000.0, step=500.0, key="metric_gm_rev")
                cogs = st.number_input("直接成本（美元）", min_value=0.0, value=4000.0, step=250.0, key="metric_gm_cogs")
                metric_result = (revenue - cogs) / revenue * 100
                result_text = f"{metric_result:.1f}%"
                formula = "（营收 − 直接成本）÷ 营收 × 100%"
                example = f"（${revenue:,.0f} − ${cogs:,.0f}）÷ ${revenue:,.0f} = {result_text}"
            elif metric_choice == "净利润率":
                revenue = st.number_input("营收（美元）", min_value=1.0, value=10000.0, step=500.0, key="metric_nm_rev")
                net_income = st.number_input("净利润（美元）", value=1500.0, step=250.0, key="metric_nm_ni")
                metric_result = net_income / revenue * 100
                result_text = f"{metric_result:.1f}%"
                formula = "净利润 ÷ 营收 × 100%"
                example = f"${net_income:,.0f} ÷ ${revenue:,.0f} = {result_text}"
            elif metric_choice == "每股收益 EPS":
                net_income = st.number_input("归属于普通股的净利润（美元）", min_value=-100000000.0, value=1500.0, step=250.0, key="metric_eps_ni")
                shares = st.number_input("加权平均普通股股数（示例）", min_value=1.0, value=1000.0, step=100.0, key="metric_eps_shares")
                metric_result = net_income / shares
                result_text = f"${metric_result:,.2f}/股"
                formula = "归属于普通股股东的净利润 ÷ 加权平均普通股股数"
                example = f"${net_income:,.0f} ÷ {shares:,.0f} 股 = {result_text}"
            elif metric_choice == "市盈率 P/E":
                price = st.number_input("当前股价（美元）", min_value=0.01, value=30.0, step=1.0, key="metric_pe_price")
                eps = st.number_input("每股收益 EPS（美元）", value=1.5, step=0.25, key="metric_pe_eps")
                metric_result = price / eps if eps > 0 else np.nan
                result_text = f"{metric_result:.1f} 倍" if pd.notna(metric_result) else "负盈利/零盈利，不适用简单 P/E"
                formula = "股价 ÷ 每股收益 EPS（须注意盈利期间与口径）"
                example = f"${price:,.2f} ÷ ${eps:,.2f} = {result_text}" if eps > 0 else "当 EPS ≤ 0 时，普通 P/E 通常不适合直接比较。"
            elif metric_choice == "有息债务 / 股东权益":
                debt = st.number_input("短期借款 + 长期借款（美元）", min_value=0.0, value=5500.0, step=500.0, key="metric_debt")
                equity = st.number_input("股东权益（美元）", min_value=-100000000.0, value=5000.0, step=500.0, key="metric_equity")
                metric_result = debt / equity if equity > 0 else np.nan
                result_text = f"{metric_result:.2f} 倍" if pd.notna(metric_result) else "权益为零或负数，需谨慎解释"
                formula = "有息债务 ÷ 股东权益"
                example = f"${debt:,.0f} ÷ ${equity:,.0f} = {result_text}" if equity > 0 else "股东权益为零或负数时，简单倍数可能失去直观意义。"
            elif metric_choice == "经营现金流 / 净利润":
                cfo = st.number_input("经营活动现金流（美元）", value=900.0, step=250.0, key="metric_cfo")
                net_income = st.number_input("净利润（美元）", value=1500.0, step=250.0, key="metric_cfo_ni")
                metric_result = cfo / net_income if net_income != 0 else np.nan
                result_text = f"{metric_result:.2f} 倍" if pd.notna(metric_result) else "净利润为零，无法计算"
                formula = "经营活动现金流 ÷ 净利润"
                example = f"${cfo:,.0f} ÷ ${net_income:,.0f} = {result_text}" if net_income != 0 else "净利润为零时无法计算。"
            else:
                cfo = st.number_input("经营活动现金流（美元）", value=900.0, step=250.0, key="metric_fcf_cfo")
                capex = st.number_input("资本开支（美元）", min_value=0.0, value=1200.0, step=250.0, key="metric_fcf_capex")
                metric_result = cfo - capex
                result_text = f"${metric_result:,.0f}"
                formula = "自由现金流（简化） = 经营活动现金流 − 资本开支"
                example = f"${cfo:,.0f} − ${capex:,.0f} = {result_text}"
        with mright:
            st.markdown(escape_markdown_dollars(f"**{metric_choice}**\n\n公式：{formula}\n\n示例：{example}"))
            st.markdown(escape_markdown_dollars(f"当前示例计算结果：{result_text}"))
            explainers = {
                "营收增长率": ("它回答：公司卖出去的商品或服务收入，比上期多了还是少了？", "增长可能来自销量、涨价、收购或汇率；营收增长不自动等于利润或现金增长。", "查看毛利率、净利润率、现金流，以及管理层解释增长来源。"),
                "毛利率": ("每 100 美元营收，在扣除直接成本后还剩多少。", "毛利还没有扣除全部研发、营销、管理、利息和税费。", "比较同一公司历年变化，并找同行业作为参照。"),
                "净利润率": ("每 100 美元营收，最终留下多少会计净利润。", "一次性收益、税项或会计估计可能让某一期净利润特别高或低。", "同时查看现金流和利润是否可持续。"),
                "每股收益 EPS": ("把某一期间的盈利按加权平均股数分摊到每股。", "EPS 上升不一定意味着总利润同比同幅增长；股份回购或股数变化也会影响它。", "同时查看净利润和加权平均股数的变化。"),
                "市盈率 P/E": ("市场价格相对于每股收益的倍数，可理解为市场为每一单位当前盈利支付多少价格。", "低 P/E 不保证便宜，高 P/E 也不自动意味着高估；增长预期、风险和会计口径很重要。", "与同行业、公司历史区间、增长前景和盈利质量一起比较。"),
                "有息债务 / 股东权益": ("粗略观察公司用多少有息债务相对于股东权益来支持经营。", "不同来源可能对债务和权益采用不同口径；银行、保险等行业也需特别谨慎。", "继续看债务期限、利率、现金余额和利息覆盖能力。"),
                "经营现金流 / 净利润": ("检查会计利润是否在同一期间转化成经营现金。", "单期比率可能受季节性、客户付款时间和营运资金变动影响，不能独立用作质量判定。", "查看多期趋势，并检查应收账款、存货和应付账款变化。"),
                "自由现金流 FCF": ("简化理解为经营现金流扣掉资本开支后剩下的现金。", "负自由现金流可能来自扩张投资，也可能反映资金压力；不同公司披露口径可能不同。", "查看资本开支目的、经营现金流趋势、融资需求和债务到期安排。"),
            }
            plain, caution, next_evidence = explainers[metric_choice]
            st.markdown(f"**白话解释：** {plain}")
            st.markdown(f"**容易误读：** {caution}")
            st.markdown(f"**下一步找证据：** {next_evidence}")
        with st.expander("想快速复习其他常见指标？"):
            quick_table = pd.DataFrame([
                {"指标": "营收 Revenue", "它回答的问题": "公司卖出了多少商品或服务？"},
                {"指标": "毛利率 Gross Margin", "它回答的问题": "扣掉直接成本后，营收还剩多少比例？"},
                {"指标": "净利润 Net Income", "它回答的问题": "扣除相关成本、费用、利息和税后，账面赚了多少？"},
                {"指标": "EPS", "它回答的问题": "会计利润按加权平均股数分摊后，每股是多少？"},
                {"指标": "P/E", "它回答的问题": "当前股价相当于每股盈利的多少倍？"},
                {"指标": "自由现金流 FCF", "它回答的问题": "经营现金扣除资本开支后，简化来看还剩多少？"},
            ])
            st.dataframe(quick_table, width="stretch", hide_index=True)

    # --- Tab 4: Case-based reasoning, not rote definitions ---
    elif lesson_section == "03 · 案例侦探":
        section_heading("CASE INVESTIGATION", "当数字互相矛盾时，先别急着下结论", "真实公司分析经常遇到多个指标发出不同信号。新手的任务不是立刻判断买卖，而是找出下一条最有用的证据。")
        st.caption("三个练习都使用橙果饮品公司的独立假设情境，不代表同一时期的真实财务事实。")
        cases = {
            "案例 A · 营收增长，但经营现金流下降": {
                "story": "橙果饮品公司本期营收同比增长 25%、净利润增长 10%，但经营现金流比去年下降 30%，应收账款和存货都明显增加。",
                "question": "你下一步最应该查什么？",
                "options": ["直接认定公司很好，因为营收增长", "核对应收账款回收、存货积压、现金流调节项及管理层解释", "只看最近一周股价走势"],
                "correct": 1,
                "answer": "先检查现金是否被客户欠款或存货占住，也要查看现金流量表、附注和管理层讨论。营收增长是线索，不是最终结论。",
            },
            "案例 B · 市盈率低于同行": {
                "story": "橙果饮品公司当前 P/E 为 9 倍，同行中位数为 18 倍；但产品销量正在下降，而且有较高债务。",
                "question": "能否直接说它被低估了？",
                "options": ["可以，P/E 更低一定更便宜", "不能；需要检查增长前景、盈利质量、债务风险和低估值的原因", "可以，只要股价低于同行即可"],
                "correct": 1,
                "answer": "低估值可能反映更低的增长预期、更高的风险或盈利处于周期高点。应先问市场为什么只愿意为它当前盈利支付较低倍数。",
            },
            "案例 C · EPS 上升，但总利润变化不大": {
                "story": "橙果饮品公司的净利润大致持平，但 EPS 上升了 8%。同期，公司回购了一部分股份。",
                "question": "你应优先核实什么？",
                "options": ["查看加权平均股数是否下降，以及回购使用了多少现金", "直接认为公司的主营业务增长了 8%", "EPS 上升就不需要查看其他资料"],
                "correct": 0,
                "answer": "EPS = 相关净利润 ÷ 加权平均股数。股数减少可以让 EPS 上升，即使总利润没有显著增加。还需要研究回购成本、现金流与业务发展。",
            },
        }
        case_name = st.selectbox("选择一个调查案例", list(cases.keys()), key="company_investigation_case")
        case = cases[case_name]
        # Each case has different answer choices. Clear a stale answer before
        # constructing the radio widget so a previous case's option cannot linger.
        if st.session_state.get("company_case_answer") not in case["options"]:
            st.session_state["company_case_answer"] = case["options"][0]
        st.markdown(f"**{case_name}**")
        st.write(case["story"])
        case_answer = st.radio(case["question"], case["options"], key="company_case_answer")
        if st.button("提交判断并查看证据", key="company_case_submit"):
            passed = case_answer == case["options"][case["correct"]]
            st.session_state["company_case_last"] = {"case": case_name, "passed": passed, "answer": case_answer}
            record_quiz_attempt("研究一家公司", passed)
        last_case_result = st.session_state.get("company_case_last", {})
        if last_case_result.get("case") == case_name:
            if last_case_result.get("passed"):
                st.success("判断合理。你选择了优先寻找证据，而不是用单一指标直接得出买卖结论。")
            else:
                st.error("这次选择还不够。重新查看案例中的不同信号，再试一次。")
            st.markdown(f"**解析：** {case['answer']}")
        with st.expander("给自己一个提示：什么叫“证据优先”？"):
            st.write("当数字互相矛盾，不要只挑支持自己观点的一项。先找时间序列、财报附注、管理层讨论、行业对照和现金流解释，再判断目前还缺哪些信息。")

    # --- Tab 5: apply framework to real data without pretending all fields are available ---
    elif lesson_section == "04 · 研究真实公司":
        section_heading("APPLY TO A REAL COMPANY", "把方法用到一家公司身上", "先从官方申报文件找证据。数据聚合页面可以帮助你定位数字，但不要把单一摘要当作完整研究。")
        stock_symbols = [s for s in TICKERS.keys() if s not in {"SPY", "QQQ", "EFA", "EEM", "EWJ", "FXI"}]
        real_symbol = st.selectbox("选择一家公司", stock_symbols, format_func=ticker_label, key="company_real_lookup_symbol")
        st.markdown("**第一站：官方申报文件。** 美国上市公司的公开申报资料，可从「数据与方法」页面的 SEC EDGAR 入口查询。")
        st.caption("优先找 10-K 年报与 10-Q 季报：业务介绍、风险因素、管理层讨论（MD&A）和三张财务报表。公司官网的 Investor Relations 页面也可作为入口，但应核实公告和申报日期。")
        if st.button("尝试读取行情聚合服务的公司摘要", key="company_fetch_yahoo_info"):
            with st.spinner("正在尝试读取公开公司摘要；部分字段可能缺失……"):
                try:
                    raw_info = yf.Ticker(real_symbol).get_info()
                    if not isinstance(raw_info, dict):
                        raw_info = {}
                    st.session_state["company_lookup_cache"] = {"symbol": real_symbol, "info": raw_info, "error": None}
                except Exception as exc:
                    st.session_state["company_lookup_cache"] = {"symbol": real_symbol, "info": {}, "error": str(exc)[:500]}
        lookup = st.session_state.get("company_lookup_cache", {})
        if lookup.get("symbol") == real_symbol:
            if lookup.get("error"):
                st.warning("暂时无法获取公司摘要；不影响你使用上面的教学案例。请直接使用 SEC EDGAR 核实。")
            elif lookup.get("info"):
                raw_info = lookup["info"]
                def _fmt_company_number(value, kind="money"):
                    try:
                        val = float(value)
                        if kind == "pct":
                            return f"{val * 100:.2f}%"
                        if kind == "ratio":
                            return f"{val:.2f} 倍"
                        if abs(val) >= 1e12:
                            return f"${val / 1e12:.2f}T"
                        if abs(val) >= 1e9:
                            return f"${val / 1e9:.2f}B"
                        if abs(val) >= 1e6:
                            return f"${val / 1e6:.2f}M"
                        return f"${val:,.2f}"
                    except (TypeError, ValueError):
                        return "—"
                profile_rows = [
                    ("行业", "sector", "text"), ("细分行业", "industry", "text"),
                    ("市值", "marketCap", "money"), ("总营收", "totalRevenue", "money"),
                    ("营收增长", "revenueGrowth", "pct"), ("净利润率", "profitMargins", "pct"),
                    ("市盈率 TTM", "trailingPE", "ratio"), ("预期市盈率", "forwardPE", "ratio"),
                    ("经营现金流", "operatingCashflow", "money"), ("自由现金流", "freeCashflow", "money"),
                    ("总债务", "totalDebt", "money"), ("流动比率", "currentRatio", "ratio"),
                ]
                rows = []
                for label, key, typ in profile_rows:
                    val = raw_info.get(key)
                    if val is None or val == "":
                        continue
                    shown = str(val) if typ == "text" else _fmt_company_number(val, typ)
                    rows.append({"指标": label, "聚合服务返回值": shown})
                if rows:
                    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
                else:
                    st.info("服务没有返回可显示的公司概况字段；请使用官方申报文件。")
                st.caption("聚合服务字段的口径和更新时间可能不同；重要数据以最新公司申报为准。")
                if raw_info.get("website"):
                    website = str(raw_info.get("website"))
                    if website.startswith("https://") or website.startswith("http://"):
                        st.markdown(f"公司网站：[{website}]({website})")
        st.markdown("#### 公司研究检查单")
        checklist_items = [
            "我能用两句话解释公司卖什么、客户是谁、它如何赚钱。",
            "我检查了营收、利润及至少几个期间的变化，而不是只看一个季度。",
            "我把损益表和经营现金流放在一起比较。",
            "我检查了现金、应收账款、存货、有息债务和债务期限等风险。",
            "我知道使用的估值指标是什么口径，也没有只凭一个倍数判断贵或便宜。",
            "我阅读了公司申报中的风险因素和管理层讨论，并记录仍然不确定的问题。",
        ]
        checklist_cols = st.columns(2)
        checked_count = 0
        for idx, item in enumerate(checklist_items):
            with checklist_cols[idx % 2]:
                if st.checkbox(item, key=f"company_research_check_{idx}"):
                    checked_count += 1
        st.progress(checked_count / len(checklist_items), text=f"研究检查单完成 {checked_count}/{len(checklist_items)} 项")
        st.markdown("#### 写下你的研究结论")
        research_note = st.text_area("用三句话完成：我知道什么、我还需要核实什么、最大的不确定性是什么。", key="company_research_note", height=110, placeholder="这家公司主要通过……赚钱。当前数据显示……。我还需要核实……。")
        if st.button("保存研究笔记", key="company_research_save_note"):
            if not research_note.strip():
                st.warning("请先写下至少一句自己的研究结论。")
            else:
                st.session_state["company_research_saved_note"] = research_note.strip()
                st.success("已保存到当前会话。你可以稍后回看；重启应用后可能重置。")
        if st.session_state.get("company_research_saved_note"):
            with st.expander("查看已保存的研究笔记"):
                st.write(st.session_state["company_research_saved_note"])

    st.markdown("---")
    st.caption("本课示例数字为虚构教学数据，不对应真实公司。")
    lesson_completion_button("研究一家公司", "finish_company_research")


# ============================================================
# Lesson 4: Why prices move
# ============================================================
elif chosen_page == "05 股价为什么变化":
    hero("第五课｜股价为什么变化？", "股价不仅反映公司当前的表现，也会受到未来预期、资金成本和整体市场情绪影响。试着从多个角度理解，而不是寻找单一原因。", "LESSON 05 · WHAT MOVES PRICES")
    factors = [
        ("📈", "公司业绩", "营收、利润、现金流和管理层展望会影响投资者对公司未来表现的判断。实际结果与市场原先预期的差别也很重要。", "公司层面"),
        ("🏦", "利率与通胀", "利率会影响融资成本、债券相对吸引力，以及未来现金流的估值。不同公司对利率变化的敏感度可能不同。", "宏观环境"),
        ("🧠", "市场预期", "市场价格会提前反映投资者的预期。因此，即使业绩增长，若不及预期，股价也可能下跌。", "预期差"),
        ("🌍", "行业与竞争", "新产品、竞争者变化、供应链、政策或技术进步可能改变行业前景，但影响常常因公司而异。", "行业环境"),
        ("💧", "供需与流动性", "买卖双方的订单和可交易数量会影响短期价格波动。高成交量本身并不决定涨跌方向。", "市场交易"),
        ("⚡", "突发事件与情绪", "地缘政治、监管、意外消息或风险偏好变化可能迅速改变价格，但消息的影响需要结合背景分析。", "不确定性"),
    ]
    for i in range(0, len(factors), 3):
        row = st.columns(3)
        for col, f in zip(row, factors[i:i+3]):
            with col:
                info_card(f[0], f[1], f[2], f[3])

    st.write("")
    section_heading("CASE PRACTICE", "案例：财报很好，股价为什么仍可能下跌？", "下面是教学情境，不代表某一具体公司的真实事件。")
    st.markdown('<div class="lesson-card"><div class="lesson-title">情境设定</div><div class="lesson-text">某科技公司公布季度利润同比增长 20%。但是，分析师原先预期增长 30%，同时公司下调了下一季度的销售指引。</div></div>', unsafe_allow_html=True)
    case_answer = st.radio("以下哪种解释最合理？", [
        "利润增长就一定会使股价上涨，股价变化不合理",
        "投资者可能更关注业绩是否低于预期，以及未来指引是否转弱",
        "只要当日成交量增加，就能证明股价会下跌",
    ], key="factor_case")
    if st.button("查看案例解析", key="factor_submit"):
        passed = case_answer.startswith("投资者可能")
        record_quiz_attempt("股价为什么变化", passed)
        if passed:
            st.success("正确。市场会比较实际结果与先前预期；预期差常常是解释短期反应的重要线索。")
        else:
            st.error("回到情境：增长 20% 是结果本身；市场还会比较原先预期，并评估未来展望。")
    with st.expander("把股价变化拆成 4 层来研究"):
        st.markdown("""
        1. **公司层面**：销量、价格、成本、管理、产品、竞争、财报与指引。

        2. **行业层面**：供需、技术替代、供应链、监管与行业周期。

        3. **宏观层面**：利率、通胀、就业、经济增长、汇率和政策。

        4. **市场层面**：投资者预期、风险偏好、资金流、流动性和估值水平。

        同一事件可以同时影响多个层面，而且影响可能已经被市场提前预期。分析时要记下事件发生的时间、原始来源、价格变化和其他可能解释，避免事后只挑支持自己观点的证据。
        """)
    with st.expander("基本面分析与技术分析有什么区别？"):
        st.markdown("""
        - **基本面分析**：研究公司业务、财务报表、竞争位置、管理层、估值和外部环境，尝试理解公司的经营与市场价格之间的关系。

        - **技术分析**：研究价格、成交量及由这些数据构成的图表指标，寻找历史模式。历史模式不保证重复，也不能独立证明未来方向。

        - **两者都有限制**：数据可能已被市场预期，财务报表有会计口径差异，图表可能受噪声影响；任何一种方法都不能保证投资结果。

        - **择时风险**：即使长期逻辑看起来合理，买入价格、持有期间、费用和投资者行为仍会影响实际结果。
        """)
    st.markdown("**数据核实建议：** 比较价格和成交量时，可进一步查看公司正式财报、公告日期及相应时期的宏观数据；相关来源统一列在「数据与方法」页面。")
    st.markdown('<div class="warning-callout">分析纪律：先描述你能从数据中观察到的变化，再寻找有证据支持的解释。时间上的先后关系不自动证明因果关系。</div>', unsafe_allow_html=True)
    lesson_completion_button("股价为什么变化", "finish_factors")


# ============================================================
# ============================================================
# Lesson 6: Risk and investor protection
# ============================================================
elif chosen_page == "06 风险与投资者保护":
    hero("第六课｜风险管理与投资者保护", "你无法控制市场怎么走，但可以学习识别风险、降低可避免的错误，并保护自己的账户与判断。", "LESSON 06 · RISK & INVESTOR PROTECTION")
    section_heading("RISK MAP", "新手必须认识的 6 类风险")
    risks = [
        ("📉", "市场风险", "整个市场下跌时，许多证券可能一起下跌。即使公司本身没有明显变化，也可能受到市场环境影响。"),
        ("🏢", "公司与行业风险", "产品失败、竞争、诉讼、管理问题或行业逆风可能影响单家公司或同一行业的企业。"),
        ("💧", "流动性风险", "想买卖时可能找不到足够对手方，必须接受更大的价差或更不利的执行价格。"),
        ("💱", "汇率、通胀与利率风险", "若资产币种与未来支出币种不同，汇率变化会影响本币回报；通胀和利率也会改变实际购买力与资产估值。"),
        ("🧺", "集中风险与相关性", "分散程度取决于资产的行业、风险来源、相关性与持仓重叠，而不只是代码数量。"),
        ("🧠", "行为与操作风险", "追涨杀跌、恐惧错失机会、过度交易、忽略费用、输后加注或误点订单，都可能伤害结果。"),
    ]
    risk_cols = st.columns(3)
    for col, item in zip(risk_cols, risks[:3]):
        with col:
            info_card(item[0], item[1], item[2])
    risk_cols2 = st.columns(3)
    for col, item in zip(risk_cols2, risks[3:]):
        with col:
            info_card(item[0], item[1], item[2])

    section_heading("PROTECT YOURSELF", "投资前自我保护清单")
    check_items = [
        "我能解释这项投资是什么、它如何产生回报，以及可能怎样亏损。",
        "这笔钱不是近期必须用于房租、学费、生活开支或紧急支出的资金。",
        "我检查了产品费用、交易成本、货币兑换成本，以及适用的税务规则。",
        "我了解自己的投资期限和承受亏损的能力，而不只考虑想赚多少。",
        "我检查过证券、券商/顾问和信息来源，不只依赖社交媒体或陌生人的推荐。",
        "我能说明持仓为何分散，且知道分散投资不能消除所有市场风险。",
        "我不会因为别人催促、承诺稳赚或声称内幕消息而匆忙转账或交易。",
    ]
    checks = []
    for idx, label in enumerate(check_items):
        checks.append(st.checkbox(label, key=f"investor_check_{idx}"))
    checked_count = sum(checks)
    st.progress(checked_count / len(check_items), text=f"你完成了 {checked_count}/{len(check_items)} 项自我检查")
    if checked_count < len(check_items):
        st.caption("这份检查表用于复习风险识别；尚未确认的项目可返回相应课程核对。")
    else:
        st.success("你已阅读并确认所有检查项。现实投资中仍需根据具体证券、地区法规和个人情况再次核实。")

    section_heading("RED FLAGS", "这些情况需要高度警惕")
    red_cols = st.columns(2)
    with red_cols[0]:
        info_card("🚩", "承诺高回报、低风险或稳赚", "所有投资都有风险。任何保证高回报且几乎没有风险的说法，都应视为危险信号。")
        info_card("🚩", "催促立即行动", "制造紧迫感、只开放很短时间、要求保密或让你借钱入场，都是需要暂停和核实的信号。")
    with red_cols[1]:
        info_card("🚩", "社交媒体群荐股/冒充专家", "陌生人可能冒充专业人士、券商或监管机构，也可能先拉高价格再卖出。不要只凭群聊、截图或名人头像作决定。")
        info_card("🚩", "要求先付钱才能提现或追回损失", "所谓解冻费、追回损失费或保证金可能是二次诈骗。不要再给对方提供资金或敏感信息。")

    with st.expander("账户安全与常见行为偏差"):
        st.markdown("""
        **账户安全**

        - 通过官方渠道访问券商网站或 App，不从陌生消息中的链接登录。

        - 在支持的情况下启用多因素验证；使用独立且强的密码，不分享密码、一次性验证码或恢复码。

        - 对“客服”要求远程控制设备、转账到个人账户、提供验证码或支付解冻费的要求保持警惕。

        - 定期查看登录提示、订单记录和账户对账单；发现异常时通过官方渠道联系券商。

        **行为偏差**

        - **害怕错过机会（FOMO）**：看到快速上涨就匆忙追入。

        - **损失厌恶**：亏损时只想等回本，忽略投资理由是否已改变。

        - **确认偏误**：只搜集支持自己观点的消息，忽略反面证据。

        - **过度自信与过度交易**：高估自己预测短期变化的能力，低估费用与错误的累积影响。

        - **沉没成本**：因为已投入很多时间或金钱，就继续坚持一个已不再有理据的决策。

        一个可执行的防护习惯是：投资前写下理由、主要风险、验证来源和何时重新评估；不要只在价格下跌后才临时决定。
        """)
    with st.expander("新手需要知道但不应急着使用的高级工具"):
        st.markdown("""
        - **保证金/杠杆**：借钱或使用衍生工具放大敞口，可能同时放大损失；某些账户还可能被要求追加资金或强制平仓。

        - **卖空**：先借入证券卖出，之后再买回归还；价格上涨时可能产生很大损失，机制也比普通买入复杂。

        - **期权**：合约价值受标的价格、时间、波动率等因素影响；不同策略风险差异很大，部分卖方策略可能有极高或理论上无限损失。

        - **杠杆/反向 ETF**：目标通常针对特定的每日回报倍数或反向表现，长期结果会受每日重置和复利路径影响，不等于简单的长期倍数。

        这些工具不必在入门课程中完全掌握。此阶段的目标是知道它们更复杂、风险更高，不能因为容易在交易软件中点到就贸然使用。
        """)

    scam_answer = st.radio("情境题：某社交媒体群声称可以保证每月高收益，并要求你今天转账才能进入内部股票名单。最稳妥的做法是什么？", [
        "赶快转账，避免错过机会", "暂停行动、核实机构与信息来源，不因承诺或催促作决定", "先投一小笔，稳赚后再追加"], key="scam_practice")
    if st.button("检查防骗判断", key="scam_submit"):
        passed = scam_answer.startswith("暂停行动")
        record_quiz_attempt("风险与投资者保护", passed)
        if passed:
            st.success("正确。保证收益、低风险承诺与催促转账都是典型危险信号，应独立核实并保护个人及账户信息。")
        else:
            st.error("保证收益和紧迫催促都值得警惕。不要因为群聊或陌生人推荐而转账或交易。")
    lesson_completion_button("风险与投资者保护", "finish_investor_protection")


# ============================================================
# Comprehensive final quiz
# ============================================================
elif chosen_page == "综合测验":
    hero("入门综合测验｜把知识连接起来", "24 道进阶情境题覆盖股票基础、K线、技术指标、订单、财报、股价因素与投资者保护。干扰选项围绕课程概念设计；提交后逐题标出正误，并给出对应课程。", "FINAL ASSESSMENT · BEGINNER PATHWAY")
    questions = [
        (
            "一家公司发行普通股，投资者在二级市场买入一股，最准确的描述是什么？",
            ["投资者取得公司的一部分股权，但不因此获得固定还本付息承诺。", "投资者向公司提供有到期日的贷款，公司必须按约定偿还本金。", "投资者取得公司全部资产按持股比例直接分割的所有权。", "投资者只购买一份随指数变化的计量单位，不持有任何证券权益。"],
            0, "普通股代表公司股权的一部分，但不保证股息或资本回报；股东清算分配通常排在债权人之后。", "01 股票市场基础"),
        (
            "关于股票指数与 ETF，下列哪项最精确？",
            ["指数本身通常是一套衡量规则；ETF 是可在交易所交易、可能跟踪该指数的基金产品。", "指数和 ETF 都是基金份额，差别只在交易时间。", "ETF 的价格必定等于其跟踪指数的点位，因此不会有跟踪误差。", "买入 ETF 就消除了所持证券的市场风险，因为基金由多只证券构成。"],
            0, "指数衡量一组证券的表现，不能像普通证券那样直接买入；ETF 是产品，仍可能有市场风险、费用与跟踪误差。", "01 股票市场基础"),
        (
            "A 公司每股 18 美元、已发行在外 60 亿股；B 公司每股 120 美元、已发行在外 10 亿股。仅按市值比较，正确结论是什么？",
            ["A 市值 1,080 亿美元，B 市值 1,200 亿美元，所以 B 的市值较高。", "A 市值较高，因为 A 的股数更多，不需要再乘每股价格。", "B 市值一定比 A 高得多，因为每股价格是 A 的 6.7 倍。", "无法计算市值，除非先知道两家公司的年度营收。"],
            0, "市值的简化计算是每股价格乘以已发行在外股份数。A 为 18×60 亿，B 为 120×10 亿；市值并不等同于企业价值或估值是否便宜。", "01 股票市场基础"),
        (
            "某日 K 线的 Open=50、High=54、Low=47、Close=48，成交量为 800 万股。哪项同时符合这些数据？",
            ["收盘价低于开盘价，价格区间为 7 美元；成交量是该日交易股数的度量。", "收盘价低于开盘价，因此当日最低价必定是 48 美元。", "成交量 800 万股就是当日成交金额为 800 万美元。", "成交量 800 万股表示所有成交都发生在收盘价 48 美元。"],
            0, "High 与 Low 给出该周期内价格区间；Close 低于 Open 表示收盘低于开盘。成交量合计该周期内交易股数，并不等于交易人数，也不只在收盘价成交。", "02 看懂行情"),
        (
            "一只股票当日下跌 2%，成交量约为过去 20 个交易日平均值的两倍。仅凭这两项信息，最可靠的结论是什么？",
            ["市场参与交易更活跃且当日收盘走弱，但不能只据此判断下一个交易日的方向或原因。", "放量下跌已经证明机构投资者正在出货，之后必定继续跌。", "放量下跌说明公司当日公布的利润低于预期。", "成交量翻倍足以确认下跌趋势，即使此前没有下跌或其他背景。"],
            0, "成交量描述交易活跃程度，价格描述当期结果。它们可以提供线索，但不单独证明交易者身份、公司基本面变化或未来方向。", "02 看懂行情"),
        (
            "同样是小实体、较长下影线：若形态出现在一段下跌之后，与出现在一段上涨之后，哪项表述更符合本课程？",
            ["下跌后可能按锤头线解读，上涨后可能按上吊线解读；形状本身不足以确定结果。", "无论此前趋势如何都叫锤头线，因为颜色和影线比例决定名称。", "无论此前趋势如何都代表买方占优，接下来更可能上涨。", "名称由当天成交量是否高于均值决定，不需要观察前面的价格。"],
            0, "锤头线与上吊线的形状相近，传统命名高度依赖此前趋势背景；仍要结合位置和后续价格确认。", "02A 蜡烛图形态学"),
        (
            "看涨吞没形态出现在一段下跌后，附近有先前关注的价格支撑。怎样使用这个形态最审慎？",
            ["把它当作潜在转强线索，再检查趋势背景、后续价格确认、成交量与风险；不把它当成保证上涨的指令。", "因为形态和支撑同时出现，已经足以证明底部形成，可以忽略止损和仓位。", "只要第二根是阳线，形态就有效，不必比较它与前一根实体的关系。", "形态只有在成交量恰好翻倍时才成立，其他信息都不需要。"],
            0, "形态需要符合所用定义，并结合趋势、位置和后续证据。即使多个线索同时出现，也不保证后续走势。", "02A 蜡烛图形态学"),
        (
            "相同周期下，EMA 与简单移动平均线（SMA / MA）的一个主要区别是什么？",
            ["EMA 对近期价格赋予更高权重，因此通常反应更敏感；这也可能增加短期噪声。", "EMA 只使用成交量，不使用价格。", "EMA 能消除所有滞后，并提前知道未来价格。", "两者只在图表颜色上不同，计算完全相同。"],
            0, "EMA 的权重对近期数据更高；SMA 对窗口内各个价格赋予相同权重。更敏感不代表一定更准确。", "02B 技术指标入门"),
        (
            "RSI 已超过 70，而随机指标也进入 80 以上。下列解读哪项最合理？",
            ["两个指标都来自价格数据且信息有所重叠；这说明近期动能 / 区间位置偏高，但不能保证马上反转。", "两个指标同时超过阈值，便可以保证下一交易日下跌。", "这两个数值表示公司市盈率超过行业 70% 和 80%。", "随机指标只衡量成交量，RSI 只衡量波动率，因此它们完全独立。"],
            0, "RSI 与随机指标都是动能振荡指标，但计算侧重点不同；极端读数是参考信息，不是确定的反转时点，也不是两份独立证据。", "02B 技术指标入门"),
        (
            "布林带收窄后价格向上突破上轨，哪项说法最准确？",
            ["这证明波动将继续扩大且方向必然向上。", "这一定是均值回归信号，所以应该立刻卖出。", "带宽收窄描述此前波动收敛；突破可作为观察线索，但方向与持续性仍须后续验证。", "布林带上轨等于市场保证的最高合理价格。"],
            2, "布林带宽度与标准差有关，收窄不预测扩张方向；价格可能沿上轨运行，也可能重新回到带内。", "02B 技术指标入门"),
        (
            "ADX 为 32，且 −DI 高于 +DI。最贴近指标含义的描述是什么？",
            ["ADX 32 表示价格必定上涨 32%。", "趋势强度可能较明显，而 −DI 相对 +DI 更强，提供偏向下行的方向线索；两者均不能单独保证未来。", "ADX 只在股价上涨时增加，因此方向必定向上。", "OBV 与成交量数据可以忽略，因为 ADX 会直接测量买卖人数。"],
            1, "ADX 衡量趋势强度，不独立给出涨跌方向；+DI 与 −DI 做方向性比较。阈值属于经验参考，且计算有滞后。", "02B 技术指标入门"),
        (
            "你想尽快建立一笔股票仓位，且优先考虑尽快成交，而不是把最高买入价锁定在某个数值。哪项订单思路最吻合？",
            ["市价单：强调尽快执行，但成交价格可能与提交时看到的报价不同。", "买入限价单：强调尽快成交，因此一定会按当时卖价成交。", "止损单：一旦设置，就能同时保证成交和成交价格。", "买入限价单：只要市场价格高于限价，系统就会自动把它改成市价单。"],
            0, "市价单通常优先争取执行速度，但不能保证价格；限价单提供价格控制，却可能不成交。止损单的触发与执行规则也不等于价格保证。", "03 交易如何执行"),
        (
            "最佳卖价是 101.20 美元，最佳买价是 101.05 美元。你提交一张买入限价单，限价为 100.80 美元。通常最可能发生什么？",
            ["订单暂时未成交；买入限价低于当前最佳卖价，只有市场条件变化并出现可接受的卖价时才可能成交。", "只要最近成交价跌到 100.80 美元，订单就一定会立即全数成交，即使当时最佳卖价更高。", "订单按 101.20 美元成交，因为限价只是报价参考，不会限制买入价格。", "订单可限制价格，但不会因买入限价低于当前卖价就自动提高限价。"],
            0, "买入限价单通常不会以高于限价的价格买入；在当前报价下它不是可立即成交的买单。但限价单不保证成交，具体规则也应查看券商说明。", "03 交易如何执行"),
        (
            "某股票最佳买价为 49.95 美元、最佳卖价为 50.10 美元。下列哪项判断准确？",
            ["买卖价差为 0.15 美元；价差是即时交易成本和流动性观察线索之一，但不能单独说明未来涨跌。", "买卖价差为 0.15 美元；这也表示股票当天的最高价与最低价只差 0.15 美元。", "买卖价差为 50.10 美元；最佳买价只用于显示昨天收盘价。", "买卖价差越窄，股票的市场风险就必然越低，未来回报也越高。"],
            0, "买卖价差通常是最佳卖价减最佳买价。较窄价差可能降低即时交易成本，但并不能保证价格稳定或投资风险较低。", "03 交易如何执行"),
        (
            "你想分别查明一家公司的年度营收与费用、12 月 31 日的资产和负债、以及全年现金的流入流出。三类信息应优先查哪张报表？",
            ["损益表；资产负债表；现金流量表。", "现金流量表；损益表；资产负债表。", "资产负债表；现金流量表；损益表。", "三者都只能从损益表直接读取，因为其他报表是附注。"],
            0, "损益表描述一段期间的经营表现；资产负债表显示某一时点的资产、负债与权益；现金流量表解释现金流入和流出。", "04 研究一家公司"),
        (
            "公司营收同比增加 25%，净利润也增加，但经营现金流转负，应收账款和存货同时上升。下一步最有针对性的检查是什么？",
            ["检查现金流量表、应收账款与存货变化、收入确认及相关附注，判断增长是否转化成现金以及营运资金为何增加。", "只要净利润增长，经营现金流就可以忽略，因为利润与现金在财报中完全相同。", "直接认定收入是虚假的，因为任何应收账款增长都表示客户不会付款。", "只看股价在当天是否上涨，就能确定营收增长的质量。"],
            0, "营收和会计利润不等于现金已经收到。应收账款、存货、资本开支和其他营运资金变化都可能影响现金流，需要结合报表和附注核实。", "04 研究一家公司"),
        (
            "一家公司股价为 40 美元、过去一年每股收益 EPS 为 2 美元。若使用简单的历史市盈率计算，下列哪项最准确？",
            ["P/E 为 20 倍；它描述股价相对于每股收益的倍数，本身不能单独证明股票便宜或昂贵。", "P/E 为 0.05 倍；用 EPS 除以股价后得到的比率就是通常所说的市盈率。", "P/E 为 20 倍；因此投资者可以据此确定恰好 20 年后收回成本。", "P/E 为 20 倍；单看这个倍数就足以判断它比同行便宜。"],
            0, "简化历史 P/E = 股价 ÷ EPS = 40 ÷ 2 = 20。估值还要比较增长、行业、风险、盈利质量和未来预期；它不是回本保证。", "04 研究一家公司"),
        (
            "某公司发布财报：营收同比增长 40%，股价却下跌。哪项解释与本课程最一致？",
            ["股价会对比实际结果与市场预期，也会反映未来指引、利润率、风险和其他市场因素；同比增长不保证上涨。", "只要营收同比增长，股价下跌就证明市场价格错误。", "股价下跌说明公司营收增长数字一定是假的。", "财报只影响公司长期价值，不可能影响短期市场预期或股价。"],
            0, "市场反应不只取决于增长是否为正，也取决于增长是否超出预期、未来展望以及当时市场和行业背景。", "05 股价为什么变化"),
        (
            "历史波动率是根据过去一段时间的收益变化估算出来的。它最适合被理解为哪项指标？",
            ["过去收益起伏程度的统计描述，不是未来最大损失上限，也不是上涨概率。", "未来某个日期价格的精确预测，波动率越高预测越准确。", "在任何市场环境下都不会被突破的最大亏损比例。", "衡量公司资产负债表中短期债务占比的财务指标。"],
            0, "本课程用日收益率的标准差估算历史波动率，并可用 √252 做年化近似。它来自历史数据，不能保证未来风险上限。", "投资者保护"),
        (
            "一项资产先从历史高点 100 跌到 72，之后回升至 90。以该高点之后的低点计算，最大回撤是多少？",
            ["28%，因为从 100 到 72 的跌幅是 28%；后来回升并不会抹掉此前已经发生的回撤。", "10%，因为最终价格 90 比起点 100 低 10%，因此最大回撤也只有 10%。", "72%，因为低点价格占高点的 72%。", "无法计算，因为最大回撤只看全年最后一天的收盘价。"],
            0, "最大回撤关注从此前高点到之后低点的最大跌幅：(72÷100)-1 = -28%。它描述路径中的下跌，不只是期末净变化。", "投资者保护"),
        (
            "一个组合持有 AAPL、MSFT、NVDA 和跟踪纳斯达克 100 的 QQQ。关于分散程度，哪项最合理？",
            ["虽然有四个代码，但大型科技股及 QQQ 成分重叠可能带来共同风险；应检查权重、行业和持仓重叠。", "四个不同代码代表四种独立风险来源，所以已经充分分散。", "只要每个代码权重不超过 25%，就不必再考虑相关性。", "因为其中包含 ETF，组合就不会受到科技行业或整体市场下跌影响。"],
            0, "分散不只取决于证券数量，也取决于行业、相关性、成分重叠与各资产权重。ETF 本身也可能持有同一批大盘科技股。", "投资者保护"),
        (
            "你下个月必须支付学费，这笔钱没有其他替代来源。把它投入波动较大的单只股票，最关键的问题是什么？",
            ["短期资金没有足够时间等待回撤后的恢复；一旦下跌，可能被迫在不利时点卖出。", "只要选过去一年涨幅最高的股票，资金使用期限就不再重要。", "只要分几次买入，就能消除短期下跌风险，不必预留其他可用现金。", "股票通常可以交易，所以预定支出日期不会受市场价格或流动性影响。"],
            0, "资金的用途与时间期限应匹配资产风险；近期必须支出的资金承受回撤和等待恢复的空间较小。", "投资者保护"),
        (
            "一个社交媒体投资群宣传每月稳定高回报，声称名额今天截止，并要求把钱转入个人账户。最安全的第一步是什么？",
            ["暂停转账，独立核实机构、人员、平台及信息来源；不要因保证回报或紧迫感仓促行动。", "先转一小笔测试，因为小额转账能证明投资项目真实。", "让群主提供一张盈利截图；只要截图上的账户余额真实就可以信任。", "赶在截止前转账，之后再通过证券代码核对公司是否上市。"],
            0, "保证高回报、制造紧迫感、要求转到个人账户等都属于危险信号。不要只依赖群聊截图或陌生人提供的链接。", "06 风险与投资者保护"),
        (
            "你要核实一家美国上市公司的年度财务申报。关于 SEC EDGAR，哪项理解正确？",
            ["EDGAR 是查找美国上市公司公开申报文件的官方入口；文件可供核实，但提交文件不代表 SEC 推荐或保证该公司安全。", "一家公司能在 EDGAR 搜到，就代表 SEC 已审查并保证它不会欺诈或破产。", "EDGAR 只显示社交媒体文章，不包含公司正式申报文件。", "如果公司已经发布新闻稿，就无需再核对正式申报文件和附注。"],
            0, "SEC EDGAR 提供公司申报文件的查询入口，是研究的一手来源之一；使用者仍要自行阅读、交叉核实和评估风险。", "06 风险与投资者保护"),
    ]
    # Move correct options into a balanced, non-obvious order so the answer key is not always A.
    target_positions = [2, 0, 3, 1, 0, 2, 1, 3, 2, 0, 3, 1, 2, 1, 0, 3, 1, 2, 0, 3, 1, 3, 0, 2]
    reordered_questions = []
    for item, target in zip(questions, target_positions):
        question_text, options, original_correct, explanation, lesson = item
        correct_option = options[original_correct]
        distractors = [option for idx, option in enumerate(options) if idx != original_correct]
        distractors.insert(target, correct_option)
        reordered_questions.append((question_text, distractors, target, explanation, lesson))
    questions = reordered_questions

    with st.form("final_comprehensive_quiz_form"):
        answers: list[int | None] = []
        for i, q in enumerate(questions):
            st.markdown(f'<div class="section-kicker">QUESTION {i+1:02d} / {len(questions):02d} · {escape(q[4])}</div><div style="font-size:1.02rem;font-weight:750;color:#f3f7fc;margin:.25rem 0 .7rem">{escape(q[0])}</div>', unsafe_allow_html=True)
            answer = st.radio("选择答案", q[1], key=f"comprehensive_answer_{i}", index=None, label_visibility="collapsed")
            answers.append(q[1].index(answer) if answer is not None else None)
            st.markdown("<hr style='margin:.8rem 0 1.2rem'>", unsafe_allow_html=True)
        submitted = st.form_submit_button("提交测验并查看逐题结果", width="stretch")
    if submitted:
        if any(answer is None for answer in answers):
            st.warning(f"还有 {sum(answer is None for answer in answers)} 题未作答。请完成全部 24 题后再提交。")
        else:
            score = sum(answer == q[2] for answer, q in zip(answers, questions))
            st.session_state["comprehensive_quiz_result"] = {"score": score, "answers": answers}
            record_quiz_attempt("综合测验", score >= 20)
    result = st.session_state.get("comprehensive_quiz_result")
    if result:
        score = result["score"]
        required_score = 20  # At least 80% of 24 questions, rounded up.
        st.metric("你的得分", f"{score}/{len(questions)}", f"{score / len(questions) * 100:.0f}%")
        if score >= required_score:
            st.success("通过！你已达到本套进阶检查的 80% 标准。请继续把概念应用到真实资料中；通过测验不代表可以确定预测市场。")
            if st.button("✓ 完成综合测验", key="comprehensive_quiz_complete"):
                mark_complete("综合测验")
                st.success("已记录测验完成状态。")
        else:
            st.info(f"当前未达到 {required_score}/{len(questions)} 分。建议按红色错题的对应课程复习后，再重新作答。")
        st.markdown("### 逐题结果｜绿色为答对，红色为答错")
        for i, q in enumerate(questions):
            render_final_answer_review(i + 1, q[0], q[1], int(result["answers"][i]), q[2], q[3], q[4])
        st.button("重新开始 24 题测验", key="comprehensive_quiz_retry", on_click=reset_comprehensive_quiz)

# ============================================================
# Data and methodology
# ============================================================
elif chosen_page == "数据与方法":
    hero("数据与方法｜看得懂，也要查得清", "学习网站使用真实历史市场数据作为互动材料，并公开说明变量定义、计算方法与局限。", "DATA NOTES · TRANSPARENCY")
    c1, c2 = st.columns(2)
    with c1:
        info_card("🗂️", "数据结构", "日线数据包括日期、证券代码、开盘价、最高价、最低价、收盘价和成交量。多只证券与多个交易日构成多变量数据集。", "7 个字段")
    with c2:
        info_card("🧮", "指标定义", "历史收益率由区间首末有效收盘价计算；年化波动率以日收益率标准差乘以 √252 估算；最大回撤是价格相对历史峰值的最大跌幅。", "可复核口径")

    section_heading("CURRICULUM SCOPE", "本课程覆盖哪些基础知识？")
    st.markdown("""
    课程按新手路径覆盖：

    1. 股票、债券、指数、ETF、股息、市值、交易所与券商基础；

    2. OHLC、K 线、蜡烛图形态、成交量、报价、时间周期与调整价格；

    3. 技术指标的用途与局限，包括 MA / EMA、RSI、MACD、布林带、随机指标、ADX、OBV，以及支撑阻力和斐波那契回撤等价格位置工具；

    4. 市价单、限价单、止损单、买卖价差、流动性、费用、有效期、成交与结算的概念；

    5. 损益表、资产负债表、现金流量表、营收、利润、EPS、P/E、利润率、债务和公司申报资料；

    6. 公司、行业、宏观、市场预期与流动性等股价影响因素；

    7. 价格回报与总回报、复利、基准、波动率、最大回撤、通胀、汇率和费用影响；


    8. 投资者自我保护、社交媒体荐股诈骗、账户安全、常见行为偏差及高级产品风险提醒。

    **课程范围：** 本课聚焦股票投资入门。当地税务、交易规则和产品条款请查阅官方文件；卖空、保证金、期权、期货和杠杆产品仅介绍主要风险。
    """)

    section_heading("DATA SOURCE", "来源与使用限制")
    st.markdown("""
    - **原型行情来源：** Python 包 `yfinance` 获取 Yahoo Finance 提供的历史行情数据。
    - **重要提醒：** `yfinance` 是第三方工具，不代表 Yahoo 官方认可的开放 API；可以下载数据并不等于取得公开再分发授权。
    - **课程合规：** Track 1 要求使用开放 API 或可验证的开放数据集。正式提交前，请和课程老师确认 Yahoo Finance 数据是否被接受，或换用许可条款更明确的数据源。
    - **调整价格：** `auto_adjust=True` 的日线 OHLC 经过调整，适合历史价格表现分析；数据定义、缺失值和公司行动仍应留意。
    - **蜡烛图形态专题：** 形态图库中的 K 线使用合成 OHLC 数值，仅用于说明结构；首页 01 情景题与真实市场练习使用从 Yahoo Finance 获取的历史 OHLCV。首页 01 固定观察 2024-11-01 至 2024-12-01 的 NVDA 日线，暂时隐藏截至 2024-11-21 之后的五个交易日，提交后才显示后续数据。形态比例与名称在不同教材中可能不同，本项目采用常见教学定义，不把它们当成确定性预测。
    - **首页 02 财报案例：** NVIDIA 官方于 2024-11-20 公布的 2025 财年第三季度业绩数据；页面注明公告链接与日期。该例子用于说明强劲同比增长并不自动决定股价方向。
    - **交易功能：** 本站用于教学与历史数据探索，不连接券商，也不会提交真实订单。
    """)
    with st.expander("教学结构参考与延伸学习"):
        st.markdown("""
        本项目借鉴 IBKR Campus / Traders’ Academy 的公开课程组织方式，而非复制其课程内容：
        - 按新手路径安排模块，先讲股票与 ETF 基础，再逐步进入市场结构、研究、风险和实践。
        - 把每课组织为概念讲解、实例、互动探索与知识检查。
        - 允许重复尝试练习，并把课程完成度与知识检查分开显示。

        本站的中文说明和案例均为本项目独立编写，不代表 IBKR 官方课程或建议。

        **IBKR 官方参考：** [Traders’ Academy 课程目录](https://www.interactivebrokers.com/campus/traders-academy/finance-courses/) · [Introduction to Stocks](https://www.interactivebrokers.com/campus/trading-course/intro-to-stocks/) · [学习进度与测验](https://www.interactivebrokers.com/campus/about-academy-quizzes/)
        """)
    with st.expander("官方学习资料与核实渠道"):
        st.markdown("""
        - [Investor.gov：投资入门、风险、复利与分散投资](https://www.investor.gov/introduction-investing)

        - [Investor.gov：订单类型](https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/types-orders)


        - [Investor.gov：常见投资骗局](https://www.investor.gov/additional-resources/spotlight/common-scams)

        - [SEC EDGAR：美国上市公司公开申报](https://www.sec.gov/edgar/search/)

        这些资料主要面向美国市场；其他地区的券商资格、税务、交易规则、结算和投资者保护安排可能不同，应咨询当地官方监管机构并查看具体券商文件。
        """)
    method_period = st.selectbox("生成可下载的数据集", list(PERIODS.keys()), index=4, format_func=lambda x: PERIODS[x], key="method_period")
    method_symbols = st.multiselect("选择数据代码", list(TICKERS.keys()), default=["AAPL", "MSFT", "NVDA", "SPY", "QQQ"], format_func=ticker_label, key="method_symbols")
    if st.button("获取并整理数据", key="method_fetch"):
        method_data, method_error = safe_prices(method_symbols, method_period)
        st.session_state["method_data"] = method_data
        st.session_state["method_error"] = method_error
    method_data = st.session_state.get("method_data", pd.DataFrame())
    if st.session_state.get("method_error"):
        show_data_warning(st.session_state["method_error"])
    if isinstance(method_data, pd.DataFrame) and not method_data.empty:
        s1, s2, s3 = st.columns(3)
        s1.metric("数据行数", f"{len(method_data):,}")
        s2.metric("证券数量", f"{method_data['ticker'].nunique()}")
        s3.metric("字段数量", f"{method_data.shape[1]}")
        st.dataframe(method_data.head(30), width="stretch", hide_index=True)
        st.download_button("下载清洗后的 CSV", method_data.to_csv(index=False).encode("utf-8-sig"), file_name="stockscope_cleaned_daily_prices.csv", mime="text/csv")


# Footer
st.markdown("---")
st.caption("StockScope Learn · 股票投资基础课程原型。历史行情可能延迟、缺失或修订；历史表现不代表未来结果。公开发布前需确认数据使用与再分发授权。")

# Auto-scroll is deliberately reserved for a real main-navigation change.
# Changing the selected candle pattern never triggers a scroll-to-top action.
if _page_changed:
    scroll_main_to_top(f"page:{st.session_state.get('_scroll_sequence', 0)}:{chosen_page}")
