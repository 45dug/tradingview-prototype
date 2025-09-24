import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import base64

# Page setup with enhanced styling
st.set_page_config(
    page_title="TradeLeap - Look First, Then Leap",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to add background image
def add_bg_image():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* Overlay to improve readability */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(13, 17, 23, 0.85);
            z-index: -1;
        }}
        
        /* Main content area with transparency */
        .main .block-container {{
            background: rgba(30, 34, 45, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            margin: 20px;
            padding: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the background function
add_bg_image()

# Advanced CSS with all new features
st.markdown("""
<style>
    /* Header Styling - Look First / Then Leap with Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(41, 98, 255, 0.9) 0%, rgba(0, 172, 193, 0.9) 100%);
        padding: 4rem 2rem;
        text-align: center;
        border-radius: 15px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 300;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .hero-cta {
        background: white;
        color: #2962ff;
        border: none;
        border-radius: 30px;
        padding: 15px 40px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        color: #2962ff;
    }
    
    .hero-footer {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 1.5rem;
    }

    /* Top Navigation Bar */
    .top-nav {
        background: rgba(30, 34, 45, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-bottom: 1px solid #2a2e39;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 10px 10px 0 0;
    }
    
    .nav-section {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .nav-item {
        color: #d1d4dc;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.3s ease;
        padding: 8px 16px;
        border-radius: 6px;
    }
    
    .nav-item:hover {
        color: #2962ff;
        background: rgba(41, 98, 255, 0.1);
    }
    
    /* Main content styling */
    .content-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Rest of your existing styles remain the same */
    .forex-section, .news-section, .economy-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .news-item {
        background: rgba(42, 46, 57, 0.6);
        padding: 15px;
        margin: 10px 0;
        border-radius: 6px;
        border-left: 3px solid #2962ff;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        background: rgba(58, 62, 73, 0.8);
        transform: translateX(5px);
    }
    
    .currency-item {
        background: rgba(42, 46, 57, 0.6);
        padding: 10px;
        border-radius: 6px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .currency-item:hover {
        background: rgba(58, 62, 73, 0.8);
        transform: translateY(-2px);
    }
    
    .green { color: #26a69a; font-weight: 600; }
    .red { color: #ef5350; font-weight: 600; }
    .blue { color: #2962ff; }
    
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
        background-color: #1e52d4;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Generate advanced trading data with OHLC
def generate_advanced_data(symbol, points=200):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {
        "AAPL": 180, "TSLA": 250, "MSFT": 420, "GOOGL": 2800,
        "BTCUSD": 65000, "SPX": 5200, "NVDA": 120, "AMZN": 3500,
        "EURUSD": 1.08, "GBPUSD": 1.26, "USDJPY": 147.5, "USDCHF": 0.88
    }
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(points, 0, -1)]
    
    returns = np.random.normal(0, 0.002, points)
    prices = base_price * np.exp(np.cumsum(returns))
    
    opens, highs, lows, closes = [], [], [], []
    
    for i in range(points):
        open_price = closes[i-1] if i > 0 and closes else base_price
        close_price = prices[i]
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005)))
        
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
    
    return pd.DataFrame({
        'timestamp': dates,
        'open': opens, 'high': highs, 'low': lows, 'close': closes,
        'volume': np.random.randint(1000000, 5000000, points)
    })

def calculate_indicators(df):
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df

def generate_forex_news():
    return [
        {"time": "yesterday - Dow Jones Newswires", "headline": "Sterling Gains 0.31% to $1.3514 — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "The WSJ Dollar Index Falls 0.23% to 94.77 — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Loses 0.17% to 147.72 Yen — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Gains 0.27% to 1.3819 Canadian Dollars — Data Talk", "source": "DJN"},
    ]

# Initialize session state
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "EURUSD"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_advanced_data("EURUSD")
if 'is_live' not in st.session_state:
    st.session_state.is_live = False
if 'timeframe' not in st.session_state:
    st.session_state.timeframe = "1D"
if 'base_currency' not in st.session_state:
    st.session_state.base_currency = "EUR"
if 'show_more_news' not in st.session_state:
    st.session_state.show_more_news = False

st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)

# Hero Section with Background Image
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Look First / Then Leap</div>
    <div class="hero-subtitle">The best trades require research, then commitment.</div>
    <a href="#" class="hero-cta">Get started for free</a>
    <div class="hero-footer">$0 forever, no credit card needed</div>
</div>
""", unsafe_allow_html=True)

# Top Navigation Bar
st.markdown("""
<div class="top-nav">
    <div class="nav-section">
        <div class="nav-item">Search (3K)</div>
        <div class="nav-item">Products</div>
        <div class="nav-item">Community</div>
        <div class="nav-item">Markets</div>
        <div class="nav-item">Brokers</div>
        <div class="nav-item">More</div>
    </div>
    <div class="nav-section">
        <div class="nav-item">EN</div>
        <button class="hero-cta" style="padding: 10px 25px; font-size: 0.9rem; background: #2962ff; color: white;">Get started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 💱 Forex Rates")
    
    base_currencies = ["EUR", "USD", "GBP", "JPY", "CHF", "AUD", "CNY", "CAD"]
    base_cols = st.columns(8)
    for i, currency in enumerate(base_currencies):
        with base_cols[i]:
            if st.button(currency, key=f"base_{currency}", use_container_width=True):
                st.session_state.base_currency = currency
                st.session_state.current_symbol = f"{currency}USD" if currency != "USD" else "EURUSD"
                st.session_state.chart_data = generate_advanced_data(st.session_state.current_symbol)
                st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
                st.rerun()
    
    st.markdown("#### Quote Currencies")
    quote_currencies = ["USD", "GBP", "JPY", "CHF", "AUD", "CNY", "CAD"]
    quote_cols = st.columns(7)
    
    for i, currency in enumerate(quote_currencies):
        with quote_cols[i]:
            if currency != st.session_state.base_currency:
                rate = np.random.uniform(0.8, 1.5) if st.session_state.base_currency == "EUR" else np.random.uniform(100, 150) if currency == "JPY" else np.random.uniform(0.7, 2.0)
                change = np.random.uniform(-0.02, 0.02)
                st.metric(currency, f"{rate:.4f}", f"{change*100:+.2f}%")
    
    st.markdown("#### Timeframe")
    timeframes = ["1D", "1W", "1M", "3M", "6M", "1Y", "YTD", "5Y", "All"]
    tf_cols = st.columns(9)
    for i, tf in enumerate(timeframes):
        with tf_cols[i]:
            if st.button(tf, key=f"time_{tf}", use_container_width=True):
                st.session_state.timeframe = tf
                st.rerun()
    
    st.markdown("### 📈 Advanced Chart")
    chart_data = st.session_state.chart_data.set_index('timestamp')[['close', 'sma_20', 'sma_50']]
    st.line_chart(chart_data, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 📰 Forex News")
    st.markdown('<div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">Sign in to read exclusive news ></div>', unsafe_allow_html=True)
    
    news_data = generate_forex_news()
    for news in news_data[:3]:
        st.markdown(f"""
        <div class="news-item">
            <div style="color: #8c9baf; font-size: 0.9rem;">{news['time']}</div>
            <div style="font-weight: 600; margin: 5px 0;">{news['headline']}</div>
            <div style="color: #26a69a; font-size: 0.8rem;">{news['source']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Keep reading >", key="keep_reading", use_container_width=True):
        st.session_state.show_more_news = not st.session_state.show_more_news
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 🌍 Economy")
    st.markdown('<div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">Global inflation map ></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin: 15px 0;">
        <div style="background: #1a237e; padding: 8px; border-radius: 4px; text-align: center; color: white; font-size: 0.8rem;">&lt; 0%</div>
        <div style="background: #283593; padding: 8px; border-radius: 4px; text-align: center; color: white; font-size: 0.8rem;">0-3%</div>
        <div style="background: #303f9f; padding: 8px; border-radius: 4px; text-align: center; color: white; font-size: 0.8rem;">3-7%</div>
        <div style="background: #5c6bc0; padding: 8px; border-radius: 4px; text-align: center; color: white; font-size: 0.8rem;">7-12%</div>
        <div style="background: #7986cb; padding: 8px; border-radius: 4px; text-align: center; color: white; font-size: 0.8rem;">12-25%</div>
        <div style="background: #9fa8da; padding: 8px; border-radius: 4px; text-align: center; color: #1a237e; font-size: 0.8rem;">&gt; 25%</div>
    </div>
    """, unsafe_allow_html=True)
    
    inflation_data = {"USA": 3.2, "UK": 4.1, "Germany": 2.8, "France": 3.5, "Japan": 2.1}
    for country, rate in inflation_data.items():
        color = "#26a69a" if rate < 3 else "#ffa726" if rate < 7 else "#ef5350"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px; background: rgba(42,46,57,0.6); margin: 5px 0; border-radius: 4px;">
            <span>{country}</span>
            <span style="color: {color}; font-weight: 600;">{rate}%</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Trading Panel
st.markdown("### 🎯 Trading Panel")
tcol1, tcol2, tcol3, tcol4, tcol5, tcol6, tcol7 = st.columns(7)

with tcol1:
    if st.button("⏸️" if st.session_state.is_live else "▶️", use_container_width=True):
        st.session_state.is_live = not st.session_state.is_live
        st.rerun()

with tcol6:
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        current_data = st.session_state.chart_data.iloc[-1]
        st.success(f"✅ BUY 100 {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

with tcol7:
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        current_data = st.session_state.chart_data.iloc[-1]
        st.error(f"✅ SELL 100 {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d;'>
    <p>TradeLeap Pro • Look First, Then Leap • Real-time Data • Professional Charts</p>
    <p>© 2025 TradeLeap. All rights reserved. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
