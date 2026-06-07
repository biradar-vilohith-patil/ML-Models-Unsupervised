import pandas as pd
import os
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.mixture import GaussianMixture

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'Heart Rate']
    X = df[features]

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the GMM normally on the real data distribution
    gmm = GaussianMixture(n_components=3, covariance_type='full', random_state=42, n_init=5)
    gmm.fit(X_scaled)

    # --- DETERMINISTIC PHYSIOLOGY MAPPER ---
    means = gmm.means_
    scores = []
    
    for i in range(3):
        # Translate the scaled cluster centers back to real-world numbers
        real_world_stats = scaler.inverse_transform([means[i]])[0]
        
        sleep = real_world_stats[0]
        quality = real_world_stats[1]
        activity = real_world_stats[2] / 10.0 # Normalize activity weight
        stress = real_world_stats[3]
        hr = real_world_stats[4] / 10.0       # Normalize HR weight
        
        # Calculate physiological Health Score (High Sleep/Activity is good, High Stress/HR is bad)
        health_score = sleep + quality + activity - stress - hr
        scores.append((i, health_score))

    # Sort clusters from Healthiest (highest score) to Most Fatigued (lowest score)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Force the mapping: 0 = Optimized, 1 = Baseline, 2 = Burnout
    mapping = {
        scores[0][0]: 0,
        scores[1][0]: 1,
        scores[2][0]: 2
    }

    model_artifacts = {
        'scaler': scaler,
        'gmm': gmm,
        'mapping': mapping,
        'features': features
    }

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'recovery_gmm_artifacts.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(model_artifacts, f)
        
    return model_artifacts

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_sleep_metrics.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)