import pickle
import pandas as pd
import os

def load_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipeline_path = os.path.join(base_dir, 'models', 'algorithm_dbscan_pipeline.pkl')
    with open(pipeline_path, 'rb') as f:
        return pickle.load(f)

def run_inference(input_dict):
    pipeline = load_pipeline()
    df_input = pd.DataFrame([input_dict])
    cluster_id = pipeline.predict(df_input)[0]
    return int(cluster_id)