import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ===== TRADINGVIEW COMPLETE PROTOTYPE =====
# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView - Where the world does markets",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== TRADINGVIEW CSS STYLING =====
st.markdown("""
<style>
    /* Main TradingView Dark Theme */
    .main { 
        background-color: #131722; 
        color: #d1d4dc; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #000000 0%, #131722 100%);
        padding: 80px 20px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2962ff 0%, #00bcd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.9;
        margin-bottom: 40px;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #2962ff 0%, #00bcd4 100%);
        border: none;
        padding: 15px 40px;
        font-size: 1.2rem;
        border-radius: 30px;
        color: white;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1e222d;
        color: #d1d4dc;
    }
    
    /* Cards and Containers */
    .market-card {
        background-color: #1e222d;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #2962ff;
    }
    
    .feature-card {
        background-color: #1e222d;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
    }
    
    /* Watchlist Items */
    .watchlist-item {
        padding: 12px;
        margin: 6px 0;
        border-radius: 6px;
        background-color: #2a2e39;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .watchlist-item:hover {
        background-color: #3a3e49;
        transform: translateX(5px);
    }
    
    /* Colors */
    .green { color: #26a69a; font-weight: 600; }
    .red { color: #ef5350; font-weight: 600; }
    .blue { color: #2962ff; }
    
    /* Buttons */
    .stButton>button {
        background-color: #2962ff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1e53e5;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ===== SAMPLE DATA GENERATION =====
def generate_price_data(symbol, periods=100):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {
        "AAPL": 180, "MSFT": 420, "TSLA": 250, 
        "BTCUSD": 65000, "SPX": 5200, "GOOGL": 2800
    }
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(periods, 0, -1)]
    prices = base_price + np.cumsum(np.random.randn(periods) * 0.8)
    
    return pd.DataFrame({'Time': dates, 'Price': prices})

# ===== WATCHLIST DATA =====
WATCHLIST = {
    "AAPL": {"name": "Apple Inc.", "price": 180.25, "change": +1.25, "change_pct": +0.70},
    "MSFT": {"name": "Microsoft Corp.", "price": 421.80, "change": -2.30, "change_pct": -0.54},
    "TSLA": {"name": "Tesla Inc.", "price": 248.90, "change": +5.60, "change_pct": +2.30},
    "BTCUSD": {"name": "Bitcoin/USD", "price": 65123.45, "change": +1234.56, "change_pct": +1.93},
    "SPX": {"name": "S&P 500 Index", "price": 5200.67, "change": +15.80, "change_pct": +0.30},
    "GOOGL": {"name": "Google LLC", "price": 2798.30, "change": +15.80, "change_pct": +0.57}
}

# ===== INITIALIZE SESSION STATE =====
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'price_data' not in st.session_state:
    st.session_state.price_data = generate_price_data("AAPL")
if 'show_trading_platform' not in st.session_state:
    st.session_state.show_trading_platform = False

# ===== LANDING PAGE =====
if not st.session_state.show_trading_platform:
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Where the world does markets</h1>
        <p class="hero-subtitle">Join 100 million traders and investors taking the future into their own hands.</p>
        <button class="cta-button" onclick="window.showTradingPlatform()">Get started for free</button>
        <p style="margin-top: 20px; font-size: 1rem; opacity: 0.7;">$0 forever, no credit card needed</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Look first / Then leap.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.8;'>The best trades require research, then commitment.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Advanced Charts</h3>
            <p>Professional trading charts with 100+ indicators and drawing tools</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Real-time Data</h3>
            <p>Live market data for stocks, crypto, forex, and indices</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤝 Social Trading</h3>
            <p>Follow top traders and share ideas with our community</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Market Overview
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Live Market Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="market-card">
            <h4>💰 Crypto Market Cap</h4>
            <h3>3.91T USD</h3>
            <p class="red">–1.26% today</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="market-card">
            <h4>📊 US Dollar Index</h4>
            <h3>97.789 USD</h3>
            <p class="green">+0.15% today</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="market-card">
            <h4>🛢️ Crude Oil</h4>
            <h3>62.77 USD/BLL</h3>
            <p class="green">+0.59%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stock Indices
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="market-card">
            <h4>🇬🇧 FTSE 100</h4>
            <h3>9,216.67</h3>
            <p class="red">–0.12%</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="market-card">
            <h4>🇩🇪 DAX</h4>
            <h3>23,639.41</h3>
            <p class="red">–0.15%</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="market-card">
            <h4>🇫🇷 CAC 40</h4>
            <h3>7,853.59</h3>
            <p class="red">–0.01%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <p style='opacity: 0.7;'>Scott 'Kidd' Poteet • The unlikely astronaut • Watch explainer</p>
        <p style='opacity: 0.5;'>© 2025 TradingView Clone. Not financial advice.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # JavaScript to switch to trading platform
    st.markdown("""
    <script>
    function showTradingPlatform() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: 'show_trading'
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)

# ===== TRADING PLATFORM =====
else:
    # Sidebar - TradingView Style
    with st.sidebar:
        st.markdown("<h1 style='color: #2962ff; margin-bottom: 30px;'>TradingView</h1>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 📊 Navigation")
        nav_options = ["Charts", "Watchlist", "Screener", "News", "Alerts", "Community"]
        for option in nav_options:
            st.button(f"• {option}", use_container_width=True)
        
        st.markdown("---")
        
        # Watchlist
        st.markdown("### 📈 Watchlist")
        for symbol, data in WATCHLIST.items():
            change_color = "green" if data["change"] >= 0 else "red"
            change_icon = "▲" if data["change"] >= 0 else "▼"
            
            if st.button(f"{symbol} - ${data['price']:.2f} {change_icon} {abs(data['change']):.2f}", 
                        key=f"watch_{symbol}", use_container_width=True):
                st.session_state.current_symbol = symbol
                st.session_state.price_data = generate_price_data(symbol)
                st.rerun()
        
        st.markdown("---")
        
        # Market Overview
        st.markdown("### 🌍 Market Overview")
        markets = [
            ("Crypto Cap", "3.91T", "-1.26%", "red"),
            ("DXY", "97.789", "+0.15%", "green"),
            ("Oil", "62.77", "+0.59%", "green"),
            ("Gold", "2345.60", "-0.45%", "red")
        ]
        
        for name, value, change, color in markets:
            st.markdown(f"**{name}**: {value} <span class='{color}'>{change}</span>", unsafe_allow_html=True)
    
    # Main Trading Interface
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # Header with symbol info
        current_data = WATCHLIST[st.session_state.current_symbol]
        change_color = "green" if current_data["change"] >= 0 else "red"
        change_icon = "▲" if current_data["change"] >= 0 else "▼"
        
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <h2>{st.session_state.current_symbol} - {current_data['name']}</h2>
            <h2 class='{change_color}'>${current_data['price']:.2f} {change_icon} {abs(current_data['change']):.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Chart
        st.line_chart(st.session_state.price_data.set_index('Time'), height=400)
        
        # Timeframe buttons
        timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W"]
        cols = st.columns(8)
        for i, tf in enumerate(timeframes):
            with cols[i]:
                st.button(tf)
    
    with col2:
        # Order Panel
        st.markdown("### 🎯 Order Entry")
        
        order_type = st.selectbox("Type", ["Market", "Limit", "Stop"])
        quantity = st.number_input("Qty", min_value=1, value=100)
        price = st.number_input("Price", value=float(current_data["price"]))
        
        if st.button("🟢 BUY", type="primary", use_container_width=True):
            st.success(f"Buy {quantity} {st.session_state.current_symbol}")
        if st.button("🔴 SELL", type="secondary", use_container_width=True):
            st.error(f"Sell {quantity} {st.session_state.current_symbol}")
        
        st.markdown("---")
        
        # Portfolio Summary
        st.markdown("### 💼 Portfolio")
        portfolio = {
            "AAPL": {"qty": 15, "avg": 175.30},
            "Cash": {"qty": 1, "avg": 12500.00}
        }
        
        for asset, info in portfolio.items():
            current_val = current_data["price"] if asset == "AAPL" else info["avg"]
            value = info["qty"] * current_val
            st.write(f"**{asset}**: {info['qty']} (${value:,.2f})")
    
    # Bottom Panel - Market News
    st.markdown("---")
    st.markdown("### 📰 Market News")
    news_items = [
        ("Apple announces new AI features", "2 hours ago", "AAPL"),
        ("Fed holds rates steady", "4 hours ago", "SPX"),
        ("Bitcoin ETF approvals expected", "6 hours ago", "BTCUSD")
    ]
    
    for headline, time, symbol in news_items:
        st.markdown(f"**{headline}** · {time} · {symbol}")

# ===== SIMPLE requirements.txt =====
# Keep your requirements.txt as:
# streamlit
# pandas
# numpy
