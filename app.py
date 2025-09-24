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
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()

# Enhanced CSS with new sections
st.markdown("""
<style>
    /* Hero Section */
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
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
    }
    
    /* Section Styling */
    .content-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .section-title {
        color: #2962ff;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #2962ff;
        padding-left: 15px;
    }
    
    /* Market Overview Cards */
    .market-card {
        background: rgba(42, 46, 57, 0.6);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        transition: all 0.3s ease;
        border-left: 4px solid;
    }
    
    .market-card:hover {
        transform: translateY(-3px);
        background: rgba(58, 62, 73, 0.8);
    }
    
    /* Educational Content */
    .edu-card {
        background: linear-gradient(135deg, rgba(41, 98, 255, 0.1), rgba(0, 172, 193, 0.1));
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid rgba(41, 98, 255, 0.3);
    }
    
    /* Performance Metrics */
    .metric-large {
        font-size: 2rem;
        font-weight: 700;
        color: #2962ff;
    }
    
    /* News Ticker */
    .news-ticker {
        background: rgba(41, 98, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #2962ff;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data generation functions
def generate_advanced_data(symbol, points=200):
    np.random.seed(hash(symbol) % 100)
    base_prices = {
        "AAPL": 180, "TSLA": 250, "MSFT": 420, "GOOGL": 2800, "BTCUSD": 65000, 
        "SPX": 5200, "NVDA": 120, "AMZN": 3500, "EURUSD": 1.08, "GBPUSD": 1.26
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
        'timestamp': dates, 'open': opens, 'high': highs, 'low': lows, 'close': closes,
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

def generate_market_overview():
    return {
        "US Markets": {"change": +0.45, "status": "Bullish", "volume": "High"},
        "European Markets": {"change": -0.23, "status": "Neutral", "volume": "Medium"},
        "Asian Markets": {"change": +1.2, "status": "Bullish", "volume": "High"},
        "Cryptocurrency": {"change": +3.4, "status": "Very Bullish", "volume": "Very High"},
        "Commodities": {"change": -0.8, "status": "Bearish", "volume": "Medium"}
    }

def generate_educational_content():
    return [
        {
            "title": "Understanding Technical Analysis",
            "level": "Beginner",
            "duration": "15 min",
            "content": "Learn how to read charts, identify trends, and use technical indicators to make informed trading decisions."
        },
        {
            "title": "Risk Management Strategies",
            "level": "Intermediate", 
            "duration": "25 min",
            "content": "Discover essential risk management techniques to protect your capital and maximize returns."
        },
        {
            "title": "Advanced Chart Patterns",
            "level": "Advanced",
            "duration": "30 min",
            "content": "Master complex chart patterns and their implications for price movement predictions."
        }
    ]

def generate_trading_ideas():
    return [
        {"symbol": "AAPL", "idea": "BUY", "confidence": 85, "reason": "Breaking resistance with high volume"},
        {"symbol": "TSLA", "idea": "HOLD", "confidence": 65, "reason": "Consolidating before earnings"},
        {"symbol": "BTCUSD", "idea": "BUY", "confidence": 78, "reason": "Bullish divergence on daily chart"},
        {"symbol": "EURUSD", "idea": "SELL", "confidence": 72, "reason": "Dollar strength continuing"}
    ]

def generate_economic_calendar():
    events = []
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        events.append({
            "date": date.strftime("%b %d"),
            "event": ["Fed Meeting", "CPI Release", "Employment Data", "GDP Report", "Retail Sales"][i % 5],
            "impact": ["High", "Medium", "High", "Medium", "Low"][i % 5],
            "forecast": f"{np.random.uniform(0.1, 0.5):.1f}%"
        })
    return events

# Initialize session state
if 'current_symbol' not in st.session_state:
    st.session_state.update({
        'current_symbol': "EURUSD",
        'chart_data': generate_advanced_data("EURUSD"),
        'is_live': False,
        'timeframe': "1D",
        'base_currency': "EUR",
        'show_more_news': False,
        'portfolio_value': 50000,
        'watchlist': ["AAPL", "TSLA", "MSFT", "GOOGL", "BTCUSD"]
    })

st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)

# ===== HERO SECTION =====
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

# ===== MARKET OVERVIEW SECTION =====
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌍 Live Market Overview</div>', unsafe_allow_html=True)

market_data = generate_market_overview()
cols = st.columns(5)
for i, (market, data) in enumerate(market_data.items()):
    with cols[i]:
        change_color = "green" if data["change"] >= 0 else "red"
        st.markdown(f"""
        <div class="market-card">
            <h4>{market}</h4>
            <div class="metric-large" style="color: {change_color};">{data['change']:+.2f}%</div>
            <div>Status: {data['status']}</div>
            <div>Volume: {data['volume']}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== MAIN TRADING INTERFACE =====
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 💱 Advanced Trading Platform")
    
    # Forex Rates
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
    
    # Chart Display
    st.markdown("#### 📈 Live Chart Analysis")
    chart_data = st.session_state.chart_data.set_index('timestamp')[['close', 'sma_20', 'sma_50']]
    st.line_chart(chart_data, height=400)
    
    # Technical Analysis
    st.markdown("#### 🔍 Technical Indicators")
    col1, col2, col3, col4 = st.columns(4)
    current_data = st.session_state.chart_data.iloc[-1]
    
    with col1:
        st.metric("RSI", f"{current_data['rsi']:.1f}")
    with col2:
        st.metric("Trend", "Bullish" if current_data['close'] > current_data['sma_50'] else "Bearish")
    with col3:
        volatility = (current_data['high'] - current_data['low']) / current_data['low'] * 100
        st.metric("Volatility", f"{volatility:.2f}%")
    with col4:
        st.metric("Volume", f"{current_data['volume']/1000000:.1f}M")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 📰 Market News & Analysis")
    
    news_items = [
        "Fed holds rates steady, signals potential cuts in Q3 2024",
        "Tech stocks rally on strong earnings reports",
        "Oil prices surge amid Middle East tensions", 
        "Bitcoin breaks $70,000 as institutional adoption grows",
        "Eurozone inflation falls faster than expected"
    ]
    
    for news in news_items:
        st.markdown(f"""
        <div class="news-ticker">
            <div style="font-weight: 600; margin-bottom: 5px;">{news}</div>
            <div style="color: #8c9baf; font-size: 0.8rem;">2 hours ago • Reuters</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown("### 💡 Trading Ideas")
    
    ideas = generate_trading_ideas()
    for idea in ideas:
        confidence_color = "#26a69a" if idea["confidence"] > 75 else "#ffa726" if idea["confidence"] > 60 else "#ef5350"
        st.markdown(f"""
        <div class="market-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4>{idea['symbol']}</h4>
                <span style="background: {confidence_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                    {idea['idea']}
                </span>
            </div>
            <div>Confidence: <strong>{idea['confidence']}%</strong></div>
            <div style="font-size: 0.9rem; color: #8c9baf;">{idea['reason']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== EDUCATIONAL CONTENT SECTION =====
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎓 Learning Center</div>', unsafe_allow_html=True)

edu_content = generate_educational_content()
cols = st.columns(3)

for i, lesson in enumerate(edu_content):
    with cols[i]:
        st.markdown(f"""
        <div class="edu-card">
            <h4>{lesson['title']}</h4>
            <div style="display: flex; gap: 10px; margin: 10px 0;">
                <span style="background: #2962ff; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                    {lesson['level']}
                </span>
                <span style="background: #26a69a; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                    {lesson['duration']}
                </span>
            </div>
            <p>{lesson['content']}</p>
            <button style="background: #2962ff; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                Start Learning
            </button>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== ECONOMIC CALENDAR SECTION =====
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📅 Economic Calendar</div>', unsafe_allow_html=True)

calendar_events = generate_economic_calendar()
for event in calendar_events[:5]:  # Show next 5 events
    impact_color = "#ef5350" if event["impact"] == "High" else "#ffa726" if event["impact"] == "Medium" else "#26a69a"
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; background: rgba(42,46,57,0.6); margin: 8px 0; border-radius: 8px;">
        <div style="font-weight: 600; width: 100px;">{event['date']}</div>
        <div style="flex: 1;">{event['event']}</div>
        <div style="background: {impact_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem;">
            {event['impact']} Impact
        </div>
        <div style="width: 80px; text-align: right;">{event['forecast']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== PORTFOLIO PERFORMANCE SECTION =====
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💼 Portfolio Performance</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Value", f"${st.session_state.portfolio_value:,.2f}")
with col2:
    st.metric("Today's Change", "+$1,234.56", "+2.47%")
with col3:
    st.metric("YTD Performance", "+15.8%")
with col4:
    st.metric("Risk Level", "Moderate")

# Portfolio holdings
holdings = [
    {"symbol": "AAPL", "shares": 50, "avg_price": 150.25, "current": 182.35},
    {"symbol": "TSLA", "shares": 25, "avg_price": 220.80, "current": 248.90},
    {"symbol": "BTCUSD", "shares": 0.5, "avg_price": 58000, "current": 65123.45}
]

st.markdown("#### Current Holdings")
for holding in holdings:
    profit_loss = (holding['current'] - holding['avg_price']) * holding['shares']
    pct_change = (holding['current'] - holding['avg_price']) / holding['avg_price'] * 100
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 10px; background: rgba(42,46,57,0.6); margin: 5px 0; border-radius: 5px;">
        <div><strong>{holding['symbol']}</strong> - {holding['shares']} shares</div>
        <div style="color: {'#26a69a' if profit_loss >= 0 else '#ef5350'}">
            ${profit_loss:+.2f} ({pct_change:+.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===== TRADING PANEL =====
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

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d; padding: 2rem;'>
    <h3>Start Your Trading Journey Today</h3>
    <p>Join thousands of successful traders who use TradeLeap to make informed decisions</p>
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
