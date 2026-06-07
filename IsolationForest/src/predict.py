import pickle
import pandas as pd
import os

def load_artifacts():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_path = os.path.join(base_dir, 'models', 'ats_isolation_artifacts.pkl')
    with open(pipeline_path, 'rb') as f:
        return pickle.load(f)

def run_inference(input_dict):
    artifacts = load_artifacts()
    df_input = pd.DataFrame([input_dict])
    
    prediction = artifacts['model'].predict(df_input)[0]
    anomaly_score = artifacts['model'].decision_function(df_input)[0]
    
    return int(prediction), float(anomaly_score), artifacts['medians']