import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView - Where the world does markets",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== EXACT TRADINGVIEW CSS =====
st.markdown("""
<style>
    /* Exact TradingView Styles */
    .main { 
        background-color: #ffffff !important; 
        color: #131722 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header Bar */
    .header-bar {
        background: linear-gradient(90deg, #2962FF 0%, #00B7D4 100%);
        padding: 12px 0;
        color: white;
        text-align: center;
        font-weight: 500;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #2962FF 0%, #00B7D4 100%);
        padding: 100px 20px;
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    .cta-button {
        background: white;
        color: #2962FF;
        border: none;
        padding: 16px 40px;
        font-size: 1.1rem;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        padding: 60px 20px;
    }
    
    .feature-card {
        text-align: center;
        padding: 30px;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: #131722;
    }
    
    .feature-desc {
        color: #5e6673;
        line-height: 1.6;
    }
    
    /* Market Data Section */
    .market-section {
        background: #f8f9fa;
        padding: 60px 20px;
    }
    
    .market-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .market-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .market-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #5e6673;
        margin-bottom: 15px;
    }
    
    .market-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #131722;
        margin-bottom: 8px;
    }
    
    .market-change {
        font-weight: 600;
        font-size: 1rem;
    }
    
    .change-positive { color: #26a69a; }
    .change-negative { color: #ef5350; }
    
    /* Footer */
    .footer {
        background: #131722;
        color: white;
        padding: 40px 20px;
        text-align: center;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .features-grid { grid-template-columns: 1fr; }
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ===== TRADINGVIEW EXACT LAYOUT =====

# Header Bar
st.markdown("""
<div class="header-bar">
    Join 100M+ traders and investors - Start free today →
</div>
""", unsafe_allow_html=True)

# Hero Section (EXACT TradingView replica)
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Where the world does markets</h1>
    <p class="hero-subtitle">Join 100 million traders and investors taking the future into their own hands.</p>
    <button class="cta-button">Get started for free</button>
    <p style="margin-top: 20px; opacity: 0.9; font-size: 0.95rem;">$0 forever, no credit card needed</p>
</div>
""", unsafe_allow_html=True)

# Features Grid
st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3 class="feature-title">Advanced Charts</h3>
        <p class="feature-desc">Professional trading charts with 100+ indicators and drawing tools</p>
    </div>
    
    <div class="feature-card">
        <div class="feature-icon">📱</div>
        <h3 class="feature-title">Real-time Data</h3>
        <p class="feature-desc">Live market data for stocks, crypto, forex, and indices</p>
    </div>
    
    <div class="feature-card">
        <div class="feature-icon">🤝</div>
        <h3 class="feature-title">Social Trading</h3>
        <p class="feature-desc">Follow top traders and share ideas with our community</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Market Data Section (EXACT TradingView style)
st.markdown("""
<div class="market-section">
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="color: #131722; font-size: 2rem; font-weight: 700;">Live Market Overview</h2>
        <p style="color: #5e6673; font-size: 1.1rem;">Real-time market data across all asset classes</p>
    </div>
    
    <div class="market-grid">
        <div class="market-card">
            <div class="market-title">Crypto Market Cap</div>
            <div class="market-value">3.91T USD</div>
            <div class="market-change change-negative">-1.26% today</div>
        </div>
        
        <div class="market-card">
            <div class="market-title">US Dollar Index</div>
            <div class="market-value">97.789 USD</div>
            <div class="market-change change-positive">+0.15% today</div>
        </div>
        
        <div class="market-card">
            <div class="market-title">Crude Oil</div>
            <div class="market-value">62.77 USD/BLL</div>
            <div class="market-change change-positive">+0.59%</div>
        </div>
        
        <div class="market-card">
            <div class="market-title">FTSE 100</div>
            <div class="market-value">9,216.67</div>
            <div class="market-change change-negative">-0.12%</div>
        </div>
        
        <div class="market-card">
            <div class="market-title">DAX</div>
            <div class="market-value">23,639.41</div>
            <div class="market-change change-negative">-0.15%</div>
        </div>
        
        <div class="market-card">
            <div class="market-title">CAC 40</div>
            <div class="market-value">7,853.59</div>
            <div class="market-change change-negative">-0.01%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Final CTA Section
st.markdown("""
<div style="text-align: center; padding: 80px 20px; background: white;">
    <h2 style="color: #131722; font-size: 2.2rem; font-weight: 700; margin-bottom: 20px;">Look first / Then leap.</h2>
    <p style="color: #5e6673; font-size: 1.2rem; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
        The best trades require research, then commitment.
    </p>
    <button class="cta-button" style="background: #2962FF; color: white;">Start Trading Now</button>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="opacity: 0.8; margin-bottom: 20px;">Scott "Kidd" Poteet • The unlikely astronaut • Watch explainer</p>
    <p style="opacity: 0.6; font-size: 0.9rem;">© 2025 TradingView. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

# ===== SIMPLE requirements.txt =====
# Keep your requirements.txt as:
# streamlit
# pandas
# numpy
