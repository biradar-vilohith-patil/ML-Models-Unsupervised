import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="Franchise Scout AI", page_icon="🏏", layout="centered")

with open('Hierarchial/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <div class='hero-title'>T20 Franchise<br>Scout AI</div>
        <div class='hero-desc'>Map player statistics against real global IPL franchise data. Our normalized hierarchical clustering engine identifies the exact tactical archetype of a batter to optimize auction strategy and squad balance.</div>
        <div class='scroll-indicator'>SCROLL TO CONFIGURE PLAYER METRICS ↓</div>
    </div>
    <div class='hero-right'>
        <div class='hero-graphic'>🏏</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='input-section-title'>Input Real Match Telemetry</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    batting_avg = st.number_input("Batting Average", min_value=0.0, max_value=100.0, value=32.0, step=1.0)

with col2:
    strike_rate = st.number_input("Strike Rate", min_value=50.0, max_value=250.0, value=135.0, step=1.0)

with col3:
    boundary_pct = st.number_input("Boundary Runs (%)", min_value=0.0, max_value=100.0, value=52.0, step=1.0)

if st.button("Know The Type.."):
    user_data = {
        'batting_avg': batting_avg,
        'batting_strike_rate': strike_rate,
        'boundaries_percent': boundary_pct
    }
    
    cluster = run_inference(user_data)
    
    archetypes = {
        0: {
            "title": "THE INNINGS ACCUMULATOR",
            "role": "Middle-Order Rotator",
            "desc": "High average, moderate strike rate, low boundary percentage. Relies heavily on singles and twos. Essential for stabilizing collapses on difficult wickets, but a liability if the required rate climbs.",
            "css": "cluster-accum"
        },
        1: {
            "title": "THE HITMAN / ANCHOR",
            "role": "Top-Order Stabilizer",
            "desc": "Elite batting average with a calculated, scalable strike rate. This player absorbs powerplay pressure, protects the fragile middle order, and bats deep into the 18th over.",
            "css": "cluster-anchor"
        },
        2: {
            "title": "THE DEATH OVERS FINISHER",
            "role": "Lower-Order Aggressor",
            "desc": "Extreme strike rate and massive boundary percentage, heavily sacrificing average. Designed purely for high-variance, high-impact scenarios in the final 4 overs. A pure ball-striker.",
            "css": "cluster-hitter"
        },
        3: {
            "title": "THE ENFORCER",
            "role": "Top-Order Aggressor",
            "desc": "High average combined with a destructive strike rate. Dominates the powerplay by hitting over the infield consistently. A rare, high-value auction target that wins matches in the first 6 overs.",
            "css": "cluster-enforcer"
        }
    }
    
    result = archetypes.get(cluster, archetypes[0])
    
    st.markdown(f"""
    <div class='result-card {result["css"]}'>
        <div class='result-label'>HIERARCHICAL CLUSTER {cluster} CONFIRMED</div>
        <div class='result-title'>{result["title"]}</div>
        <div class='result-role'>TACTICAL ROLE: {result["role"]}</div>
        <div class='result-desc'>{result["desc"]}</div>
    </div>
    """, unsafe_allow_html=True)
