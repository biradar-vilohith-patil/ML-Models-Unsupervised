import pickle
import pandas as pd
import os
import numpy as np

def load_artifacts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, 'models', 'tsne_aura_artifacts.pkl'), 'rb') as f:
        return pickle.load(f)

def run_inference(input_dict):
    artifacts = load_artifacts()
    
    df_input = pd.DataFrame([input_dict])[artifacts['features']]
    X_scaled = artifacts['scaler'].transform(df_input)
    
    # Use the KNN Regressor to predict where this user lands in the t-SNE space
    tsne_coords = artifacts['projector'].predict(X_scaled)[0]
    
    # Find nearest archetype by Euclidean distance
    dists = {name: np.linalg.norm(tsne_coords - coords) for name, coords in artifacts['archetype_coords'].items()}
    closest_archetype = min(dists, key=dists.get)
    
    return tsne_coords[0], tsne_coords[1], closest_archetype