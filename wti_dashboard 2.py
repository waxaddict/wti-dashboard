import yfinance as yf
import pandas as pd

# -----------------------
# SETTINGS
# -----------------------
symbol = "CL=F"  # WTI Crude Oil Futures
window = 6       # # of 2H candles to define an impulse leg (~12 hours)

# -----------------------
# DOWNLOAD 2H DATA
# -----------------------
data = yf.download(tickers=symbol, period="30d", interval="2h", progress=False)

# -----------------------
# CLEAN DATA
# -----------------------
data = data[['High', 'Low', 'Close']].dropna().reset_index()
if len(data) < window + 1:
    raise ValueError("Not enough 2H data to detect impulse.")

# -----------------------
# DETECT IMPULSE LEG
# -----------------------
data['change'] = data['Close'].diff()
data['abs_change'] = data['change'].abs()
data['rolling_sum'] = data['change'].rolling(window).sum()

impulse_idx = data['rolling_sum'].idxmax()
impulse_start_idx = impulse_idx - window + 1
impulse_end_idx = impulse_idx

wave1_low = data.loc[impulse_start_idx, 'Low']
wave1_high = data.loc[impulse_end_idx, 'High']

# -----------------------
# FIB RETRACEMENT LEVELS
# -----------------------
fib_382 = wave1_high - (wave1_high - wave1_low) * 0.382
fib_618 = wave1_high - (wave1_high - wave1_low) * 0.618

# -----------------------
# CURRENT PRICE & STATUS
# -----------------------
current_price = data['Close'].iloc[-1]
in_wave_2 = fib_618 <= current_price <= fib_382
wave_status = "Likely Wave 2" if in_wave_2 else "Impulse Complete or Waiting"

# -----------------------
# OUTPUT RESULTS
# -----------------------
print("\nWTI 2H Wave Detection")
print("----------------------------")
print(f"Wave 1 Range         : {round(wave1_low, 2)} → {round(wave1_high, 2)}")
print(f"Fib Entry Zone (2H)  : {round(fib_618, 2)} → {round(fib_382, 2)}")
print(f"Current Price        : {round(current_price, 2)}")
print(f"Wave Label           : {wave_status}")
