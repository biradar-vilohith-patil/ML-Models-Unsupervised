import pandas as pd
import os
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['frontend_score', 'backend_score', 'data_score', 'cloud_score', 'systems_score']
    X = df[features]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), features)
        ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('clusterer', KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, random_state=42))
    ])

    pipeline.fit(X)

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'career_kmeans_pipeline.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    return pipeline

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'developer_profiles.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)