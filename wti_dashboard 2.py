import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")
st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Directional Bias Checklist – Version 1.9")

# -----------------------
# Get Live WTI Daily Data
# -----------------------
symbol = "CL=F"
daily_data = yf.download(tickers=symbol, period="7d", interval="1d", progress=False)

if len(daily_data) < 2:
    st.error("Insufficient daily WTI data. Try again later.")
    st.stop()

# Prepare daily data
daily_data.reset_index(inplace=True)
daily_data = daily_data[["Date", "High", "Low"]].dropna().tail(2)
df = daily_data.copy()

st.subheader("OHLC Data (Last 2 Days)")
st.dataframe(df)

# -----------------------
# Live Price
# -----------------------
live_price = round(yf.Ticker(symbol).info.get("regularMarketPrice", 0), 2)
st.subheader("Live WTI Price")
st.write(f"**{live_price} USD**")

# -----------------------
# 1. Day-of-Week Bias
# -----------------------
def day_of_week_bias_score():
    today = datetime.today().strftime('%A')
    favorable_days = ['Tuesday', 'Wednesday', 'Thursday']
    score = 1 if today in favorable_days else 0
    return score, today

score1, today = day_of_week_bias_score()
st.subheader("1. Day-of-Week Bias")
st.write(f"Today is **{today}**")
st.write(f"Score: {score1}/1")

# -----------------------
# 2. Prior Day’s Range
# -----------------------
def prior_day_range_score(df, threshold=0.80):
    try:
        if len(df) < 2:
            return 0, 0
        high = float(df['High'].iloc[-2])
        low = float(df['Low'].iloc[-2])
        range_pips = abs(high - low)
        score = 1 if range_pips < threshold else 0
        return score, round(range_pips, 2)
    except:
        return 0, 0

score2, pd_range = prior_day_range_score(df)
st.subheader("2. Prior Day’s Range")
st.write(f"Range: {pd_range}")
st.write(f"Score: {score2}/1")

# -----------------------
# 3. Breakout Structure Score
# -----------------------
def breakout_structure_score(df, current_price, tolerance=0.20):
    try:
        if len(df) < 2:
            return 0, "Data Error", 0, 0
        high = float(df['High'].iloc[-2])
