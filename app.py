import streamlit as st
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(page_title="ProtoView", layout="wide")

# Create sample data function
def create_sample_data(symbol, periods=100):
    np.random.seed(hash(symbol) % 100)
    base_price = 150 if symbol == "AAPL" else 300 if symbol == "MSFT" else 1000
    volatility = 0.8
    
    dates = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='min')
    price_changes = np.random.randn(periods) * volatility
    prices = base_price + np.cumsum(price_changes)
    
    df = pd.DataFrame({
        'Date': dates,
        'Price': prices
    })
    df.set_index('Date', inplace=True)
    return df

# Watchlist
WATCHLIST = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.", 
    "TSLA": "Tesla Inc."
}

# Initialize session state
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = "AAPL"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = create_sample_data("AAPL")

# Sidebar
with st.sidebar:
    st.header("📈 Watchlist")
    for symbol, name in WATCHLIST.items():
        if st.button(f"{symbol} - {name}", key=symbol, use_container_width=True):
            st.session_state.selected_symbol = symbol
            st.session_state.chart_data = create_sample_data(symbol)
    st.divider()
    st.write("**Current:**", st.session_state.selected_symbol)

# Main chart area
st.title(f"{st.session_state.selected_symbol} Price Chart")
st.line_chart(st.session_state.chart_data)

# Simulate live updates
if st.button("Start Live Simulation"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        # Update data
        new_price = st.session_state.chart_data.iloc[-1]['Price'] + np.random.randn() * 0.5
        new_row = pd.DataFrame({'Price': [new_price]}, 
                              index=[pd.Timestamp.now()])
        st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_row])
        
        # Update chart
        st.line_chart(st.session_state.chart_data)
        
        # Update progress
        progress_bar.progress(i + 1)
        status_text.text(f"Update {i + 1}/100")
        time.sleep(0.1)
    
    progress_bar.empty()
    status_text.text("Live simulation complete!")

# Order panel
st.divider()
st.subheader("Order Entry")
col1, col2 = st.columns(2)

with col1:
    order_type = st.selectbox("Order Type", ["Market", "Limit"])
    quantity = st.number_input("Quantity", min_value=1, value=10)

with col2:
    current_price = st.session_state.chart_data.iloc[-1]['Price']
    price = st.number_input("Price", value=float(current_price), 
                           disabled=(order_type == "Market"))
    
    if st.button("BUY", type="primary"):
        st.success(f"Buy order for {quantity} {st.session_state.selected_symbol} at ${current_price:.2f}!")
    
    if st.button("SELL", type="secondary"):
        st.error(f"Sell order for {quantity} {st.session_state.selected_symbol} at ${current_price:.2f}!")
