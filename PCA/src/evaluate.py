import os
import pandas as pd
from src.model import train_and_save_model

def evaluate_pca(artifacts, data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    X = df[artifacts['features']]
    X_scaled = artifacts['scaler'].transform(X)
    
    variance_ratio = artifacts['pca'].explained_variance_ratio_
    cumulative_variance = variance_ratio.cumsum()
    
    print(f"Total Songs Evaluated: {len(df)}")
    print("\nHow much of human music taste is captured in 2D?")
    print(f"X-Axis (Intensity/Energy): {variance_ratio[0]*100:.2f}%")
    print(f"Y-Axis (Mood/Acoustics): {variance_ratio[1]*100:.2f}%")
    print(f"Total Variance Captured: {cumulative_variance[1]*100:.2f}%")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_spotify_vibes.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    artifacts = train_and_save_model(data_path, models_dir)
    evaluate_pca(artifacts, data_path)