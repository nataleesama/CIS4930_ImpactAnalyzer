import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Tuple, Optional
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from IPython.display import HTML
from plotly.subplots import make_subplots
#Working on: Implement a custom visualization technique for displaying multidimensional climate data, Create an animated visualization showing climate change over time
class Visualizer:
    @staticmethod
    def plot_precipitation_trend(years: List[int], precipitations: List[float], predictions: List[float]):
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        fig.add_trace(go.Scatter(x=[],y=[], name='Actual', line=dict(color='blue', width=3), mode='lines'))
    
        fig.add_trace(go.Scatter(x=[],y=[],name='Predicted',line=dict(color='red', width=3, dash='dash'),mode='lines'))
        
        frames = [go.Frame(data=[go.Scatter(x=years[:k+1], y=precipitations[:k+1]),go.Scatter(x=years[:k+1], y=predictions[:k+1])],name=str(year))for k, year in enumerate(years)]
        
        fig.frames = frames
        tick_vals = sorted(list(set([int(year) for year in years])))
        tick_labelAug = [f"8/{str(year)[-2:]}" for year in range(min(years),max(years))]
        fig.update_layout(
            title=f"Precipitation Trend vs Predicted Trend ({min(years)}-{max(years)})",
            xaxis=dict(
                title='Year',
                range=[min(years), max(years)],
                showgrid=True,
                tickmode='array',  # Use custom tick values
                tickvals=tick_vals,  # Only show whole years
                tickformat='d',
                ticktext = tick_labelAug
            ),
            yaxis=dict(
                title='Precipitation (normalized)',
                range=[min(precipitations+predictions)-0.1, max(precipitations+predictions)+0.1],
                showgrid=True
            ),
            hovermode='x unified',
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [
                            None, 
                            {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300}
                            }
                    ]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None], 
                        {
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ],
            "x": 0.1,
            "y": 0,
            "xanchor": "right",
            "yanchor": "top"
        }],
        sliders=[{
            "steps": [
                {
                    "args": [
                        [frame.name],
                        {"frame": {"duration": 0, "redraw": True},
                         "mode": "immediate"}
                    ],
                    "label": frame.name,
                    "method": "animate"
                }
                for frame in frames
            ],
            "x": 0.1,
            "len": 0.9,
            "currentvalue": {
                "prefix": "Year: ",
                "visible": True,
                "xanchor": "right"
            }
        }]
    )
    
    
        fig.update_layout(
            annotations=[
                dict(
                    x=0.95,
                    y=0.1,
                    xref="paper",
                    yref="paper",
                    text=f"Year: {years[0]}",
                    font=dict(size=20),
                    showarrow=False,
                    xanchor="right"
            )
        ]
        )
    
    
        for i, frame in enumerate(fig.frames):
            frame.layout.annotations = [
                dict(
                x=0.95,
                y=0.1,
                xref="paper",
                yref="paper",
                text=f"Year: {years[i]}",
                font=dict(size=20),
                showarrow=False,
                xanchor="right"
            )
        ]
    
        fig.show()
    
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

