import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Tuple
class Visualizer:
    @staticmethod
    def plot_temperature_trend(years: List[int], temperatures: List[float], predictions: List[float]) -> None:
        plt.figure(figsize=(10, 6))
        plt.plot(years, temperatures, label='Actual')
        plt.plot(years, predictions, label='Predicted')
        plt.xlabel('Year')
        plt.ylabel('Temperature (normalized)')
        plt.title('Temperature Trend Over Time')
        plt.legend()
        plt.show()
    @staticmethod
    def plot_clustered_data(data: List[Tuple[float, float]], labels: List[int]) -> None:
        plt.figure(figsize=(10, 6)) 
        # Convert data to numpy array for easier handling
        data_array = np.array(data)
        x = data_array[:, 0]
        y = data_array[:, 1]
        
        # Create scatter plot with different colors for each cluster
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        
        for label, color in zip(unique_labels, colors):
            mask = np.array(labels) == label
            plt.scatter(x[mask], y[mask], c=[color], 
                        label=f'Cluster {label}', alpha=0.7, edgecolors='w')
        
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.title('Clustered Data Visualization')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_anomalies(time_series: List[float], anomalies: List[bool]) -> None:
        plt.figure(figsize=(10, 6))
        
   
        time_series = np.array(time_series)
        anomalies = np.array(anomalies)
    
        time_axis = np.arange(len(time_series))
        
        plt.plot(time_axis, time_series, 'b-', label='Normal', alpha=0.7)
        
        if any(anomalies):
            anomaly_points = time_series[anomalies]
            anomaly_times = time_axis[anomalies]
            plt.scatter(anomaly_times, anomaly_points, color='red', 
                       s=100, label='Anomaly', edgecolors='black', zorder=3)
        
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.title('Time Series with Anomalies Highlighted')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


test_data = {'years': list(range(1990, 2023)), 'temperatures': [14 + 0.1*(i-1990) for i in range(1990, 2023)],
'predictions': [14 + 0.11*(i-1990) for i in range(1990, 2023)]}
Visualizer.plot_temperature_trend(**test_data)

minimal_data = [(1,1), (1,2), (5,1), (5,2)]
minimal_labels = [0, 0, 1, 1]
Visualizer.plot_clustered_data(minimal_data, minimal_labels)

normal_data = [10, 11, 12, 11, 10, 9, 10, 11, 10, 9, 8, 10, 30, 10, 9, 8, 7, 8, 9, 10]
anomalies = [False]*12 + [True] + [False]*7
Visualizer.plot_anomalies(normal_data, anomalies)