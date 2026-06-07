import pandas as pd
import os
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['reach_rate', 'engagement_rate', 'interaction_rate']
    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    dbscan = DBSCAN(eps=0.4, min_samples=10)
    dbscan_labels = dbscan.fit_predict(X_scaled)

    classifier = KNeighborsClassifier(n_neighbors=3, weights='distance')
    classifier.fit(X_scaled, dbscan_labels)

    pipeline = Pipeline(steps=[
        ('scaler', scaler),
        ('classifier', classifier)
    ])

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'algorithm_dbscan_pipeline.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    return pipeline

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_creator_metrics.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)