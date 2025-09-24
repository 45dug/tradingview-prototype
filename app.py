import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.express as px

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
</style>
""", unsafe_allow_html=True)

# Generate global inflation data for heat map
def generate_global_inflation_data():
    countries = [
        'United States', 'China', 'Japan', 'Germany', 'United Kingdom', 
        'France', 'India', 'Brazil', 'Canada', 'Australia', 'Russia',
        'South Korea', 'Mexico', 'Indonesia', 'Netherlands', 'Saudi Arabia',
        'Turkey', 'Switzerland', 'Argentina', 'South Africa'
    ]
    
    inflation_rates = []
    for country in countries:
        if country in ['United States', 'Germany', 'Japan', 'Switzerland']:
            base_rate = np.random.uniform(2.0, 4.0)
        elif country in ['Turkey', 'Argentina']:
            base_rate = np.random.uniform(15.0, 25.0)
        elif country in ['United Kingdom', 'Canada', 'Australia']:
            base_rate = np.random.uniform(3.0, 6.0)
        else:
            base_rate = np.random.uniform(2.0, 7.0)
        
        inflation_rates.append(round(base_rate, 1))
    
    return pd.DataFrame({
        'Country': countries,
        'Inflation Rate': inflation_rates,
        'ISO_Code': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'IND', 'BRA', 'CAN', 'AUS', 
                    'RUS', 'KOR', 'MEX', 'IDN', 'NLD', 'SAU', 'TUR', 'CHE', 'ARG', 'ZAF']
    })

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
    
    closes = []
    for i in range(points):
        close_price = prices[i]
        closes.append(close_price)
    
    return pd.DataFrame({
        'timestamp': dates,
        'close': closes,
        'volume': np.random.randint(1000000, 5000000, points)
    })

def calculate_indicators(df):
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    return df

def generate_forex_news():
    return [
        {"time": "yesterday - Dow Jones Newswires", "headline": "Sterling Gains 0.31% to $1.3514", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "The WSJ Dollar Index Falls 0.23% to 94.77", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Loses 0.17% to 147.72 Yen", "source": "DJN"},
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
        <div style="color: #d1d4dc; font-weight: 500;">Search (3K)</div>
        <div style="color: #d1d4dc; font-weight: 500;">Products</div>
        <div style="color: #d1d4dc; font-weight: 500;">Community</div>
        <div style="color: #d1d4dc; font-weight: 500;">Markets</div>
        <div style="color: #d1d4dc; font-weight: 500;">Brokers</div>
        <div style="color: #d1d4dc; font-weight: 500;">More</div>
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
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 📰 Forex News")
    
    news_data = generate_forex_news()
    for news in news_data:
        st.markdown(f"""
        <div style="background: rgba(42,46,57,0.6); padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #2962ff;">
            <div style="color: #8c9baf; font-size: 0.9rem;">{news['time']}</div>
            <div style="font-weight: 600; margin: 5px 0;">{news['headline']}</div>
            <div style="color: #26a69a; font-size: 0.8rem;">{news['source']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 🌍 Economy")
    st.markdown('<div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">Global inflation map ></div>', unsafe_allow_html=True)
    
    # Inflation Legend
    st.markdown("""
    <div class="inflation-legend">
        <div class="legend-item" style="background: #1a237e; color: white;">&lt; 0%</div>
        <div class="legend-item" style="background: #283593; color: white;">0-3%</div>
        <div class="legend-item" style="background: #303f9f; color: white;">3-7%</div>
        <div class="legend-item" style="background: #5c6bc0; color: white;">7-12%</div>
        <div class="legend-item" style="background: #7986cb; color: white;">12-25%</div>
        <div class="legend-item" style="background: #9fa8da; color: #1a237e;">&gt; 25%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Global Heat Map
    st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
    st.markdown("#### 🌡️ Global Inflation Heat Map")
    
    # Create the choropleth map with fixed syntax
    fig = px.choropleth(
        inflation_data,
        locations="ISO_Code",
        color="Inflation Rate",
        hover_name="Country",
        hover_data={"Inflation Rate": True},
        color_continuous_scale="Blues",
        range_color=[0, 25],
        title="Global Inflation Rates (%)",
        height=300
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top countries by inflation
    st.markdown("#### 📊 Highest Inflation Rates")
    top_inflation = inflation_data.nlargest(5, 'Inflation Rate')
    
    for _, country in top_inflation.iterrows():
        rate = country['Inflation Rate']
        color = "#ef5350" if rate > 12 else "#ffa726" if rate > 7 else "#26a69a"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px; background: rgba(42,46,57,0.6); margin: 5px 0; border-radius: 4px;">
            <span>{country['Country']}</span>
            <span style="color: {color}; font-weight: 600;">{rate}%</span>
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
<div style='text-align: center; color: #6a737d;'>
    <p>TradeLeap Pro • Look First, Then Leap • Real-time Data • Professional Charts</p>
    <p>© 2025 TradeLeap. All rights reserved. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
