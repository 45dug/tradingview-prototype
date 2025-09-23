import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page setup
st.set_page_config(
    page_title="TradingView - Advanced Charts",
    layout="wide"
)

# CSS for professional look
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card { background: white; padding: 15px; border-radius: 8px; margin: 5px; border-left: 4px solid #2962ff; }
    
    /* Improved chart appearance */
    .stLineChart {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Better watchlist items */
    .watchlist-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        background: white;
        border-left: 4px solid #2962ff;
        transition: all 0.3s ease;
    }
    
    .watchlist-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Trading panel styling */
    .trading-panel {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate realistic trading data
def generate_stock_data(symbol, points=100):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {"AAPL": 180, "TSLA": 250, "MSFT": 420, "BTCUSD": 65000}
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(hours=x) for x in range(points)]
    prices = base_price + np.cumsum(np.random.randn(points) * 2)
    
    df = pd.DataFrame({
        'timestamp': dates[::-1],  # Reverse to show oldest first
        'price': prices[::-1]
    })
    
    return df

# Initialize session state
if 'current_stock' not in st.session_state:
    st.session_state.current_stock = "AAPL"
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = generate_stock_data("AAPL")
if 'is_live' not in st.session_state:
    st.session_state.is_live = False

# Sidebar - Watchlist and Controls
with st.sidebar:
    st.title("📊 TradingView")
    st.markdown("---")
    
    st.subheader("📍 Watchlist")
    
    watchlist = {
        "AAPL": {"name": "Apple Inc.", "price": 182.35, "change": +1.25, "change_pct": +0.69},
        "TSLA": {"name": "Tesla Inc.", "price": 248.90, "change": +5.60, "change_pct": +2.30},
        "MSFT": {"name": "Microsoft", "price": 421.80, "change": -2.30, "change_pct": -0.54},
        "BTCUSD": {"name": "Bitcoin", "price": 65123.45, "change": +1234.56, "change_pct": +1.93}
    }
    
    for symbol, data in watchlist.items():
        change_color = "color: #26a69a;" if data["change"] >= 0 else "color: #ef5350;"
        change_icon = "▲" if data["change"] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="watchlist-item" onclick="this.style.background='#f0f7ff'">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{symbol}</strong><br>
                    <small>{data['name']}</small>
                </div>
                <div style="text-align: right;">
                    <div>${data['price']:.2f}</div>
                    <div style="{change_color}">{change_icon} {data['change_pct']:.2f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View {symbol}", key=f"btn_{symbol}", use_container_width=True):
            st.session_state.current_stock = symbol
            st.session_state.stock_data = generate_stock_data(symbol)
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("⚙️ Chart Controls")
    chart_type = st.radio("Chart Type", ["Line", "Area"], horizontal=True)
    timeframe = st.select_slider("Timeframe", options=["1D", "1W", "1M", "3M", "1Y"])
    
    st.markdown("---")
    
    st.subheader("📈 Technical Indicators")
    indicators = ["Moving Average", "RSI", "MACD", "Bollinger Bands", "Volume"]
    for indicator in indicators:
        if st.checkbox(f"• {indicator}"):
            st.slider(f"{indicator} Period", 5, 50, 14, key=f"slider_{indicator}")
    
    st.markdown("---")
    
    st.subheader("💼 Portfolio")
    st.metric("Total Value", "$125,430.25", "+2.3%")
    st.write("**Cash:** $12,500.00")
    st.write("**AAPL:** 15 shares")
    st.write("**TSLA:** 5 shares")

# Main trading interface
st.title(f"📈 {st.session_state.current_stock} - {watchlist[st.session_state.current_stock]['name']}")

# Current price info
current_price = st.session_state.stock_data['price'].iloc[-1]
previous_price = st.session_state.stock_data['price'].iloc[-2]
price_change = current_price - previous_price
change_percent = (price_change / previous_price) * 100

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Current Price", 
        f"${current_price:.2f}", 
        f"{change_percent:+.2f}%"
    )
with col2:
    st.metric("Today's High", f"${st.session_state.stock_data['price'].max():.2f}")
with col3:
    st.metric("Today's Low", f"${st.session_state.stock_data['price'].min():.2f}")
with col4:
    st.metric("Volume", "2.5M")

# Price chart
st.subheader("Price Chart")

# Add timeframe buttons above the chart
timeframes = ["1D", "1W", "1M", "3M", "1Y", "All"]
cols = st.columns(6)
for i, tf in enumerate(timeframes):
    with cols[i]:
        if st.button(tf, use_container_width=True):
            st.info(f"Switched to {tf} view")

# Display the chart with better styling
chart_data = st.session_state.stock_data.set_index('timestamp')
if chart_type == "Area":
    st.area_chart(chart_data, height=400)
else:
    st.line_chart(chart_data, height=400)

# Add price levels below the chart
st.caption(f"📊 Chart showing {len(chart_data)} data points | Latest: ${current_price:.2f}")

# Trading panel
st.markdown('<div class="trading-panel">', unsafe_allow_html=True)
st.subheader("🎯 Trading Panel")

# Trading controls in a more compact layout
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])

with col1:
    live_status = "⏸️" if st.session_state.is_live else "▶️"
    if st.button(live_status, help="Live/Simulation Mode"):
        st.session_state.is_live = not st.session_state.is_live

with col2:
    if st.button("🔄", help="Refresh Data"):
        st.session_state.stock_data = generate_stock_data(st.session_state.current_stock)
        st.rerun()

with col3:
    order_type = st.selectbox("Type", ["Market", "Limit"], label_visibility="collapsed")

with col4:
    quantity = st.number_input("Qty", min_value=1, value=100, label_visibility="collapsed")

with col5:
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        st.success(f"✅ BUY {quantity} {st.session_state.current_stock} @ ${current_price:.2f}")

with col6:
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        st.error(f"✅ SELL {quantity} {st.session_state.current_stock} @ ${current_price:.2f}")

st.markdown('</div>', unsafe_allow_html=True)

# Live data simulation
if st.session_state.is_live:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(10):
        if not st.session_state.is_live:
            break
            
        # Add new data point
        new_price = current_price * (1 + np.random.uniform(-0.01, 0.01))
        new_time = datetime.now()
        
        new_row = pd.DataFrame({
            'timestamp': [new_time],
            'price': [new_price]
        })
        
        st.session_state.stock_data = pd.concat([
            st.session_state.stock_data.iloc[1:],  # Remove oldest point
            new_row
        ], ignore_index=True)
        
        progress_bar.progress((i + 1) / 10)
        status_text.text(f"📡 Live data updating... {i + 1}/10")
        time.sleep(1)
    
    progress_bar.empty()
    status_text.empty()
    st.session_state.is_live = False
    st.rerun()

# Market news section
st.subheader("📰 Market News")
news = [
    {"headline": "Apple announces new AI features for iPhone", "time": "2 hours ago", "symbol": "AAPL"},
    {"headline": "Tesla deliveries exceed expectations", "time": "4 hours ago", "symbol": "TSLA"},
    {"headline": "Microsoft partners with OpenAI for new AI tools", "time": "6 hours ago", "symbol": "MSFT"}
]

for item in news:
    with st.expander(f"📌 {item['headline']}"):
        st.write(f"**{item['time']}** · Symbol: #{item['symbol']}")
        st.write("Market analysts are optimistic about this development...")

# Footer
st.markdown("---")
st.caption("TradingView Professional · Real-time market data · Not financial advice")
