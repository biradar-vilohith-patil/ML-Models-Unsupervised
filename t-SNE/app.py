import streamlit as st
from src.predict import run_inference

st.set_page_config(page_title="Digital Aura Catcher", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0a0a0f; font-family: 'Space Grotesk', sans-serif; color: #FFFFFF; }
    
    .hero-container { display: flex; align-items: center; justify-content: space-between; background: linear-gradient(135deg, #4F46E5 0%, #06b6d4 100%); padding: 50px 50px; border-radius: 12px; margin-bottom: 40px; box-shadow: 0 10px 40px rgba(6, 182, 212, 0.2); }
    .hero-title { font-size: 4.5rem; font-weight: 900; letter-spacing: -2px; margin: 0; line-height: 1.1; color: #FFFFFF; }
    .hero-subtitle { font-size: 1.1rem; color: #e0e7ff; font-weight: 500; margin-top: 15px; }
    
    .stSlider label { font-size: 1.1rem !important; font-weight: 700 !important; color: #FFFFFF !important; margin-bottom: 5px; letter-spacing: 0.5px; }
    div[data-testid="stThumbValue"] { font-size: 1rem !important; font-weight: 800 !important; color: #06b6d4 !important; }
    .stSlider > div > div > div > div { background-color: #06b6d4 !important; }
    
    .stButton > button { background: linear-gradient(90deg, #4F46E5 0%, #06b6d4 100%) !important; color: #FFFFFF !important; border-radius: 4px !important; font-weight: 800 !important; padding: 20px 32px !important; width: 100%; border: none !important; letter-spacing: 2px; text-transform: uppercase; transition: transform 0.2s ease; margin-top: 25px;}
    .stButton > button:hover { transform: scale(1.02); }
    
    .result-card { background-color: #111119; padding: 40px; border-radius: 8px; border: 1px solid #1f1f2e; }
    .aura-header { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; color: #818cf8; font-weight: 800; margin-bottom: 15px; }
    .aura-title { font-size: 3.5rem; font-weight: 900; margin-bottom: 15px; line-height: 1.1; letter-spacing: -1px; }
    .aura-desc { font-size: 1.05rem; color: #9ca3af; line-height: 1.6; margin-bottom: 30px; }
    
    div[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 900 !important; color: #06b6d4 !important; letter-spacing: -1px; }
    div[data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 0.85rem !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <h1 class='hero-title'>Digital Aura Catcher</h1>
        <p class='hero-subtitle'>Map your screen-time psychology. Our t-SNE algorithm clusters your digital footprint into a localized topological archetype.</p>
    </div>
    <div class='hero-right'>
        <div style="font-size: 7rem; text-shadow: 0 0 30px rgba(255,255,255,0.4);">🌐</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    doom = st.slider("Doomscrolling (TikTok/Reels)", 0, 10, 5)
    deep = st.slider("Deep Work (Study/Code/Build)", 0, 10, 6)
    social = st.slider("Social Battery (DMs/Calls/Insta)", 0, 10, 7)
    escape = st.slider("Escapism (Gaming/Netflix)", 0, 10, 4)
    scan_btn = st.button("CALCULATE AURA")

with col2:
    if scan_btn:
        tsne_x, tsne_y, archetype = run_inference({
            'doomscrolling': doom, 'deep_work': deep, 
            'social_battery': social, 'escapism': escape
        })
        
        if archetype == "brain_rot":
            aura, color, desc = "Terminally Online", "#ec4899", "High doomscrolling, massive social consumption. Your algorithm knows you better than you know yourself. Please touch grass."
        elif archetype == "academic":
            aura, color, desc = "Academic Weapon", "#10b981", "Low distractions, pure focus. You exist in a state of flow. The t-SNE matrix isolates you as a high-productivity outlier."
        elif archetype == "escapist":
            aura, color, desc = "The Cozy Escapist", "#8b5cf6", "High gaming, high streaming. Reality is optional. You've clustered directly into the digital comfort zone."
        else:
            aura, color, desc = "The Creator", "#f59e0b", "High social output, high execution. You aren't just consuming the feed, you are actively curating the grid."

        html_str = f"""
        <div style="background: linear-gradient(180deg, {color} 0%, #111119 100%); padding: 2px; border-radius: 10px;">
            <div class='result-card'>
                <div class='aura-header'>TOPOLOGICAL CLUSTER DETECTED</div>
                <div class='aura-title' style='color: {color};'>{aura}</div>
                <div class='aura-desc'>{desc}</div>
                <div style='color: #4b5563; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;'>t-SNE Coordinates</div>
            </div>
        </div>
        """
        st.markdown(html_str, unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Manifold X", f"{tsne_x:.2f}")
        m2.metric("Manifold Y", f"{tsne_y:.2f}")