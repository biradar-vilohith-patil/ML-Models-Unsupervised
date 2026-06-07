import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="Archetype AI", page_icon="⚡", layout="centered")

with open('KMeans/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <div class='hero-title'>Engineering<br>Archetype AI</div>
        <div class='hero-desc'>Stop guessing your career path. We cluster your technical DNA against thousands of industry profiles to reveal your exact role fit in the modern tech ecosystem.</div>
        <div class='scroll-indicator'>SCROLL TO CONFIGURE DNA ↓</div>
    </div>
    <div class='hero-right'>
        <div class='hero-graphic'>⚡</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='input-section-title'>Define Your Proficiency (0-100)</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    frontend = st.slider("Frontend & UI (React, CSS, TS)", 0, 100, 50)
    backend = st.slider("Backend & APIs (Node, Python, Go)", 0, 100, 50)
    data = st.slider("Data & ML (SQL, Pandas, PyTorch)", 0, 100, 50)

with col2:
    cloud = st.slider("Cloud & DevOps (AWS, Docker, CI/CD)", 0, 100, 50)
    systems = st.slider("Systems & Low-Level (C++, Rust, OS)", 0, 100, 50)

if st.button("EXTRACT ARCHETYPE"):
    user_data = {
        'frontend_score': frontend,
        'backend_score': backend,
        'data_score': data,
        'cloud_score': cloud,
        'systems_score': systems
    }
    
    cluster = run_inference(user_data)
    
    archetypes = {
        0: {
            "title": "THE FULL-STACK ARCHITECT",
            "role": "Product Engineer / Full-Stack Developer",
            "desc": "You thrive at the intersection of user experience and business logic. You are highly adaptable and capable of shipping end-to-end products autonomously. Companies rely on you for speed and product iteration.",
            "css": "cluster-fs"
        },
        1: {
            "title": "THE INTELLIGENCE ENGINEER",
            "role": "Data Scientist / Machine Learning Engineer",
            "desc": "Your DNA is deeply mathematical and analytical. You extract signal from noise and build the predictive engines that drive modern tech. You belong in data-heavy domains and AI research labs.",
            "css": "cluster-data"
        },
        2: {
            "title": "THE INFRASTRUCTURE COMMANDER",
            "role": "DevOps / Site Reliability Engineer (SRE)",
            "desc": "You are the backbone of scale. You excel at automation, deployment pipelines, and cloud architecture. When millions of users hit the servers, you ensure the system doesn't collapse.",
            "css": "cluster-cloud"
        },
        3: {
            "title": "THE BARE-METAL OPTIMIZER",
            "role": "Systems Programmer / Embedded Engineer",
            "desc": "You operate close to the hardware. You care about memory management, latency, and extreme performance. Your domain is writing high-performance engines in C, C++, or Rust.",
            "css": "cluster-sys"
        }
    }
    
    result = archetypes.get(cluster, archetypes[0])
    
    st.markdown(f"""
    <div class='result-card {result["css"]}'>
        <div class='result-label'>DNA CLUSTER {cluster} IDENTIFIED</div>
        <div class='result-title'>{result["title"]}</div>
        <div class='result-role'>OPTIMAL ROLE: {result["role"]}</div>
        <div class='result-desc'>{result["desc"]}</div>
    </div>
    """, unsafe_allow_html=True)
