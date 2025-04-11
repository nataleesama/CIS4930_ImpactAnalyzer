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

    orlandoProcessor.load_data()
    orlandoProcessor.clean_data()
    ox, oy = orlandoProcessor.get_features_and_target()

    tallahasseeProcessor.load_data()
    tallahasseeProcessor.clean_data()
    tx, ty = tallahasseeProcessor.get_features_and_target()

    # Prediction Graph
    if args.action == "predict":
        model = CustomPrecipitationPredictor()
        model.fit(tx, ty)
        predictions = model.predict(tx)
        years = [row.year for row in tx]
        Visualizer.plot_precipitation_trend(years, ty.tolist(), predictions.tolist())

    # Cluster Graph
    elif args.action == "cluster":
        data = list(zip(tx, ty))
        labels = custom_clustering(np.array(data), n_clusters=2)
        Visualizer.plot_clustered_data(data, labels.tolist())

    # Anomalies
    elif args.action == "anomalies":
        # Use just the target variable for anomaly detection
        #anomalies = detect_anomalies(y)
        #Visualizer.plot_anomalies(y.tolist()) #y is the get features and target, but want to convert this to the separate stations
        Visualizer.plot_anomalies(my.tolist(),oy.tolist(),ty.tolist()) #send in these separated lists, and handle in that visualizeer funciton


if __name__ == "__main__":
    main()
