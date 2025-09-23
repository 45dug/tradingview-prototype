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

# ===== PIXEL-PERFECT TRADINGVIEW CSS =====
st.markdown("""
<style>
    /* Reset and base styles */
    .main { 
        background-color: #ffffff !important; 
        color: #131722 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
    }
    
    /* TradingView Top Banner */
    .top-banner {
        background: linear-gradient(90deg, #2962FF 0%, #2196F3 100%);
        padding: 8px 0;
        text-align: center;
        color: white;
        font-weight: 500;
        font-size: 14px;
    }
    
    /* Main Navigation */
    .main-nav {
        background: white;
        padding: 16px 0;
        border-bottom: 1px solid #e3e4eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
    }
    
    .logo {
        font-size: 24px;
        font-weight: 800;
        color: #2962FF;
        text-decoration: none;
    }
    
    .nav-links {
        display: flex;
        gap: 32px;
        font-weight: 500;
    }
    
    .nav-links a {
        color: #131722;
        text-decoration: none;
        font-size: 14px;
    }
    
    .nav-links a:hover {
        color: #2962FF;
    }
    
    /* Hero Section - Exact TradingView Style */
    .hero {
        background: linear-gradient(135deg, #2962FF 0%, #2196F3 100%);
        padding: 120px 0;
        text-align: center;
        color: white;
    }
    
    .hero-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .hero h1 {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 24px;
        line-height: 1.1;
    }
    
    .hero p {
        font-size: 20px;
        opacity: 0.95;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    .cta-button {
        background: white;
        color: #2962FF;
        border: none;
        padding: 16px 48px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Features Section */
    .features {
        padding: 80px 0;
        background: white;
    }
    
    .features-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 32px;
        margin-top: 48px;
    }
    
    .feature-card {
        text-align: center;
        padding: 32px;
        border-radius: 12px;
        background: #f8f9fa;
        transition: all 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 40px;
        margin-bottom: 20px;
        color: #2962FF;
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 16px;
        color: #131722;
    }
    
    .feature-desc {
        color: #5e6673;
        line-height: 1.6;
        font-size: 16px;
    }
    
    /* Market Data Section */
    .market-section {
        background: #f8f9fa;
        padding: 80px 0;
    }
    
    .market-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .market-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin-top: 48px;
    }
    
    .market-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #2962FF;
    }
    
    .market-title {
        font-size: 14px;
        font-weight: 600;
        color: #5e6673;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .market-value {
        font-size: 24px;
        font-weight: 700;
        color: #131722;
        margin-bottom: 8px;
    }
    
    .market-change {
        font-weight: 600;
        font-size: 14px;
    }
    
    .change-positive { color: #26a69a; }
    .change-negative { color: #ef5350; }
    
    /* Footer */
    .footer {
        background: #131722;
        color: white;
        padding: 60px 0 40px;
        text-align: center;
    }
    
    .footer p {
        opacity: 0.8;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .features-grid { grid-template-columns: 1fr; gap: 24px; }
        .hero h1 { font-size: 36px; }
        .hero p { font-size: 18px; }
        .market-grid { grid-template-columns: 1fr; }
        .nav-links { display: none; }
    }
</style>
""", unsafe_allow_html=True)

# ===== EXACT TRADINGVIEW LAYOUT =====

# Top Banner
st.markdown("""
<div class="top-banner">
    Join 100M+ traders and investors - Start free today →
</div>
""", unsafe_allow_html=True)

# Main Navigation
st.markdown("""
<div class="main-nav">
    <div class="nav-container">
        <a href="#" class="logo">TradingView</a>
        <div class="nav-links">
            <a href="#">Products</a>
            <a href="#">Charts</a>
            <a href="#">Screener</a>
            <a href="#">Community</a>
            <a href="#">Markets</a>
            <a href="#">Brokers</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>Where the world does markets</h1>
        <p>Join 100 million traders and investors taking the future into their own hands.</p>
        <a href="#" class="cta-button">Get started for free</a>
        <p style="margin-top: 20px; opacity: 0.9; font-size: 14px;">$0 forever, no credit card needed</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="features">
    <div class="features-container">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 32px; font-weight: 700; color: #131722; margin-bottom: 16px;">Look first / Then leap.</h2>
            <p style="font-size: 18px; color: #5e6673; max-width: 600px; margin: 0 auto;">The best trades require research, then commitment.</p>
        </div>
        
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
    </div>
</div>
""", unsafe_allow_html=True)

# Market Data Section
st.markdown("""
<div class="market-section">
    <div class="market-container">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 32px; font-weight: 700; color: #131722; margin-bottom: 16px;">Live Market Overview</h2>
            <p style="font-size: 18px; color: #5e6673;">Real-time market data across all asset classes</p>
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
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Scott "Kidd" Poteet • The unlikely astronaut • Watch explainer</p>
    <p style="margin-top: 20px; opacity: 0.6;">© 2025 TradingView. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
