import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go  # ✅ updated import

# -------------------------------
# TradingView Prototype
# -------------------------------

st.set_page_config(page_title="TradingView Prototype", layout="wide")

# Title
st.title("📈 TradingView Prototype")

# Sidebar
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Enter Symbol (e.g. BTCUSDT)", "BTCUSDT")
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "4h", "1d"])
limit = st.sidebar.slider("Number of Candles", 50, 500, 100)

# Binance API fetch
def get_binance_data(symbol, interval, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Load data
df = get_binance_data(symbol, interval, limit)

if not df.empty:
    st.subheader(f"Candlestick Chart - {symbol} ({interval})")

    # Plot candlestick
    fig = go.Figure(data=[go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Candlesticks"
    )])

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show data table
    with st.expander("Show Raw Data"):
        st.write(df)
else:
    st.warning("No data available. Please check the symbol or interval.")

