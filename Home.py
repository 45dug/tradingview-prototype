import streamlit as st

st.set_page_config(page_title="TradingView - Where the world does markets", layout="wide")

# TradingView Style CSS
st.markdown("""
<style>
    .main { background-color: #000000; color: white; }
    .hero { text-align: center; padding: 80px 20px; background: linear-gradient(135deg, #000000 0%, #131722 100%); }
    .hero h1 { font-size: 4rem; font-weight: 700; margin-bottom: 20px; background: linear-gradient(135deg, #2962ff 0%, #00bcd4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero p { font-size: 1.5rem; opacity: 0.9; margin-bottom: 40px; }
    .cta-button { background: linear-gradient(135deg, #2962ff 0%, #00bcd4 100%); border: none; padding: 15px 40px; font-size: 1.2rem; border-radius: 30px; color: white; font-weight: 600; }
    .feature-card { background-color: #1e222d; padding: 30px; border-radius: 15px; margin: 10px; }
    .market-card { background-color: #1e222d; padding: 20px; border-radius: 10px; margin: 10px; }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>Where the world does markets</h1>
    <p>Join 100 million traders and investors taking the future into their own hands.</p>
    <a href="/Trading_Platform" target="_self">
        <button class="cta-button">Get started for free</button>
    </a>
    <p style="margin-top: 20px; font-size: 1rem; opacity: 0.7;">$0 forever, no credit card needed</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>Look first / Then leap.</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>The best trades require research, then commitment.</p>", unsafe_allow_html=True)

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

# Crypto Market
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="market-card">
        <h4>💰 Crypto Market Cap</h4>
        <h3>3.91T USD</h3>
        <p style='color: #ef5350;'>–1.26% today</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="market-card">
        <h4>📊 US Dollar Index</h4>
        <h3>97.789 USD</h3>
        <p style='color: #26a69a;'>+0.15% today</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="market-card">
        <h4>🛢️ Crude Oil</h4>
        <h3>62.77 USD/BLL</h3>
        <p style='color: #26a69a;'>+0.59%</p>
    </div>
    """, unsafe_allow_html=True)

# Stock Indices
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="market-card">
        <h4>🇬🇧 FTSE 100</h4>
        <h3>9,216.67</h3>
        <p style='color: #ef5350;'>–0.12%</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="market-card">
        <h4>🇩🇪 DAX</h4>
        <h3>23,639.41</h3>
        <p style='color: #ef5350;'>–0.15%</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="market-card">
        <h4>🇫🇷 CAC 40</h4>
        <h3>7,853.59</h3>
        <p style='color: #ef5350;'>–0.01%</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 40px;'>
    <p style='opacity: 0.7;'>The unlikely astronaut • Watch explainer</p>
    <p style='opacity: 0.5;'>© 2025 TradingView Clone. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
