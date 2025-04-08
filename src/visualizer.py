import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Tuple, Optional
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from IPython.display import HTML

class Visualizer:
    @staticmethod
    def plot_precipitation_trend(years: List[int], precipitations: List[float], predictions: List[float]) -> None:
        #print("Display Precipitation Trend Graph Interactive/Static: ")
        #print("Static: 0")
        #print("Interactive: 1")
        interactive = True
        if interactive:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=precipitations, name='Actual', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=years, y=predictions, name='Predicted', line=dict(color='red', dash='dash')))
            fig.update_layout(
                title='Precipitation Trend Over Time (Interactive)',
                xaxis_title='Year',
                yaxis_title='Precipitation (normalized)',
                hovermode='x unified'
            )
            fig.show()
        else:
            plt.figure(figsize=(10, 6))
            plt.plot(years, precipitations, label='Actual')
            plt.plot(years, predictions, label='Predicted')
            plt.xlabel('Year')
            plt.ylabel('Precipitation (normalized)')
            plt.title('Precipitation Trend Over Time')
            plt.legend()
            plt.show()
    
    @staticmethod
    def plot_clustered_data(data: List[Tuple[float, float]], labels: List[int]) -> None:
        plt.figure(figsize=(10, 6)) #presetting the size for legibility
        
        dataArray = np.array(data)
        x = dataArray[:, 0]
        y = dataArray[:, 1]

        bounds = [2020,2025,0,100] #axis aka years, these would be the static markers for the xaxis
        plt.scatter(x, y)

        xTickYears = range(2020,2025)
        xTickLabels = [f"08/{year}" for year in xTickYears]

        plt.xticks(xTickYears,xTickLabels) #ticks need to be represented as integers, and aug 1 ~2020.58. fix later
        #plt.axis(bounds) #so this sets the max for both x and y
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

