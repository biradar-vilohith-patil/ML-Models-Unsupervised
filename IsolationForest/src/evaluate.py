import os
import pandas as pd
from sklearn.metrics import classification_report
from src.model import train_and_save_model

def evaluate_anomaly_detector(artifacts, data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    X = df[artifacts['features']]
    
    predictions = artifacts['model'].predict(X)
    anomaly_scores = artifacts['model'].decision_function(X)
    
    df['Anomaly'] = predictions
    df['Score'] = anomaly_scores
    
    total_candidates = len(df)
    standard_pool = len(df[df['Anomaly'] == 1])
    outliers = len(df[df['Anomaly'] == -1])
    
    print(f"Total Profiles Evaluated: {total_candidates}")
    print(f"Standard Applicant Pool (Inliers): {standard_pool} ({(standard_pool/total_candidates)*100:.1f}%)")
    print(f"Isolated Profiles (Anomalies): {outliers} ({(outliers/total_candidates)*100:.1f}%)")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_amcat_profiles.csv')
    models_dir = os.path.join(base_dir, 'models')
    
    artifacts = train_and_save_model(data_path, models_dir)
    evaluate_anomaly_detector(artifacts, data_path)