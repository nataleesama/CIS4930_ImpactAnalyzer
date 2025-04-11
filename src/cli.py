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
    miamiProcessor = DataProcessor("../data/miamiData.json")
    orlandoProcessor = DataProcessor("../data/orlandoData.json")
    tallahasseeProcessor = DataProcessor("../data/tallahasseeData.json")
    
    miamiProcessor.load_data()
    miamiProcessor.clean_data()
    mx, my = miamiProcessor.get_features_and_target() # get dates and values
    mz = miamiProcessor.get_precipitation()
    
    orlandoProcessor.load_data()
    orlandoProcessor.clean_data()
    ox, oy = orlandoProcessor.get_features_and_target()
    oz = orlandoProcessor.get_precipitation()
    
    tallahasseeProcessor.load_data()
    #tallahasseeProcessor.clean_data()
    tx, ty = tallahasseeProcessor.get_features_and_target()
    tz = tallahasseeProcessor.get_precipitation()
    tx_unnorm = tallahasseeProcessor.unnormalized_date()

    # Prediction Graph
    if args.action == "predict":
        model = CustomPrecipitationPredictor()
        model.fit(tx, ty)
        predictions = model.predict(tx)
        Visualizer.plot_precipitation_trend(tx_unnorm, ty.tolist(), predictions.tolist())

    # Cluster Graph
    elif args.action == "cluster":
        data = list(zip(tx, ty))
        labels = custom_clustering(np.array(data), n_clusters=2)
        Visualizer.plot_clustered_data(data, labels.tolist())

    # Anomalies
    elif args.action == "anomalies":
        # Use just the target variable for anomaly detection
        model = CustomPrecipitationPredictor()

        # Prepare station data dictionary
        station_data = {
            'Tallahassee': {
                'values': tz,
                'anomalies': model.detect_anomalies(tx, tz)[0]
            },
            'Miami': {
                'values': mz,
                'anomalies': model.detect_anomalies(mx, mz)[0]
            },
            'Orlando': {
                'values': oz,
                'anomalies': model.detect_anomalies(ox, oz)[0]
            }
        }

        # Plot combined boxplot with anomalies
        Visualizer.plot_anomalies(station_data)


if __name__ == "__main__":
    main()
