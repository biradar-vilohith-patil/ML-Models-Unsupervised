import os
import pandas as pd
from sklearn.metrics import silhouette_score
from src.model import train_and_save_model

def evaluate_clusters(pipeline, data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['frontend_score', 'backend_score', 'data_score', 'cloud_score', 'systems_score']
    X = df[features]
    
    labels = pipeline.predict(X)
    X_processed = pipeline.named_steps['preprocessor'].transform(X)
    
    sil_score = silhouette_score(X_processed, labels, random_state=42)
    print(f"Silhouette Score: {sil_score:.4f}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'developer_profiles.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    pipeline = train_and_save_model(data_path, models_dir)
    evaluate_clusters(pipeline, data_path)