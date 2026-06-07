import os
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from src.model import train_and_save_model

def evaluate_anomaly_engine(pipeline, data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['reach_rate', 'engagement_rate', 'interaction_rate']
    X = df[features]
    
    labels = pipeline.predict(X)
    X_processed = pipeline.named_steps['scaler'].transform(X)
    
    core_mask = labels != -1
    if len(set(labels[core_mask])) > 1:
        sil_score = silhouette_score(X_processed[core_mask], labels[core_mask], random_state=42)
        print(f"Core Cluster Silhouette Score: {sil_score:.4f}")
    
    total_posts = len(labels)
    anomalies = np.sum(labels == -1)
    core_posts = total_posts - anomalies
    
    print(f"Total Posts Analyzed: {total_posts}")
    print(f"Standard Engagement (Core Clustering): {core_posts} ({(core_posts/total_posts)*100:.2f}%)")
    print(f"Identified Anomalies (Noise): {anomalies} ({(anomalies/total_posts)*100:.2f}%)")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_creator_metrics.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    pipeline = train_and_save_model(data_path, models_dir)
    evaluate_anomaly_engine(pipeline, data_path)