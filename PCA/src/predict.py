import pickle
import pandas as pd
import os
import numpy as np

def load_artifacts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_path = os.path.join(base_dir, 'models', 'pca_vibe_artifacts.pkl')
    with open(pipeline_path, 'rb') as f:
        return pickle.load(f)

def run_inference(input_dict):
    artifacts = load_artifacts()
    
    df_input = pd.DataFrame([input_dict])
    df_input = df_input[artifacts['features']]
    
    X_scaled = artifacts['scaler'].transform(df_input)
    pca_coords = artifacts['pca'].transform(X_scaled)[0]
    
    # THE FIX: Calculate Euclidean distance to find the closest absolute archetype
    dists = {}
    for name, coords in artifacts['archetype_coords'].items():
        dist = np.linalg.norm(pca_coords - coords)
        dists[name] = dist
        
    closest_archetype = min(dists, key=dists.get)
    
    return pca_coords[0], pca_coords[1], closest_archetype