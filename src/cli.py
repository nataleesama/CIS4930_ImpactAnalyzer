import argparse
from data_processor import DataProcessor
from algorithms import CustomPrecipitationPredictor
from visualizer import Visualizer
import numpy as np
import pandas as pd

def main():

    # Parse Arguments Choice
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["predict", "cluster", "anomalies"], required=True)
    args = parser.parse_args()

    # Load and preprocess data
    processorT = DataProcessor("../data/tallahasseeData.json")
    processorT.load_data()
    processorT.clean_data()
    x, y = processorT.get_features_and_target() # get dates and values
    z = processorT.get_precipitation()

    processorM = DataProcessor("../data/miamiData.json")
    processorM.load_data()
    processorM.clean_data()
    xM, yM = processorM.get_features_and_target() # get dates and values
    zM = processorM.get_precipitation()

    processorO = DataProcessor("../data/orlandoData.json")
    processorO.load_data()
    processorO.clean_data()
    xO, yO = processorO.get_features_and_target() # get dates and values
    zO = processorO.get_precipitation()
    #zero values are properly dropped

    
    # Prediction Graph
    if args.action == "predict":
        model = CustomPrecipitationPredictor()
        model.fit(x, y)
        predictions = model.predict(x)
        years = [row.year for row in x]
        Visualizer.plot_precipitation_trend(years, y.tolist(), predictions.tolist())

    # Cluster Graph
    elif args.action == "cluster":
        data = list(zip(x, y))
        #labels = custom_clustering(np.array(data), n_clusters=2)
        #Visualizer.plot_clustered_data(data, labels.tolist())

    # Anomalies
    elif args.action == "anomalies":
        # Use just the target variable for anomaly detection
        
        model = CustomPrecipitationPredictor()
    
        # Prepare station data dictionary
        station_data = {
            'Tallahassee': {
                'values': z,
                'anomalies': model.detect_anomalies(x, z)[0]
            },
            'Miami': {
                'values': zM,
                'anomalies': model.detect_anomalies(xM, zM)[0]
            },
            'Orlando': {
                'values': zO,
                'anomalies': model.detect_anomalies(xO, zO)[0]
            }
        }
    
        # Plot combined boxplot with anomalies
        Visualizer.plot_anomalies(station_data)
        #Debugging
        '''
        results_df = pd.DataFrame({
        'Date': x,
        'Precipitation': z,
        'Is_Anomaly': anomalies
        })
        with open("anomalies_output.txt", "w") as f:
            # Write header
            f.write("ANOMALY DETECTION RESULTS\n")
            f.write("="*40 + "\n\n")
            
            # Write all data points
            f.write("ALL DATA POINTS:\n")
            f.write("Date\t\tPrecipitation\tAnomaly\n")
            f.write("-"*40 + "\n")
            for date, precip, is_anomaly in zip(x, z, anomalies):
                f.write(f"{date}\t{precip:.6f}\t{is_anomaly}\n")
            
            # Write summary statistics
            f.write("\n\nSUMMARY STATISTICS:\n")
            f.write(f"Total points: {len(x)}\n")
            f.write(f"Anomalies detected: {sum(anomalies)}\n")
            f.write(f"Anomaly percentage: {sum(anomalies)/len(x):.2%}\n")
            
            # Write anomalies only
            f.write("\n\nDETECTED ANOMALIES:\n")
            f.write("Date\t\tPrecipitation\n")
            f.write("-"*40 + "\n")
            for date, precip, is_anomaly in zip(x, z, anomalies):
                if is_anomaly:
                    f.write(f"{date}\t{precip:.6f}\n")

            print("Results written to anomalies_output.txt")
        '''
        

if __name__ == "__main__":
    main()
