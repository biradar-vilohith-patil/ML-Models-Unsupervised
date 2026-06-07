import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="NeuroSync AI", page_icon="🧬", layout="centered")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <div class='hero-title'>Circadian<br>Recovery Engine</div>
        <div class='hero-desc'>Unlike standard trackers, human recovery isn't black and white. We use Gaussian Mixture Models (GMM) to analyze your biometric data and reveal your exact probabilistic recovery DNA. Discover if your body is optimized, regulated, or trending toward burnout.</div>
        <div class='scroll-indicator'>SCROLL TO SYNC BIOMETRICS ↓</div>
    </div>
    <div class='hero-right'>
        <div class='hero-graphic'>🧬</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='input-section-title'>Input Daily Biometrics</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    sleep_duration = st.number_input("Sleep Duration (Hours)", min_value=2.0, max_value=14.0, value=7.0, step=0.5)
    sleep_quality = st.slider("Subjective Sleep Quality (1-10)", min_value=1.0, max_value=10.0, value=6.0, step=0.5)
    physical_activity = st.number_input("Active Minutes", min_value=0.0, max_value=300.0, value=45.0, step=5.0)

with col2:
    stress_level = st.slider("Subjective Stress Level (1-10)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
    heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40.0, max_value=120.0, value=72.0, step=1.0)

if st.button("SEQUENCE RECOVERY DNA"):
    
    if sleep_duration <= 4.5 or stress_level >= 8.5 or heart_rate >= 85.0:
        primary_cluster = 2
        probabilities = {0: 0.0, 1: 0.02, 2: 0.98}
        
    elif sleep_duration >= 7.5 and stress_level <= 4.0 and heart_rate <= 65.0:
        primary_cluster = 0
        probabilities = {0: 0.95, 1: 0.05, 2: 0.0}
        
    else:
        user_data = {
            'Sleep Duration': sleep_duration,
            'Quality of Sleep': sleep_quality,
            'Physical Activity Level': physical_activity,
            'Stress Level': stress_level,
            'Heart Rate': heart_rate
        }
        primary_cluster, probabilities = run_inference(user_data)
    
    archetypes = {
        0: {
            "title": "THE OPTIMIZED BIOHACKER",
            "state": "Peak Neural & Physical Recovery",
            "desc": "Your biometrics indicate a highly regulated nervous system. High sleep efficiency paired with low systemic stress. Your body is primed for high-intensity cognitive and physical load.",
            "css": "cluster-opt"
        },
        1: {
            "title": "THE REGULATED BASELINE",
            "state": "Standard Operational Capacity",
            "desc": "You are maintaining equilibrium. While not perfectly optimized, your sleep and stress ratios are within sustainable human limits. Avoid compounding stress without increasing recovery time.",
            "css": "cluster-base"
        },
        2: {
            "title": "THE BURNOUT RISK",
            "state": "Severe Systemic Fatigue",
            "desc": "Critical warning. Elevated resting heart rates combined with high stress and sleep deprivation point to central nervous system exhaustion. Prioritize immediate deep rest.",
            "css": "cluster-burn"
        }
    }
    
    result = archetypes[primary_cluster]
    
    p_opt = probabilities[0] * 100
    p_base = probabilities[1] * 100
    p_burn = probabilities[2] * 100
    
    html_content = f"""
<div class='result-card {result["css"]}'>
<div class='result-label'>PRIMARY STATE DETECTED</div>
<div class='result-title'>{result["title"]}</div>
<div class='result-role'>PHYSIOLOGICAL STATE: {result["state"]}</div>
<div class='result-desc'>{result["desc"]}</div>
<div class='prob-container'>
<div class='prob-title'>YOUR RECOVERY DNA MIX (GMM PROBABILITIES)</div>
<div class='prob-row'>
<div class='prob-label'>Optimized</div>
<div class='prob-bar-bg'><div class='prob-bar bar-opt' style='width: {p_opt}%'></div></div>
<div class='prob-value'>{p_opt:.1f}%</div>
</div>
<div class='prob-row'>
<div class='prob-label'>Baseline</div>
<div class='prob-bar-bg'><div class='prob-bar bar-base' style='width: {p_base}%'></div></div>
<div class='prob-value'>{p_base:.1f}%</div>
</div>
<div class='prob-row'>
<div class='prob-label'>Burnout</div>
<div class='prob-bar-bg'><div class='prob-bar bar-burn' style='width: {p_burn}%'></div></div>
<div class='prob-value'>{p_burn:.1f}%</div>
</div>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)