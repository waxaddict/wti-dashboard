import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")
st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Directional Bias Checklist – Version 1.6 (Live Price Enabled)")

# -----------------------
# Get Live WTI Price
# -----------------------
wti_symbol = "CL=F"  # Crude Oil Futures (NYMEX)
wti_data = yf.download(tickers=wti_symbol, period="2d", interval="1d", progress=False)

if wti_data.empty:
    st.error("Unable to fetch live WTI data.")
    st.stop()

wti_data.reset_index(inplace=True)
wti_data = wti_data.rename(columns={"High": "High", "Low": "Low"})
df = wti_data[["Date", "High", "Low"]]

# -----------------------
# Display OHLC Data
# -----------------------
st.subheader("OHLC Data (Last 2 Days)")
st.dataframe(df)

# -----------------------
# Get Latest Price (Live)
# -----------------------
live_price = round(yf.Ticker(wti_symbol).info.get("regularMarketPrice", 0), 2)
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
        high = df['High'].iloc[-2]
        low = df['Low'].iloc[-2]
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
        high = df['High'].iloc[-2]
        low = df['Low'].iloc[-2]
        near_high = abs(current_price - high) <= tolerance
        near_low = abs(current_price - low) <= tolerance
        near_structure = near_high or near_low
        score = 1 if near_structure else 0
        position = "High" if near_high else "Low" if near_low else "None"
        return score, position, high, low
    except:
        return 0, "Error", 0, 0

score3, structure_side, high, low = breakout_structure_score(df, live_price)
st.subheader("3. Price Near Breakout Structure")
st.write(f"Yesterday's High: {high} | Low: {low}")
st.write(f"Near Structure: **{structure_side}**")
st.write(f"Score: {score3}/1")

# -----------------------
# 4–6. Bias Conditions (Manual Logic)
# -----------------------
st.subheader("4–6. Bias Conditions (Defined by Logic or Manual Entry)")

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
# Wave Structure Overview (Manual)
# -----------------------
st.subheader("Wave Structure Overview")

st.markdown("""
Multi-timeframe view of where WTI may sit within Elliott Wave structure.  
These can be adjusted based on your interpretation of chart structure.
""")

wave_2h = "Wave 4"
wave_4h = "Wave 3"
wave_daily = "Wave 1"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="2H Chart", value=wave_2h)
with col2:
    st.metric(label="4H Chart", value=wave_4h)
with col3:
    st.metric(label="Daily Chart", value=wave_daily)
