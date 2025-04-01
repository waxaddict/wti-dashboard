import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="WTI 100-Pip Bullish Signal Dashboard", layout="centered")

st.title("WTI 100-Pip Bullish Signal Dashboard")
st.markdown("Version 1.0 – Includes Candle Momentum Spike Metric")

# -----------------------
# Sample OHLC Data (Replace with API or upload later)
# -----------------------
st.subheader("Sample OHLC Data (Last 11 Days)")

data = {
    "Date": pd.date_range(end=datetime.today(), periods=11),
    "Open": [68.10, 68.95, 69.00, 69.70, 70.10, 69.90, 70.30, 70.80, 71.10, 70.90, 71.60],
    "Close": [68.95, 69.00, 69.70, 70.10, 69.90, 70.30, 70.80, 71.10, 70.90, 71.60, 71.40],
}
df = pd.DataFrame(data)
st.dataframe(df)

# -----------------------
# Candle Momentum Spike Function
# -----------------------
def candle_momentum_score(df, window=10, multiplier=1.5):
    """
    Calculates if the most recent candle shows a momentum spike based on body size.
    """
    df['body_size'] = abs(df['Close'] - df['Open'])

    avg_body = df['body_size'].iloc[-(window+1):-1].mean()
    current_body = df['body_size'].iloc[-1]

    score = 1 if current_body >= multiplier * avg_body else 0
    status = "Yes" if score == 1 else "No"

    return score, current_body, avg_body, status

def day_of_week_bias_score():
    """
    Scores 1 if today is Tuesday, Wednesday, or Thursday.
    """
    today = datetime.today().strftime('%A')
    favorable_days = ['Tuesday', 'Wednesday', 'Thursday']
    score = 1 if today in favorable_days else 0
    return score, today

# -----------------------
# Output: Candle Momentum Spike
# -----------------------
st.subheader("Candle Momentum Spike")

# -----------------------
# Day-of-Week Bias Section
# -----------------------
st.subheader("Day-of-Week Bias")

day_score, today = day_of_week_bias_score()
status = "Favorable" if day_score == 1 else "Unfavorable"

st.metric(label="Today", value=today)
st.write(f"Bias Status: {status}")
st.write(f"Score: {day_score}/1")

try:
    score, current_body, avg_body, status = candle_momentum_score(df)
    st.metric(label="Momentum Spike Detected", value=status)
    st.write(f"Current Body: {round(current_body, 2)} | Avg Body (last 10): {round(avg_body, 2)}")
    st.write(f"Score: {score}/1")
except Exception as e:
    st.error(f"Could not calculate momentum spike: {e}")

# -----------------------
# Future Checklist Area
# -----------------------
st.subheader("WTI Checklist (Coming Soon)")

st.markdown("""
- [ ] Prior day’s range  
- [ ] Fib retracement zone  
- [ ] EMA alignment  
- [ ] Wave count snapshot  
- [ ] Volume spike  
""")
