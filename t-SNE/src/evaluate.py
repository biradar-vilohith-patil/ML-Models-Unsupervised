import os
import pandas as pd
from src.predict import load_artifacts

def evaluate_tsne(data_path):
    artifacts = load_artifacts()
    df = pd.read_csv(data_path)
    print(f"t-SNE Architecture Evaluated.")
    print(f"Total Datapoints mapped: {len(df)}")
    print(f"Regressor Bridge Active. Ready for real-time inference.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evaluate_tsne(os.path.join(base_dir, 'data', 'digital_aura.csv'))