import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="AlgoCheck", page_icon="📱", layout="centered")

with open('dbScan/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <div class='hero-title'>Algorithm<br>Status Check</div>
        <div class='hero-desc'>Stop stressing over the algorithm. We compare your post's stats against thousands of real creators to tell you exactly what's happening. Find out if you're going viral, getting fake likes, or if the app is hiding your content.</div>
        <div class='scroll-indicator'>SCROLL TO CHECK POST ↓</div>
    </div>
    <div class='hero-right'>
        <div class='hero-graphic'>📱</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='input-section-title'>Enter Your Post Stats</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    followers = st.number_input("Total Followers", min_value=100, max_value=100000000, value=15000, step=100)
    impressions = st.number_input("Total Views (Impressions)", min_value=10, max_value=100000000, value=2500, step=100)

with col2:
    likes = st.number_input("Total Likes", min_value=0, max_value=10000000, value=180, step=10)
    comments = st.number_input("Total Comments", min_value=0, max_value=1000000, value=12, step=1)

if st.button("CHECK ALGORITHM STATUS"):
    reach_rate = impressions / followers if followers > 0 else 0
    engagement_rate = likes / impressions if impressions > 0 else 0
    interaction_rate = comments / likes if likes > 0 else 0
    
    user_data = {
        'reach_rate': reach_rate,
        'engagement_rate': engagement_rate,
        'interaction_rate': interaction_rate
    }
    
    cluster = run_inference(user_data)
    
    if cluster != -1:
        st.markdown("""
        <div class='result-card core-card'>
            <div class='result-label'>STATUS: NORMAL</div>
            <div class='result-title'>ALL GOOD / ORGANIC REACH</div>
            <div class='result-desc'>Your stats look completely normal compared to other creators. The app is showing your post to your regular audience. Keep doing what you're doing.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if reach_rate > 1.0:
            st.markdown("""
            <div class='result-card viral-card'>
                <div class='result-label'>STATUS: OUTPERFORMING</div>
                <div class='result-title'>GOING VIRAL! 🚀</div>
                <div class='result-desc'>Wow. Your views are way higher than your follower count. The algorithm loved this and pushed it to the explore page or 'For You' feed.</div>
            </div>
            """, unsafe_allow_html=True)
            
        elif engagement_rate > 0.4:
            st.markdown("""
            <div class='result-card bot-card'>
                <div class='result-label'>STATUS: SUSPICIOUS ACTIVITY</div>
                <div class='result-title'>FAKE LIKES DETECTED 🤖</div>
                <div class='result-desc'>The number of likes compared to views is unnatural. This usually means bot accounts or fake engagement groups are liking the post.</div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class='result-card shadow-card'>
                <div class='result-label'>STATUS: RESTRICTED REACH</div>
                <div class='result-title'>HIDDEN BY ALGORITHM 📉</div>
                <div class='result-desc'>Your views are strangely low for how many followers you have. The app is likely restricting your reach and not showing this post to your own audience.</div>
            </div>
            """, unsafe_allow_html=True)
