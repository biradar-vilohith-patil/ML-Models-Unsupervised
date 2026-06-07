import os
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

def evaluate_clusters(data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    features = ['batting_avg', 'batting_strike_rate', 'boundaries_percent']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    hierarchical = AgglomerativeClustering(n_clusters=4, linkage='ward')
    labels = hierarchical.fit_predict(X_scaled)
    
    sil_score = silhouette_score(X_scaled, labels, random_state=42)
    print(f"Hierarchical Silhouette Score: {sil_score:.4f}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'cleaned_ipl_batters.csv')
    evaluate_clusters(data_path)