import yfinance as yf
import pandas as pd

st.subheader("2H Wave Detection (Automated)")

# Pull 2H WTI data
symbol = "CL=F"
window = 6
lookback_period = "21d"

try:
    data = yf.download(tickers=symbol, period=lookback_period, interval="2h", progress=False)
    data = data[['High', 'Low', 'Close']].dropna().reset_index()

    if len(data) < window + 1:
        st.warning("Not enough 2H candles to detect an impulse leg. Try a longer time period.")
    else:
        data['change'] = data['Close'].diff()
        data['rolling_sum'] = data['change'].rolling(window).sum()

        impulse_idx = data['rolling_sum'].idxmax()
        impulse_start_idx = impulse_idx - window + 1
        impulse_end_idx = impulse_idx

        wave1_low = data.loc[impulse_start_idx, 'Low']
        wave1_high = data.loc[impulse_end_idx, 'High']

        fib_382 = wave1_high - (wave1_high - wave1_low) * 0.382
        fib_618 = wave1_high - (wave1_high - wave1_low) * 0.618

        current_price = data['Close'].iloc[-1]
        in_wave_2 = fib_618 <= current_price <= fib_382
        wave_status = "Likely Wave 2" if in_wave_2 else "Impulse Complete or Waiting"

        st.write(f"**Wave 1 Range**: {round(wave1_low, 2)} → {round(wave1_high, 2)}")
        st.write(f"**Fib Entry Zone (38.2–61.8%)**: {round(fib_618, 2)} → {round(fib_382, 2)}")
        st.write(f"**Current Price**: {round(current_price, 2)}")
        st.write(f"**Wave Status**: {wave_status}")

except Exception as e:
    st.error(f"Wave detection failed: {e}")
