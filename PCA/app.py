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
    
    .stApp {
        background-color: #121212;
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF;
    }
    
    .hero-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(180deg, #1DB954 0%, #121212 100%);
        padding: 50px 50px;
        border-radius: 12px;
        margin-bottom: 40px;
    }
    
    .hero-left {
        flex: 1.2;
    }
    
    .hero-right {
        flex: 0.8;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    
    .spotify-title {
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;
        line-height: 1.1;
        color: #FFFFFF;
    }
    
    .spotify-subtitle {
        font-size: 1.1rem;
        color: #e5e5e5;
        font-weight: 500;
        margin-top: 15px;
        max-width: 90%;
    }
    
    /* CLEAN & BOLD SLIDER UI */
    .stSlider label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        color: #FFFFFF !important;
        margin-bottom: 5px;
    }
    
    div[data-testid="stThumbValue"] {
        font-size: 1rem !important;
        font-weight: 800 !important;
        color: #1DB954 !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #1DB954 !important;
    }
    
    /* BUTTON UI */
    .stButton > button {
        background-color: #1DB954 !important;
        color: #000000 !important;
        border-radius: 500px !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        padding: 20px 32px !important;
        border: none !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        transition: transform 0.2s ease, filter 0.2s ease;
        width: 100%;
        margin-top: 25px;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        filter: brightness(1.1);
    }
    
    /* RESULT CARD UI */
    .result-card {
        background-color: #181818;
        padding: 40px;
        border-radius: 8px;
        margin-top: 5px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .playlist-header {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #FFFFFF;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    .playlist-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 15px;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    
    .playlist-desc {
        font-size: 1.05rem;
        color: #b3b3b3;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 900 !important;
        color: #1DB954 !important;
        letter-spacing: -1px;
    }
    div[data-testid="stMetricLabel"] {
        color: #b3b3b3 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# HERO SECTION WITH REAL SPOTIFY ICON
st.markdown("""
<div class='hero-container'>
    <div class='hero-left'>
        <h1 class='spotify-title'>The Vibe Matrix</h1>
        <p class='spotify-subtitle'>Adjust your aesthetic. Our PCA algorithm will compress your frequency into a 2D coordinate and map you to a definitive playlist archetype.</p>
    </div>
    <div class='hero-right'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" width="160" style="filter: drop-shadow(0 0 20px rgba(0,0,0,0.4));">
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    mood = st.slider("Mood (1 = Devdas , 10 = Relangi mama ✨)", 1, 10, 5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    energy = st.slider("Energy (1 = Calm 🧘, 10 = Balakrishna 🦁)", 1, 10, 6)
    
    st.markdown("<br>", unsafe_allow_html=True)
    acoustic = st.slider("Sound (1 = Mass 🥁, 10 = Class 🎻)", 1, 10, 3)
    
    st.markdown("<br>", unsafe_allow_html=True)
    groove = st.slider("Lungi Dance (1 = Slight Touch 🎧, 10 = 1 2 3 4, Dancefloor 🕺)", 1, 10, 7)
    
    scan_btn = st.button("Detect the Type")

with col2:
    if scan_btn:
        user_data = {
            'valence': mood / 10.0,
            'energy': energy / 10.0,
            'acousticness': acoustic / 10.0,
            'danceability': groove / 10.0
        }
        
        # Pulling the guaranteed archetype directly from the backend distance calculation
        pc1, pc2, archetype = run_inference(user_data)
        
        if archetype == "euphoria":
            playlist ="Enjoy Mode"
            color = "#1DB954" # Spotify Green
            desc = "High energy, high mood. The mathematical equivalent of a massive comeback. Fast-paced, driving with the windows down, absolute synthetic energy."
            gif_path = "b11.gif"
            
        elif archetype == "villain":
            playlist = "Locked In"
            color = "#ef4444" # Red
            desc = "High energy combined with a dark, aggressive mood. Peak gym anthem, underground rap, or heavy metal aesthetic. Zero distractions."
            gif_path = "b2.gif"
            
        elif archetype == "chill":
            playlist = "Chill Mood"
            color = "#f59e0b" # Warm Orange
            desc = "Stripped back, highly acoustic, and warmly positive. No chaotic energy here. Touching grass and achieving pure relaxed homeostasis."
            gif_path = "b3.gif"
            
        else:
            playlist = "It's So Over"
            color = "#3b82f6" # Blue
            desc = "Low energy and crushing melancholy. The aesthetic of staring at your bedroom ceiling at 3AM. Atmospheric, sad, and deeply introspective."
            gif_path = "b4.gif"
        
        # Convert the designated GIF to Base64
        gif_base64 = get_base64_gif(gif_path)
        
        # Added height: 280px and object-fit: cover to ensure all GIFs render exactly the same size without stretching
        gif_html = f'<img src="data:image/gif;base64,{gif_base64}" style="width: 100%; height: 390px; object-fit: cover; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">' if gif_base64 else ''

        st.markdown(f"""
        <div style="background: linear-gradient(180deg, {color} 0%, #121212 100%); padding: 2px; border-radius: 10px;">
            <div class='result-card'>
                <div class='playlist-header'>TFI Archetype • AI Generated</div>
                {gif_html}
                <div class='playlist-title'>{playlist}</div>
                <div class='playlist-desc'>{desc}</div>
                <div style='color: #FFFFFF; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;'>Spotify PCA Coordinates</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        m1.metric("Intensity Axis (PC1)", f"{pc1:.2f}")
        m2.metric("Mood Axis (PC2)", f"{pc2:.2f}")