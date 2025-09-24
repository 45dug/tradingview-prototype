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

# Advanced CSS with all new features
st.markdown("""
<style>
    /* Main TradingView Theme with Wallpaper */
    .main { 
        background: linear-gradient(135deg, #0c2461 0%, #1e3799 50%, #4a69bd 100%);
        color: #d1d4dc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        min-height: 100vh;
    }
    
    /* Wallpaper effect with subtle pattern */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 20%);
        z-index: -1;
    }
    
    /* Header Styling - Look First / Then Leap */
    .header-container {
        background: rgba(30, 34, 45, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #2962ff;
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #2962ff, #00acc1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        text-align: center;
        color: #b0b3b8;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .cta-button {
        background: linear-gradient(45deg, #2962ff, #00acc1);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        text-decoration: none;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(41, 98, 255, 0.4);
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(30, 34, 45, 0.9);
        backdrop-filter: blur(10px);
        padding: 0.8rem 2rem;
        margin: -2rem -1rem 1rem -1rem;
        border-bottom: 1px solid #2a2e39;
        display: flex;
        justify-content: space-between;
        align-items: center;
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
    }
    
    .nav-item:hover {
        color: #2962ff;
    }
    
    .search-box {
        background: rgba(42, 46, 57, 0.8);
        border: 1px solid #3a3e49;
        border-radius: 20px;
        padding: 8px 15px;
        color: #d1d4dc;
        width: 200px;
    }
    
    /* Forex Rates Section */
    .forex-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .currency-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
        margin: 15px 0;
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
    
    .currency-item.active {
        background: #2962ff;
        color: white;
    }
    
    .timeframe-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 5px;
        margin: 15px 0;
    }
    
    .timeframe-btn {
        background: rgba(42, 46, 57, 0.6);
        color: #d1d4dc;
        border: none;
        border-radius: 4px;
        padding: 8px 5px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .timeframe-btn.active {
        background: #2962ff;
        color: white;
    }
    
    /* News Section */
    .news-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .news-item {
        background: rgba(42, 46, 57, 0.6);
        padding: 15px;
        margin: 10px 0;
        border-radius: 6px;
        border-left: 3px solid #2962ff;
    }
    
    .news-time {
        color: #8c9baf;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .news-headline {
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .news-source {
        color: #26a69a;
        font-size: 0.8rem;
    }
    
    /* Economy Section */
    .economy-section {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
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
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: rgba(30, 34, 45, 0.9);
        color: #d1d4dc;
        backdrop-filter: blur(10px);
    }
    
    /* Professional Cards */
    .card {
        background: rgba(30, 34, 45, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #2962ff;
        backdrop-filter: blur(5px);
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
    
    # Generate realistic price movement with volatility
    returns = np.random.normal(0, 0.002, points)
    prices = base_price * np.exp(np.cumsum(returns))
    
    # Create OHLC data
    opens = []
    highs = []
    lows = []
    closes = []
    
    for i in range(points):
        if i == 0:
            open_price = base_price
        else:
            open_price = closes[i-1] if closes else base_price
            
        close_price = prices[i]
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005)))
        
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': opens, 'high': highs, 'low': lows, 'close': closes,
        'volume': np.random.randint(1000000, 5000000, points)
    })
    
    return df

# Calculate technical indicators
def calculate_indicators(df):
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df

# Generate forex news data
def generate_forex_news():
    return [
        {"time": "yesterday - Dow Jones Newswires", "headline": "Sterling Gains 0.31% to $1.3514 — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "The WSJ Dollar Index Falls 0.23% to 94.77 — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Loses 0.17% to 147.72 Yen — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Gains 0.27% to 1.3819 Canadian Dollars — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Euro Gains 0.49% to $1.1804 — Data Talk", "source": "DJN"},
        {"time": "yesterday - Dow Jones Newswires", "headline": "Dollar Loses 0.27% to 18.3585 Mexican Pesos — Data Talk", "source": "DJN"},
        {"time": "yesterday - Reuters", "headline": "Brazil's central bank to auction up to $2 billion with repurchase deal", "source": "Reuters"},
        {"time": "2 days ago - Bloomberg", "headline": "New Zealand to make an announcement related to central bank on Wednesday", "source": "Bloomberg"}
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

# Calculate indicators
st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)

# Header Section - Look First / Then Leap
st.markdown("""
<div class="header-container">
    <div class="header-title">Look First / Then Leap</div>
    <div class="header-subtitle">The best trades require research, then commitment.</div>
    <a href="#trading-section" class="cta-button">Get started for free</a>
    <div style="text-align: center; margin-top: 10px; font-size: 0.9rem; color: #8c9baf;">
        $0 forever, no credit card needed
    </div>
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
        <button class="cta-button" style="padding: 8px 20px; font-size: 0.9rem;">Get started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Forex Rates Section
    st.markdown("""
    <div class="forex-section">
        <h3>💱 Forex Rates</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h4>Base Currency: {}</h4>
            <div style="color: #8c9baf; font-size: 0.9rem;">See all rates ></div>
        </div>
    </div>
    """.format(st.session_state.base_currency), unsafe_allow_html=True)
    
    # Base Currency Selection
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
    
    # Quote Currencies Display
    st.markdown("#### Quote Currencies")
    quote_currencies = ["USD", "GBP", "JPY", "CHF", "AUD", "CNY", "CAD"]
    quote_cols = st.columns(7)
    
    for i, currency in enumerate(quote_currencies):
        with quote_cols[i]:
            if currency != st.session_state.base_currency:
                # Generate realistic exchange rate
                if st.session_state.base_currency == "EUR":
                    rate = np.random.uniform(0.8, 1.5)
                elif currency == "JPY":
                    rate = np.random.uniform(100, 150)
                else:
                    rate = np.random.uniform(0.7, 2.0)
                
                change = np.random.uniform(-0.02, 0.02)
                change_pct = change * 100
                
                st.metric(
                    label=currency,
                    value=f"{rate:.4f}",
                    delta=f"{change_pct:+.2f}%",
                    delta_color="normal"
                )
    
    # Timeframe Selection
    st.markdown("#### Timeframe")
    timeframes = ["1D", "1W", "1M", "3M", "6M", "1Y", "YTD", "5Y", "All"]
    tf_cols = st.columns(9)
    
    for i, tf in enumerate(timeframes):
        with tf_cols[i]:
            if st.button(tf, key=f"time_{tf}", use_container_width=True):
                st.session_state.timeframe = tf
                st.rerun()
    
    # Main Chart Display
    st.markdown("### 📈 Advanced Chart")
    
    # Use Streamlit's native charting instead of Plotly
    chart_data = st.session_state.chart_data.set_index('timestamp')[['close', 'sma_20', 'sma_50']]
    st.line_chart(chart_data, height=500)

with col2:
    # Forex News Section
    st.markdown("""
    <div class="news-section">
        <h3>📰 Forex News</h3>
        <div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">
            Sign in to read exclusive news >
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    news_data = generate_forex_news()
    
    for i, news in enumerate(news_data[:4]):  # Show first 4 news items
        st.markdown(f"""
        <div class="news-item">
            <div class="news-time">{news['time']}</div>
            <div class="news-headline">{news['headline']}</div>
            <div class="news-source">{news['source']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Keep reading >", key="keep_reading", use_container_width=True):
        st.session_state.show_more_news = not st.session_state.show_more_news
        st.rerun()
    
    if st.session_state.show_more_news:
        for i, news in enumerate(news_data[4:]):
            st.markdown(f"""
            <div class="news-item">
                <div class="news-time">{news['time']}</div>
                <div class="news-headline">{news['headline']}</div>
                <div class="news-source">{news['source']}</div>
            </div>
            """, unsafe_allow_html=True)

with col3:
    # Economy Section
    st.markdown("""
    <div class="economy-section">
        <h3>🌍 Economy</h3>
        <div style="color: #8c9baf; font-size: 0.9rem; margin-bottom: 15px;">
            Global inflation map >
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inflation Legend
    st.markdown("""
    <div class="inflation-legend">
        <div class="legend-item" style="background: #1a237e; color: white;">Less than 0%</div>
        <div class="legend-item" style="background: #283593; color: white;">0-3%</div>
        <div class="legend-item" style="background: #303f9f; color: white;">3-7%</div>
        <div class="legend-item" style="background: #5c6bc0; color: white;">7-12%</div>
        <div class="legend-item" style="background: #7986cb; color: white;">12-25%</div>
        <div class="legend-item" style="background: #9fa8da; color: #1a237e;">More than 25%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple inflation data display (replacing the map)
    inflation_data = {
        "USA": 3.2, "UK": 4.1, "Germany": 2.8, "France": 3.5, 
        "Japan": 2.1, "Canada": 3.8, "Australia": 4.2, "Brazil": 8.5
    }
    
    for country, rate in inflation_data.items():
        color = "#26a69a" if rate < 3 else "#ffa726" if rate < 7 else "#ef5350"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px; background: rgba(42,46,57,0.6); margin: 5px 0; border-radius: 4px;">
            <span>{country}</span>
            <span style="color: {color}; font-weight: 600;">{rate}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Products Section
    st.markdown("""
    <div class="news-section">
        <h3>📦 Products</h3>
    </div>
    """, unsafe_allow_html=True)
    
    products = [
        {"name": "Product Sheet", "year": "2022", "time": "15:00"},
        {"name": "Community Marks", "year": "", "time": "15:00"},
        {"name": "Markets Brokers More", "year": "", "time": "10:00"}
    ]
    
    for product in products:
        st.markdown(f"""
        <div class="news-item">
            <div class="news-headline">{product['name']}</div>
            <div style="display: flex; justify-content: space-between;">
                <div class="news-source">{product['year']}</div>
                <div class="news-time">{product['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Trading Panel at the bottom
st.markdown("### 🎯 Trading Panel")

tcol1, tcol2, tcol3, tcol4, tcol5, tcol6, tcol7 = st.columns(7)

with tcol1:
    live_icon = "⏸️" if st.session_state.is_live else "▶️"
    if st.button(live_icon, help="Live Trading Mode", use_container_width=True):
        st.session_state.is_live = not st.session_state.is_live
        st.rerun()

with tcol2:
    if st.button("🔄", help="Refresh Data", use_container_width=True):
        st.session_state.chart_data = generate_advanced_data(st.session_state.current_symbol)
        st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
        st.rerun()

with tcol6:
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        current_data = st.session_state.chart_data.iloc[-1]
        quantity = 100
        order_value = quantity * current_data['close']
        st.success(f"✅ BUY {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

with tcol7:
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        current_data = st.session_state.chart_data.iloc[-1]
        quantity = 100
        order_value = quantity * current_data['close']
        st.error(f"✅ SELL {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.4f}")

# Live data simulation
if st.session_state.is_live:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(10):
        if not st.session_state.is_live:
            break
            
        # Generate new data point
        last_close = st.session_state.chart_data['close'].iloc[-1]
        new_return = np.random.normal(0, 0.0015)
        new_close = last_close * (1 + new_return)
        
        new_row = pd.DataFrame({
            'timestamp': [datetime.now()],
            'open': [last_close],
            'high': [max(last_close, new_close) * (1 + abs(np.random.normal(0, 0.002)))],
            'low': [min(last_close, new_close) * (1 - abs(np.random.normal(0, 0.002)))],
            'close': [new_close],
            'volume': [np.random.randint(1000000, 3000000)]
        })
        
        st.session_state.chart_data = pd.concat([
            st.session_state.chart_data.iloc[1:],
            new_row
        ], ignore_index=True)
        
        st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
        
        progress_bar.progress((i + 1) / 10)
        current_change = (new_close - last_close) / last_close * 100
        status_text.text(f"📡 Live: {st.session_state.current_symbol} | ${new_close:.4f} | {current_change:+.2f}%")
        time.sleep(1)
    
    progress_bar.empty()
    status_text.empty()
    st.session_state.is_live = False
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d;'>
    <p>TradeLeap Pro • Look First, Then Leap • Real-time Data • Professional Charts</p>
    <p>© 2025 TradeLeap. All rights reserved. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
