import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="Resume Scanner", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .hero-container { display: flex; align-items: center; justify-content: space-between; padding: 40px 0; border-bottom: 1px solid #1a1a1a; }
    .hero-left { flex: 1; }
    .hero-right { flex: 0.5; display: flex; justify-content: center; }
    .result-card { padding: 30px; border-radius: 15px; margin-top: 20px; border-left: 8px solid; }
    .cluster-normal { background-color: #1e3a8a; border-color: #3b82f6; }
    .cluster-unicorn { background-color: #064e3b; border-color: #10b981; }
    .cluster-flag { background-color: #7f1d1d; border-color: #ef4444; }
    </style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <h1>Placement ATS Engine</h1>
        <p>Does your resume pass the automated screening? We compare your profile against thousands of other graduates to see if you stand out or get lost in the crowd.</p>
    </div>
    <div class='hero-right'>
        <div style='font-size: 8rem;'>🎯</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- INPUT/RESULT SPLIT ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("Enter Your Stats")
    cgpa = st.number_input("Academics (CGPA/%)", 40.0, 100.0, 75.0, 1.0)
    logical = st.number_input("Aptitude Score (100-900)", 100.0, 900.0, 500.0, 10.0)
    programming = st.number_input("Coding Score (100-900)", 100.0, 900.0, 450.0, 10.0)
    scan_btn = st.button("EXECUTE SCAN", use_container_width=True)

with col2:
    if scan_btn:
        pred, score, medians = run_inference({'collegeGPA': cgpa, 'Aptitude_Index': logical, 'ComputerProgramming': programming})
        
        if pred == 1:
            title, state, desc, css = "YOU ARE IN THE CROWD", "Standard Profile", "Your skills are like thousands of others. You'll likely be filtered out by automated systems. Focus on building unique projects.", "cluster-normal"
        elif programming > medians['ComputerProgramming'] and cgpa >= 70.0:
            title, state, desc, css = "TOP TIER TALENT", "High Potential Profile", "Your coding skills put you ahead of the majority. Your profile is strong enough to pass automated screening for top companies.", "cluster-unicorn"
        else:
            title, state, desc, css = "NON-STANDARD PROFILE", "Profile Anomaly", "Your profile is very different from the usual. This can be good or bad. Be prepared to explain your unique journey in interviews.", "cluster-flag"

        st.markdown(f"<div class='result-card {css}'>", unsafe_allow_html=True)
        st.subheader(title)
        st.caption(f"Status: {state}")
        st.write(desc)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Academics", f"{cgpa:.1f}", f"{cgpa - medians['collegeGPA']:.1f}")
        m2.metric("Aptitude", f"{logical:.0f}", f"{logical - medians['Aptitude_Index']:.0f}")
        m3.metric("Coding", f"{programming:.0f}", f"{programming - medians['ComputerProgramming']:.0f}")
        st.markdown("</div>", unsafe_allow_html=True)