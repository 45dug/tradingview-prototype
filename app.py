import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lightweight_charts import renderLightweightCharts

# Page configuration - makes it look more like an app
st.set_page_config(page_title="ProtoView", layout="wide", initial_sidebar_state="collapsed")

# Load sample price data for different symbols
@st.cache_data
def load_sample_data(symbol):
    # This creates fake but realistic sample data for a symbol
    np.random.seed(hash(symbol) % 100)  # For consistent fake data per symbol
    date_range = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='min')
    base_price = 150 if symbol == "AAPL" else 300 if symbol == "MSFT" else 1000
    volatility = 0.5

    close_prices = base_price + np.cumsum(np.random.randn(100) * volatility)
    open_prices = close_prices - np.random.rand(100) * 0.5 - 0.25
    high_prices = np.maximum(open_prices, close_prices) + np.random.rand(100) * 0.5
    low_prices = np.minimum(open_prices, close_prices) - np.random.rand(100) * 0.5

    df = pd.DataFrame({
        'time': date_range,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices
    })
    # Format time for the charting library
    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return df.to_dict('records')

# Define the watchlist
WATCHLIST = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.",
    "BTCUSD": "Bitcoin / USD"
}

# Initialize the selected symbol in session state
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = "AAPL"

# SIDEBAR - WATCHLIST
with st.sidebar:
    st.header("📈 Watchlist")
    for symbol, name in WATCHLIST.items():
        if st.button(f"{symbol} - {name}", key=symbol, use_container_width=True):
            st.session_state.selected_symbol = symbol
    st.divider()
    st.write("**Current:**", st.session_state.selected_symbol)

# MAIN CHART AREA
st.title(f"Chart: {st.session_state.selected_symbol}")

# Load the data for the selected symbol
chart_data = load_sample_data(st.session_state.selected_symbol)

# Configure the chart options for a dark theme (like TradingView)
chartOptions = {
    "layout": {
        "textColor": 'black',
        "background": {
            "type": 'solid',
            "color": 'white'
        }
    },
    "grid": {
        "vertLines": {
            "color": 'rgba(197, 203, 206, 0.5)'
        },
        "horzLines": {
            "color": 'rgba(197, 203, 206, 0.5)'
        }
    },
    "timeScale": {
        "timeVisible": True,
        "secondsVisible": False,
    }
}

# Create the series for candlesticks
candleSeries = {
    "type": 'Candlestick',
    "data": chart_data,
    "options": {
        "upColor": '#26a69a',
        "downColor": '#ef5350',
        "borderVisible": False,
        "wickUpColor": '#26a69a',
        "wickDownColor": '#ef5350'
    }
}

# Render the chart. The key is important for stability.
renderLightweightCharts([
    {
        "chart": chartOptions,
        "series": [candleSeries]
    }
], 'chart')

# BOTTOM PANEL - Placeholder for order entry or news
st.divider()
st.subheader("Order Entry")
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Order Type", ["Market", "Limit"], key="order_type")
    st.number_input("Quantity", min_value=1, value=10, key="qty")
with col2:
    st.number_input("Price", value=float(f"{chart_data[-1]['close']:.2f}"), key="price", disabled=(st.session_state.order_type == "Market"))
    if st.button("BUY", type="primary", use_container_width=True):
        st.success(f"Market Buy order for {st.session_state.qty} {st.session_state.selected_symbol} placed!")
    if st.button("SELL", type="secondary", use_container_width=True):
        st.error(f"Market Sell order for {st.session_state.qty} {st.session_state.selected_symbol} placed!")
