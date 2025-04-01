import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")
st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Full Bias Checklist – Version 1.1")

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
# 1. Day-of-Week Bias
# -----------------------
def day_of_week_bias_score():
    today = datetime.today().strftime('%A')
    favorable_days = ['Tuesday', 'Wednesday', 'Thursday']
    score = 1 if today in favorable_days else 0
    return score, today

score1, today = day_of_week_bias_score()
st.subheader("1. Day-of-Week Bias")
st.write(f"Today is **{today}** — Score: {score1}/1")

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
st.write(f"Range: {pd_range} | Score: {score2}/1")

# -----------------------
# 3–6. Manual Inputs with Tick/X
# -----------------------
st.subheader("3–6. Visual Bias Components")

col1, col2 = st.columns(2)

with col1:
    is_structure = st.checkbox("✅ Price Near Breakout Structure", value=False)
    score3 = 1 if is_structure else 0
    st.markdown(f"Score: {score3}/1")

    is_fib = st.checkbox("✅ In 38.2–61.8% Fib Zone", value=False)
    score5 = 1 if is_fib else 0
    st.markdown(f"Score: {score5}/1")

with col2:
    is_ema = st.checkbox("✅ EMA Alignment Bullish (1H/4H/Daily)", value=False)
    score4 = 1 if is_ema else 0
    st.markdown(f"Score: {score4}/1")

    is_wave = st.checkbox("✅ Bullish Elliott Wave Likely Forming", value=False)
    score6 = 1 if is_wave else 0
    st.markdown(f"Score: {score6}/1")

# -----------------------
# Total Bias Score
# -----------------------
total_score = score1 + score2 + score3 + score4 + score5 + score6
st.subheader("Total Bias Score")
st.metric(label="Bias Strength", value=f"{total_score}/6")

# -----------------------
# Interpretation
# -----------------------
if total_score >= 5:
    st.success("High Bullish Bias – Look for Entry Setup")
elif total_score >= 3:
    st.warning("Moderate Bias – Entry May Need Confirmation")
else:
    st.error("Low Bias – Avoid Entry or Wait")
