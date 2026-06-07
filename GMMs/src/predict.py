import pickle
import pandas as pd
import os

def load_artifacts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_path = os.path.join(base_dir, 'models', 'recovery_gmm_artifacts.pkl')
    with open(pipeline_path, 'rb') as f:
        return pickle.load(f)

def run_inference(input_dict):
    artifacts = load_artifacts()
    df_input = pd.DataFrame([input_dict])
    
    X_scaled = artifacts['scaler'].transform(df_input)
    raw_probs = artifacts['gmm'].predict_proba(X_scaled)[0]
    
    # Reroute the raw probabilities to the correct UI buckets
    mapped_probs = {0: 0.0, 1: 0.0, 2: 0.0}
    for raw_id, fixed_id in artifacts['mapping'].items():
        mapped_probs[fixed_id] = raw_probs[raw_id]
        
    # Select the highest probability from the corrected mapping
    primary_cluster = max(mapped_probs, key=mapped_probs.get)
    
    return int(primary_cluster), mapped_probs