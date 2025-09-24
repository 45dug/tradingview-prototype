import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

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
        
        .main .block-container {{
            background: rgba(30, 34, 45, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            margin: 20px;
            padding: 20px;
        }}
        
        .heatmap-container {{
            background: rgba(42, 46, 57, 0.6);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()

# Advanced CSS
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, rgba(41, 98, 255, 0.9) 0%, rgba(0, 172, 193, 0.9) 100%);
        padding: 4rem 2rem;
        text-align: center;
        border-radius: 15px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 300;
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
        display: inline-block;
        text-decoration: none;
    }
    
    .top-nav {
        background: rgba(30, 34, 45, 0.95);
        padding: 1rem 2rem;
        border-bottom: 1px solid #2a2e39;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 10px 10px 0 0;
    }
    
    .content-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .inflation-legend {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 5px;
        margin: 15px 0;
    }
    
    .legend-item {
        padding: 8px;
        border-radius: 4px;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .heatmap-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin: 20px 0;
    }
    
    .country-cell {
        background: rgba(42, 46, 57, 0.8);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .country-cell:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Generate global inflation data for heat map (using text-based visualization)
def generate_global_inflation_data():
    countries = [
        'USA', 'China', 'Japan', 'Germany', 'UK', 
        'France', 'India', 'Brazil', 'Canada', 'Australia',
        'Russia', 'S.Korea', 'Mexico', 'Indonesia', 'S.Arabia',
        'Turkey', 'Switzerland', 'Argentina', 'S.Africa', 'Italy'
    ]
    
    inflation_data = {}
    for country in countries:
        if country in ['USA', 'Germany', 'Japan', 'Switzerland']:
            base_rate = np.random.uniform(2.0, 4.0)
        elif country in ['Turkey', 'Argentina']:
            base_rate = np.random.uniform(15.0, 25.0)
        elif country in ['UK', 'Canada', 'Australia']:
            base_rate = np.random.uniform(3.0, 6.0)
        else:
            base_rate = np.random.uniform(2.0, 8.0)
        
        inflation_data[country] = round(base_rate, 1)
    
    return inflation_data

# Generate trading data
def generate_advanced_data(symbol, points=200):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {
        "AAPL": 180, "TSLA": 250, "MSFT": 420, "GOOGL": 2800,
        "BTCUSD": 65000, "EURUSD": 1.08, "GBPUSD": 1.26, "USDJPY": 147.5
    }
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(points, 0, -1)]
    returns = np.random.normal(0, 0.002, points)
    prices = base_price * np.exp(np.cumsum(returns))
    
    return pd.DataFrame({
        'timestamp': dates,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, points)
    })

def calculate_indicators(df):
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    return df

def generate_forex_news():
    return [
        {"time": "2 hours ago", "headline": "Sterling Gains 0.31% to $1.3514", "source": "DJN"},
        {"time": "3 hours ago", "headline": "Dollar Index Falls 0.23% to 94.77", "source": "DJN"},
        {"time": "4 hours ago", "headline": "Yen Strengthens Amid Bank of Japan Meeting", "source": "Reuters"},
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

st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
inflation_data = generate_global_inflation_data()

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Look First / Then Leap</div>
    <div class="hero-subtitle">The best trades require research, then commitment.</div>
    <a href="#" class="hero-cta">Get started for free</a>
    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 1.5rem;">
        $0 forever, no credit card needed
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="top-nav">
    <div style="display: flex; align-items: center; gap: 2rem;">
        <div style="color: #d1d4dc; font-weight: 500;">Search</div>
        <div style="color: #d1d4dc; font-weight: 500;">Products</div>
        <div style="color: #d1d4dc; font-weight: 500;">Community</div>
        <div style="color: #d1d4dc; font-weight: 500;">Markets</div>
        <div style="color: #d1d4dc; font-weight: 500;">Brokers</div>
    </div>
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="color: #d1d4dc; font-weight: 500;">EN</div>
        <button style="background: #2962ff; color: white; border: none; padding: 10px 25px; border-radius: 20px; font-weight: 600;">Get started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 💱 Forex Rates")
    
    base_currencies = ["EUR", "USD", "GBP", "JPY", "CHF", "AUD"]
    base_cols = st.columns(6)
    for i, currency in enumerate(base_currencies):
        with base_cols[i]:
            if st.button(currency, key=f"base_{currency}", use_container_width=True):
                st.session_state.base_currency = currency
                st.session_state.current_symbol = f"{currency}USD" if currency != "USD" else "EURUSD"
                st.session_state.chart_data = generate_advanced_data(st.session_state.current_symbol)
                st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
                st.rerun()
    
    st.markdown("#### Quote Currencies")
    quote_currencies = ["USD", "GBP", "JPY", "CHF", "AUD"]
    quote_cols = st.columns(5)
    
    for i, currency in enumerate(quote_currencies):
        with quote_cols[i]:
            if currency != st.session_state.base_currency:
                rate = np.random.uniform(0.8, 1.5)
                change = np.random.uniform(-0.02, 0.02)
                st.metric(currency, f"{rate:.4f}", f"{change*100:+.2f}%")
    
    st.markdown("#### Timeframe")
    timeframes = ["1D", "1W", "1M", "3M", "6M", "1Y"]
    tf_cols = st.columns(6)
    for i, tf in enumerate(timeframes):
        with tf_cols[i]:
            if st.button(tf, key=f"time_{tf}", use_container_width=True):
                st.session_state.timeframe = tf
                st.rerun()
    
    st.markdown("### 📈 Advanced Chart")
    if not st.session_state.chart_data.empty:
        chart_data = st.session_state.chart_data.set_index('timestamp')[['close']]
        st.line_chart(chart_data, height=400)
    
    # Technical indicators
    if not st.session_state.chart_data.empty:
        current_data = st.session_state.chart_data.iloc[-1]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${current_data['close']:.4f}")
        with col2:
            st.metric("20 SMA", f"${current_data.get('sma_20', current_data['close']):.4f}")
        with col3:
            st.metric("Volume", f"{current_data['volume']/1000000:.1f}M")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 📰 Market News")
    
    news_data = generate_forex_news()
    for news in news_data:
        st.markdown(f"""
        <div style="background: rgba(42,46,57,0.6); padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #2962ff;">
            <div style="color: #8c9baf; font-size: 0.9rem;">{news['time']}</div>
            <div style="font-weight: 600; margin: 5px 0;">{news['headline']}</div>
            <div style="color: #26a69a; font-size: 0.8rem;">{news['source']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### 💡 Trading Ideas")
    ideas = [
        {"symbol": "EUR/USD", "action": "BUY", "confidence": 75},
        {"symbol": "GBP/JPY", "action": "SELL", "confidence": 68},
        {"symbol": "USD/CAD", "action": "HOLD", "confidence": 82}
    ]
    
    for idea in ideas:
        color = "#26a69a" if idea["confidence"] > 70 else "#ffa726"
        st.markdown(f"""
        <div style="background: rgba(42,46,57,0.6); padding: 12px; margin: 8px 0; border-radius: 6px;">
            <div style="display: flex; justify-content: space-between;">
                <strong>{idea['symbol']}</strong>
                <span style="color: {color}; font-weight: 600;">{idea['action']}</span>
            </div>
            <div style="color: #8c9baf; font-size: 0.8rem;">Confidence: {idea['confidence']}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 🌍 Global Economy")
    st.markdown('<div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">Inflation Heat Map</div>', unsafe_allow_html=True)
    
    # Inflation Legend
    st.markdown("""
    <div class="inflation-legend">
        <div class="legend-item" style="background: #1a237e; color: white;">&lt; 3%</div>
        <div class="legend-item" style="background: #283593; color: white;">3-5%</div>
        <div class="legend-item" style="background: #303f9f; color: white;">5-7%</div>
        <div class="legend-item" style="background: #5c6bc0; color: white;">7-10%</div>
        <div class="legend-item" style="background: #7986cb; color: white;">10-15%</div>
        <div class="legend-item" style="background: #9fa8da; color: #1a237e;">&gt; 15%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text-based Heat Map Grid
    st.markdown("#### 🌡️ Global Inflation Rates")
    st.markdown('<div class="heatmap-grid">', unsafe_allow_html=True)
    
    # Create a grid of country cells with color coding
    countries = list(inflation_data.keys())
    for i in range(0, min(20, len(countries)), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(countries):
                country = countries[i + j]
                rate = inflation_data[country]
                
                # Determine color based on inflation rate
                if rate < 3:
                    color = "#1a237e"
                elif rate < 5:
                    color = "#283593"
                elif rate < 7:
                    color = "#303f9f"
                elif rate < 10:
                    color = "#5c6bc0"
                elif rate < 15:
                    color = "#7986cb"
                else:
                    color = "#9fa8da"
                
                with cols[j]:
                    st.markdown(f"""
                    <div class="country-cell" style="border-left: 4px solid {color};">
                        <div style="font-weight: 600; font-size: 0.9rem;">{country}</div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: {color};">{rate}%</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Economic indicators
    st.markdown("#### 📊 Key Indicators")
    indicators = [
        {"name": "Global GDP Growth", "value": "3.1%", "change": "-0.2%"},
        {"name": "Unemployment Rate", "value": "5.2%", "change": "+0.1%"},
        {"name": "Oil Prices", "value": "$78.30", "change": "+1.8%"},
        {"name": "Gold Prices", "value": "$1,842", "change": "-0.5%"}
    ]
    
    for indicator in indicators:
        change_color = "green" if "-" in indicator["change"] else "red" if "+" in indicator["change"] else "gray"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; background: rgba(42,46,57,0.6); margin: 5px 0; border-radius: 4px;">
            <span>{indicator['name']}</span>
            <div>
                <span style="font-weight: 600;">{indicator['value']}</span>
                <span style="color: {change_color}; margin-left: 10px;">{indicator['change']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Trading Panel
st.markdown("### 🎯 Trading Panel")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    if st.button("⏸️" if st.session_state.is_live else "▶️", use_container_width=True):
        st.session_state.is_live = not st.session_state.is_live
        st.rerun()

with col2:
    if st.button("🔄", use_container_width=True):
        st.session_state.chart_data = generate_advanced_data(st.session_state.current_symbol)
        st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
        st.rerun()

with col6:
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        if not st.session_state.chart_data.empty:
            current_data = st.session_state.chart_data.iloc[-1]
            st.success(f"✅ BUY 100 {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

with col7:
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        if not st.session_state.chart_data.empty:
            current_data = st.session_state.chart_data.iloc[-1]
            st.error(f"✅ SELL 100 {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d; padding: 2rem;'>
    <h3>Start Your Trading Journey Today</h3>
    <p>Professional tools for informed trading decisions</p>
    <button style="background: linear-gradient(45deg, #2962ff, #00acc1); color: white; border: none; 
                   padding: 12px 30px; border-radius: 25px; font-weight: 600; cursor: pointer; margin: 10px;">
        Create Free Account
    </button>
    <div style="margin-top: 20px;">
        <p>TradeLeap Pro • Look First, Then Leap • Real-time Data • Professional Charts</p>
        <p>© 2025 TradeLeap. All rights reserved. Not financial advice.</p>
    </div>
</div>
""", unsafe_allow_html=True)
