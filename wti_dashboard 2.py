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
        return 0, 0

score2, pd_range = prior_day_range_score(df)
st.subheader("2. Prior Day’s Range")
st.write(f"Range: {pd_range}")
st.write(f"Score: {score2}/1")

# -----------------------
# 3. Breakout Structure Score (Automated)
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

score3, structure_side, high, low = breakout_structure_score(df, current_price)
st.subheader("3. Price Near Breakout Structure")
st.write(f"Yesterday's High: {high} | Low: {low}")
st.write(f"Near Structure: **{structure_side}**")
st.write(f"Score: {score3}/1")

# -----------------------
# 4–6. Fixed YES/NO Based on Your Backend Logic
# -----------------------
st.subheader("4–6. Bias Conditions (Fixed Values)")

# --- Update these manually or via logic later
condition_4 = "Yes"  # EMA Alignment Bullish
condition_5 = "No"   # In Fib Zone
condition_6 = "Yes"  # Bullish Wave Forming

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

# -----------------------
# Interpretation
# -----------------------
if total_score >= 5:
    st.success("High Bullish Bias – Look for Entry Setup")
elif total_score >= 3:
    st.warning("Moderate Bias – Entry May Need Confirmation")
else:
    st.error("Low Bias – Avoid Entry or Wait")
