import streamlit as st
import pandas as pd
import numpy as np

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView - Where the world does markets",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CLEAN, PROFESSIONAL CSS =====
st.markdown("""
<style>
    /* Clean modern reset */
    .main { 
        background-color: #ffffff; 
        color: #131722;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Remove Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Simple clean sections */
    .section {
        padding: 80px 20px;
        text-align: center;
    }
    
    .hero {
        background: linear-gradient(135deg, #2962FF 0%, #2196F3 100%);
        color: white;
    }
    
    .features {
        background: #ffffff;
    }
    
    .markets {
        background: #f8f9fa;
    }
    
    /* Typography */
    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    h2 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Buttons */
    .btn {
        display: inline-block;
        background: white;
        color: #2962FF;
        padding: 15px 40px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        margin: 10px;
    }
    
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Simple grid */
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    .card {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .market-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        text-align: left;
        border-left: 4px solid #2962FF;
    }
    
    /* Colors */
    .positive { color: #26a69a; font-weight: 600; }
    .negative { color: #ef5350; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ===== SIMPLE, CLEAN LAYOUT =====

# Hero Section
st.markdown("""
<div class="section hero">
    <h1>Where the world does markets</h1>
    <p class="subtitle">Join 100 million traders and investors taking the future into their own hands.</p>
    <button class="btn">Get started for free</button>
    <p style="margin-top: 20px; opacity: 0.9;">$0 forever, no credit card needed</p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="section features">
    <h2>Look first / Then leap.</h2>
    <p class="subtitle">The best trades require research, then commitment.</p>
    
    <div class="grid-3">
        <div class="card">
            <h3>📊 Advanced Charts</h3>
            <p>Professional trading charts with indicators and drawing tools</p>
        </div>
        
        <div class="card">
            <h3>📱 Real-time Data</h3>
            <p>Live market data for stocks, crypto, forex, and indices</p>
        </div>
        
        <div class="card">
            <h3>🤝 Social Trading</h3>
            <p>Follow top traders and share ideas with our community</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Markets Section
st.markdown("""
<div class="section markets">
    <h2>Live Market Overview</h2>
    
    <div class="grid-3">
        <div class="market-card">
            <h4>Crypto Market Cap</h4>
            <h3>3.91T USD</h3>
            <p class="negative">-1.26% today</p>
        </div>
        
        <div class="market-card">
            <h4>US Dollar Index</h4>
            <h3>97.789 USD</h3>
            <p class="positive">+0.15% today</p>
        </div>
        
        <div class="market-card">
            <h4>Crude Oil</h4>
            <h3>62.77 USD/BLL</h3>
            <p class="positive">+0.59%</p>
        </div>
        
        <div class="market-card">
            <h4>FTSE 100</h4>
            <h3>9,216.67</h3>
            <p class="negative">-0.12%</p>
        </div>
        
        <div class="market-card">
            <h4>DAX</h4>
            <h3>23,639.41</h3>
            <p class="negative">-0.15%</p>
        </div>
        
        <div class="market-card">
            <h4>CAC 40</h4>
            <h3>7,853.59</h3>
            <p class="negative">-0.01%</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px; background: #131722; color: white;">
    <p>Scott "Kidd" Poteet • The unlikely astronaut • Watch explainer</p>
    <p style="opacity: 0.7; margin-top: 10px;">© 2025 TradingView. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
