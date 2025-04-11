import argparse
from data_processor import DataProcessor
from algorithms import CustomPrecipitationPredictor
from visualizer import Visualizer
import numpy as np

def main():

    # Parse Arguments Choice
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["predict", "cluster", "anomalies"], required=True)
    args = parser.parse_args()

    # Load and preprocess data
    processor = DataProcessor("../data/climate_data.json")
    processor.load_data()
    processor.clean_data()
    x, y = processor.get_features_and_target() # get dates and values

    # Prediction Graph
    if args.action == "predict":
        model = CustomPrecipitationPredictor()
        model.fit(x, y)
        predictions = model.predict(x)
        years = [row[0] for row in x]
        Visualizer.plot_precipitation_trend(years, y.tolist(), predictions.tolist())

    # Cluster Graph
    elif args.action == "cluster":
        data = list(zip(x, y))
        labels = custom_clustering(np.array(data), n_clusters=2)
        Visualizer.plot_clustered_data(data, labels.tolist())

    # Anomalies
    elif args.action == "anomalies":
        # Use just the target variable for anomaly detection
        anomalies = detect_anomalies(y)
        Visualizer.plot_anomalies(y.tolist(), anomalies.tolist(),years)


if __name__ == "__main__":
    main()
