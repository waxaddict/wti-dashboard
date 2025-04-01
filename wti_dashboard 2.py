import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")
st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Directional Bias Checklist – Version 1.4")

# -----------------------
# Sample OHLC Data (Last 2 Days)
# -----------------------
st.subheader("Sample OHLC Data (Last 2 Days)")

data = {
    "Date": pd.date_range(end=datetime.today(), periods=2),
    "High": [70.30, 71.60],
    "Low": [69.80, 70.90],
}
df = pd.DataFrame(data)
st.dataframe(df)

# -----------------------
# Current Price (can be replaced with live input later)
# -----------------------
current_price = 71.40
st.subheader("Current Price")
st.write(f"**{current_price}**")

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
        return
