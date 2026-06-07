import streamlit as st
import base64
from src.predict import run_inference

# Helper function to load local GIFs for HTML rendering
@st.cache_data
def get_base64_gif(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

st.set_page_config(page_title="Spotify Vibe Matrix", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;900&display=swap');
    .stApp { background-color: #121212; font-family: 'Montserrat', sans-serif; color: #FFFFFF; }
    
    .hero-container { display: flex; align-items: center; justify-content: space-between; background: linear-gradient(180deg, #1DB954 0%, #121212 100%); padding: 50px 50px; border-radius: 12px; margin-bottom: 40px; }
    .hero-title { font-size: 4.5rem; font-weight: 900; letter-spacing: -2px; margin: 0; line-height: 1.1; color: #FFFFFF; }
    .hero-subtitle { font-size: 1.1rem; color: #e5e5e5; font-weight: 500; margin-top: 15px; }
    
    .stSlider label { font-size: 1.1rem !important; font-weight: 700 !important; color: #FFFFFF !important; margin-bottom: 5px; }
    .stButton > button { background-color: #1DB954 !important; color: #000000 !important; border-radius: 500px !important; font-weight: 800 !important; padding: 20px 32px !important; width: 100%; margin-top: 25px; }
    
    .result-card { background-color: #181818; padding: 40px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .playlist-title { font-size: 3.5rem; font-weight: 900; margin-bottom: 15px; }
    .playlist-desc { font-size: 1.05rem; color: #b3b3b3; line-height: 1.6; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <h1 class='hero-title'>The Vibe Matrix</h1>
        <p class='hero-subtitle'>Adjust your aesthetic. Our PCA algorithm compresses your frequency into a coordinate and maps you to a definitive TFI archetype.</p>
    </div>
    <div class='hero-right'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" width="160">
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    mood = st.slider("Mood (1 = Devdas , 10 = Relangi mama ✨)", 1, 10, 5)
    energy = st.slider("Energy (1 = Calm 🧘, 10 = Balakrishna 🦁)", 1, 10, 6)
    acoustic = st.slider("Sound (1 = Mass 🥁, 10 = Class 🎻)", 1, 10, 3)
    groove = st.slider("Lungi Dance (1 = Slight Touch 🎧, 10 = 1 2 3 4, Dancefloor 🕺)", 1, 10, 7)
    scan_btn = st.button("DETECT THE TYPE")

with col2:
    if scan_btn:
        pc1, pc2, archetype = run_inference({
            'valence': mood/10.0, 'energy': energy/10.0, 
            'acousticness': acoustic/10.0, 'danceability': groove/10.0
        })
        
        # Archetype mapping
        if archetype == "euphoria":
            playlist, color, desc, gif = "Enjoy Mode", "#1DB954", "High energy, high mood. Massive comeback energy.", "b11.gif"
        elif archetype == "villain":
            playlist, color, desc, gif = "Locked In", "#ef4444", "Aggressive, dark, peak gym anthem.", "b2.gif"
        elif archetype == "chill":
            playlist, color, desc, gif = "Chill Mood", "#f59e0b", "Stripped back, acoustic, and positive vibes.", "b3.gif"
        else:
            playlist, color, desc, gif = "It's So Over", "#3b82f6", "Atmospheric, sad, and deeply introspective.", "b4.gif"
        
        gif_b64 = get_base64_gif(gif)
        # 1:1 Aspect Ratio Snippet
        gif_html = f'<img src="data:image/gif;base64,{gif_b64}" style="width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 8px; margin-bottom: 20px;">' if gif_b64 else ''

        st.markdown(f"""
        <div style="background: linear-gradient(180deg, {color} 0%, #121212 100%); padding: 2px; border-radius: 10px;">
            <div class='result-card'>
                {gif_html}
                <div class='playlist-title'>{playlist}</div>
                <div class='playlist-desc'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Intensity (PC1)", f"{pc1:.2f}")
        m2.metric("Mood (PC2)", f"{pc2:.2f}")