import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['valence', 'energy', 'acousticness', 'danceability']
    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2, random_state=42)
    pca.fit(X_scaled)
    
    # THE FIX: Mathematically define the 4 extremes [valence, energy, acousticness, danceability]
    anchors_raw = np.array([
        [0.95, 0.90, 0.05, 0.90], # Euphoric
        [0.10, 0.95, 0.05, 0.50], # Villain
        [0.85, 0.20, 0.85, 0.40], # Chill
        [0.05, 0.10, 0.95, 0.10]  # Doomer
    ])
    
    # Project the anchors into the PCA space to find their exact coordinates
    anchors_scaled = scaler.transform(anchors_raw)
    anchors_pca = pca.transform(anchors_scaled)
    
    archetype_coords = {
        "euphoria": anchors_pca[0],
        "villain": anchors_pca[1],
        "chill": anchors_pca[2],
        "doomer": anchors_pca[3]
    }

    model_artifacts = {
        'scaler': scaler,
        'pca': pca,
        'features': features,
        'archetype_coords': archetype_coords
    }

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'pca_vibe_artifacts.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(model_artifacts, f)
        
    return model_artifacts

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_spotify_vibes.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)