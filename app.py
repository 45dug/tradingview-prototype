import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go

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
        
        /* Heat map container styling */
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
    
    /* Economy section specific styling */
    .economy-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
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

# Generate global inflation data for heat map
def generate_global_inflation_data():
    countries = [
        'United States', 'China', 'Japan', 'Germany', 'United Kingdom', 
        'France', 'India', 'Brazil', 'Canada', 'Australia', 'Russia',
        'South Korea', 'Mexico', 'Indonesia', 'Netherlands', 'Saudi Arabia',
        'Turkey', 'Switzerland', 'Argentina', 'South Africa', 'Nigeria',
        'Egypt', 'Pakistan', 'Bangladesh', 'Vietnam', 'Thailand', 'Malaysia',
        'Singapore', 'Philippines', 'New Zealand', 'Chile', 'Colombia',
        'Peru', 'Venezuela', 'Ukraine', 'Poland', 'Sweden', 'Norway',
        'Denmark', 'Finland', 'Italy', 'Spain', 'Portugal', 'Greece',
        'Ireland', 'Austria', 'Belgium', 'Czech Republic', 'Hungary'
    ]
    
    # Generate realistic inflation rates
    inflation_rates = []
    for country in countries:
        # Different base rates for different economic conditions
        if country in ['United States', 'Germany', 'Japan', 'Switzerland']:
            base_rate = np.random.uniform(2.0, 4.0)
        elif country in ['Turkey', 'Argentina', 'Venezuela']:
            base_rate = np.random.uniform(15.0, 45.0)
        elif country in ['United Kingdom', 'Canada', 'Australia']:
            base_rate = np.random.uniform(3.0, 6.0)
        elif country in ['India', 'Brazil', 'South Africa']:
            base_rate = np.random.uniform(4.0, 8.0)
        else:
            base_rate = np.random.uniform(2.0, 7.0)
        
        inflation_rates.append(round(base_rate, 1))
    
    return pd.DataFrame({
        'Country': countries,
        'Inflation Rate': inflation_rates,
        'ISO_Code': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'IND', 'BRA', 'CAN', 'AUS', 
                    'RUS', 'KOR', 'MEX', 'IDN', 'NLD', 'SAU', 'TUR', 'CHE', 'ARG', 'ZAF',
                    'NGA', 'EGY', 'PAK', 'BGD', 'VNM', 'THA', 'MYS', 'SGP', 'PHL', 'NZL',
                    'CHL', 'COL', 'PER', 'VEN', 'UKR', 'POL', 'SWE', 'NOR', 'DNK', 'FIN',
                    'ITA', 'ESP', 'PRT', 'GRC', 'IRL', 'AUT', 'BEL', 'CZE', 'HUN']
    })

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

# Generate global inflation data
inflation_data = generate_global_inflation_data()

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
    
    # Create the choropleth map
    fig = px.choropleth(
        inflation_data,
        locations="ISO_Code",
        color="Inflation Rate",
        hover_name="Country",
        hover_data={"Inflation Rate": ":.1f%", "ISO_Code": False},
        color_continuous_scale="Blues",
        range_color=[0, 40],  # Cap at 40% for better visualization
        title="Global Inflation Rates (%)",
        height=400
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
        font=dict(color='white'),
        coloraxis_colorbar=dict(
            title="Inflation %",
            thickness=15,
            len=0.75,
            yanchor="
