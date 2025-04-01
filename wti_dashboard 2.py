import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")
st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Directional Bias Checklist – Version 2.1")

# -----------------------
# Get Live WTI Daily Data
# -----------------------
symbol = "CL=F"
daily_data = yf.download(tickers=symbol, period="7d", interval="1d", progress=False)

if len(daily_data) < 2:
    st.error("Insufficient daily WTI data. Try again later.")
    st.stop()

daily_data.reset_index(inplace=True)
daily_data = daily_data[["Date", "High", "Low"]].dropna().tail(2)
df = daily_data.copy()

st.subheader("OHLC Data (Last 2 Days)")
st.dataframe(df)

# -----------------------
# Live WTI Price
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
    except Exception:
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
        low = float(df['Low'].iloc[-2])
        near_high = abs(current_price - high) <= tolerance
        near_low = abs(current_price - low) <= tolerance
        position = "High" if near_high else "Low" if near_low else "None"
        score = 1 if near_high or near_low else 0
        return score, position, high, low
    except Exception:
        return 0, "Error", 0, 0

score3, structure_side, high, low = breakout_structure_score(df, live_price)
st.subheader("3. Price Near Breakout Structure")
st.write(f"Yesterday's High: {high} | Low: {low}")
st.write(f"Near Structure: **{structure_side}**")
st.write(f"Score: {score3}/1")

# -----------------------
# 4–6. Bias Conditions (Manual)
# -----------------------
st.subheader("4–6. Bias Conditions (Manual Logic)")

condition_4 = "Yes"  # EMA Alignment Bullish
condition_5 = "No"   # In Fib Zone
condition_6 = "Yes"  # Bullish Elliott Wave

score4 = 1 if condition_4 == "Yes" else 0
score5 = 1 if condition_5 == "Yes" else 0
score6 = 1 if condition_6 == "Yes" else 0

st.write(f"4. EMA Alignment Bullish: **{condition_4}** — Score: {score4}/1")
st.write(f"5. In 38.2–61.8% Fib Zone: **{condition_5}** — Score: {score5}/1")
st.write(f"6. Bullish Elliott Wave Likely Forming: **{condition_6}** — Score: {score6}/1")

# -----------------------
# Total Bias Score
# -----------------------
total_score = score1 + score2 + score3 + score4 + score5 + score6
st.subheader("Total Bias Score")
st.metric(label="Bias Strength", value=f"{total_score}/6")

if total_score >= 5:
    st.success("High Bullish Bias – Look for Entry Setup")
elif total_score >= 3:
    st.warning("Moderate Bias – Entry May Need Confirmation")
else:
    st.error("Low Bias – Avoid Entry or Wait")

# -----------------------
# 2H Wave Detection (Debug Mode)
# -----------------------
st.subheader("2H Wave Detection (Automated – Debug Mode)")

wave_status = "Unavailable"

try:
    data_2h = yf.download(tickers=symbol, period="21d", interval="2h", progress=False)
    data_2h = data_2h[['High', 'Low', 'Close']].dropna().reset_index()
    st.write(f"Fetched {len(data_2h)} candles from 2H feed.")

    if len(data_2h) < 10:
        st.warning("Not enough candles for detection.")
    else:
        window = 6
        data_2h['change'] = data_2h['Close'].diff()
        data_2h['rolling_sum'] = data_2h['change'].rolling(window).sum()

        impulse_idx = data_2h['rolling_sum'].idxmax()
        st.write(f"Impulse Index: {impulse_idx}")

        if impulse_idx < window:
            st.warning("Impulse leg is too early in the dataset.")
        else:
            impulse_start_idx = impulse_idx - window + 1
            impulse_end_idx = impulse_idx
            st.write(f"Impulse Leg: {impulse_start_idx} to {impulse_end_idx}")

            wave1_low = data_2h.loc[impulse_start_idx, 'Low']
            wave1_high = data_2h.loc[impulse_end_idx, 'High']

            fib_382 = wave1_high - (wave1_high - wave1_low) * 0.382
            fib_618 = wave1_high - (wave1_high - wave1_low) * 0.618

            current_price_2h = data_2h['Close'].iloc[-1]
            st.write(f"Fib Zone: {round(fib_618, 2)} to {round(fib_382, 2)}")
            st.write(f"Current Price: {round(current_price_2h, 2)}")

            in_wave_2 = fib_618 <= current_price_2h <= fib_382
            wave_status = "Likely Wave 2" if in_wave_2 else "Impulse Complete / Waiting"
            st.write(f"Wave Status: {wave_status}")

except Exception as e:
    st.warning(f"Wave detection failed: {e}")

# -----------------------
# Wave Structure Overview
# -----------------------
st.subheader("Wave Structure Overview")

wave_4h = "Wave 3"
wave_daily = "Wave 1"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="2H Chart", value=wave_status)
with col2:
    st.metric(label="4H Chart", value=wave_4h)
with col3:
    st.metric(label="Daily Chart", value=wave_daily)
