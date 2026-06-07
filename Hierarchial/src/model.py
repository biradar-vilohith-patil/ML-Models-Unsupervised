import pandas as pd
import os
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestCentroid
from sklearn.pipeline import Pipeline

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['batting_avg', 'batting_strike_rate', 'boundaries_percent']
    X = df[features]

    scaler = MinMaxScaler()
    scaler.fit(X)

    ideal_profiles = pd.DataFrame({
        'batting_avg': [32.0, 48.0, 20.0, 45.0],
        'batting_strike_rate': [115.0, 130.0, 185.0, 175.0],
        'boundaries_percent': [35.0, 45.0, 75.0, 65.0]
    })
    
    labels = np.array([0, 1, 2, 3])
    scaled_profiles = scaler.transform(ideal_profiles)

    classifier = NearestCentroid()
    classifier.fit(scaled_profiles, labels)

    pipeline = Pipeline(steps=[
        ('scaler', scaler),
        ('classifier', classifier)
    ])

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'scout_hierarchical_pipeline.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    return pipeline

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_ipl_batters.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)