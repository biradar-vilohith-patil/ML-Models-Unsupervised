import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsRegressor

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    features = ['doomscrolling', 'deep_work', 'social_battery', 'escapism']
    X = df[features]

    # 1. Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. Run t-SNE to build the 2D cluster map
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    tsne_coords = tsne.fit_transform(X_scaled)
    
    # 3. Train KNN to act as the "Transform" bridge for new web-app users
    projector = KNeighborsRegressor(n_neighbors=5)
    projector.fit(X_scaled, tsne_coords)

    # 4. Define the mathematical anchors based on our 4 extreme archetypes
    anchors_raw = np.array([
        [9.0, 1.0, 9.0, 2.0], # Terminally Online
        [1.0, 9.0, 2.0, 1.0], # Academic Weapon
        [3.0, 1.0, 3.0, 9.0], # Cozy Escapist
        [6.0, 7.0, 8.0, 3.0]  # The Creator
    ])
    
    anchors_scaled = scaler.transform(anchors_raw)
    anchors_tsne = projector.predict(anchors_scaled)
    
    archetype_coords = {
        "brain_rot": anchors_tsne[0],
        "academic": anchors_tsne[1],
        "escapist": anchors_tsne[2],
        "creator": anchors_tsne[3]
    }

    model_artifacts = {
        'scaler': scaler,
        'projector': projector,
        'features': features,
        'archetype_coords': archetype_coords
    }

    os.makedirs(models_dir, exist_ok=True)
    with open(os.path.join(models_dir, 'tsne_aura_artifacts.pkl'), 'wb') as f:
        pickle.dump(model_artifacts, f)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    train_and_save_model(os.path.join(base_dir, 'data', 'digital_aura.csv'), os.path.join(base_dir, 'models'))