import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page setup
st.set_page_config(page_title="Trading App", layout="wide")

# Create sample data
def create_data(symbol):
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=50, freq='min')
    base_price = 150 if symbol == "AAPL" else 300
    prices = base_price + np.cumsum(np.random.randn(50))
    
    df = pd.DataFrame({
        'Time': dates,
        'Price': prices
    })
    return df

# Watchlist
WATCHLIST = {"AAPL": "Apple", "MSFT": "Microsoft", "TSLA": "Tesla"}

# Initialize
if 'symbol' not in st.session_state:
    st.session_state.symbol = "AAPL"
if 'data' not in st.session_state:
    st.session_state.data = create_data("AAPL")

# Sidebar
with st.sidebar:
    st.title("Trading App")
    for sym, name in WATCHLIST.items():
        if st.button(f"{sym} - {name}"):
            st.session_state.symbol = sym
            st.session_state.data = create_data(sym)

# Main chart
st.header(f"{st.session_state.symbol} Price Chart")
st.line_chart(st.session_state.data.set_index('Time'))

# Current price
current_price = st.session_state.data['Price'].iloc[-1]
st.metric("Current Price", f"${current_price:.2f}")

# Order panel
st.divider()
st.subheader("Place Order")
col1, col2 = st.columns(2)
with col1:
    qty = st.number_input("Quantity", value=10)
with col2:
    if st.button("BUY", type="primary"):
        st.success(f"Bought {qty} shares at ${current_price:.2f}")
    if st.button("SELL"):
        st.error(f"Sold {qty} shares at ${current_price:.2f}")

# Footer
st.divider()
st.caption("Trading prototype - Not real data")
