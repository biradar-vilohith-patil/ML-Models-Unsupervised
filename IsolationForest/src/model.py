import pandas as pd
import os
import pickle
from sklearn.ensemble import IsolationForest

def train_and_save_model(data_path, models_dir):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['collegeGPA', 'Aptitude_Index', 'ComputerProgramming']
    X = df[features]

    clf = IsolationForest(
        n_estimators=500,
        max_samples='auto',
        contamination=0.08,
        max_features=1.0,
        random_state=42,
        n_jobs=-1
    )
    
    clf.fit(X)
    
    medians = X.median().to_dict()

    model_artifacts = {
        'model': clf,
        'features': features,
        'medians': medians
    }

    os.makedirs(models_dir, exist_ok=True)
    artifact_path = os.path.join(models_dir, 'ats_isolation_artifacts.pkl')
    
    with open(artifact_path, 'wb') as f:
        pickle.dump(model_artifacts, f)
        
    return model_artifacts

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_amcat_profiles.csv')
    models_dir = os.path.join(base_dir, 'models')
    train_and_save_model(data_path, models_dir)