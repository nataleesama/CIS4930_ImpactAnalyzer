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
    minneapolisProcessor = DataProcessor("../data/minneapolisData.json")
    phoenixProcessor = DataProcessor("../data/phoenixData.json")

    miamiProcessor.load_data()
    miamiProcessor.clean_data()
    mx, my = miamiProcessor.get_features_and_target() # get dates and values
    mz = miamiProcessor.get_precipitation()
    mc = (-80.19, 25.76)
    
    orlandoProcessor.load_data()
    orlandoProcessor.clean_data()
    ox, oy = orlandoProcessor.get_features_and_target()
    oz = orlandoProcessor.get_precipitation()
    oc = (-81.38, 28.54)
    tallahasseeProcessor.load_data()
    tallahasseeProcessor.clean_data()
    tx, ty = tallahasseeProcessor.get_features_and_target()
    tz = tallahasseeProcessor.get_precipitation()
    tc = (-84.28, 30.44)
    minneapolisProcessor.load_data()
    minneapolisProcessor.clean_data()
    Mx, My = minneapolisProcessor.get_features_and_target()
    Mz = minneapolisProcessor.get_precipitation()
    Mc = (-93.27, 44.98)
    phoenixProcessor.load_data()
    phoenixProcessor.clean_data()
    px, py = phoenixProcessor.get_features_and_target()
    pz = phoenixProcessor.get_precipitation()
    pc = (-112.07, 33.45)
    # Prediction Graph
    if args.action == "predict":
        model = CustomPrecipitationPredictor()
        model.fit(tx, ty)
        predictions = model.predict(tx)
        years = [row.year for row in tx]
        Visualizer.plot_precipitation_trend(years, ty.tolist(), predictions.tolist())

    # Cluster Graph
    elif args.action == "cluster":
        #cluster algorithm 
        station_data = {
        'Miami': {'values': mz, 'dates': mx,'coordinates': mc},
        'Orlando': {'values': oz, 'dates': ox,'coordinates': oc},
        'Tallahassee': {'values': tz, 'dates': tx,'coordinates': tc},
        'Minneapolis': {'values': Mz, 'dates': Mx,'coordinates': Mc},
        'Phoenix': {'values': pz, 'dates': px,'coordinates': pc}
        }
    
        # Perform clustering
        model = CustomPrecipitationPredictor()
        results = model.custom_clustering(station_data, n_clusters=3)
        Visualizer.plot_cluster(results)
        # Visualize results
        
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
