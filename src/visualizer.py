import matplotlib
matplotlib.use('Agg')  # Ensures html translation

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Tuple, Optional
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from IPython.display import HTML
from plotly.subplots import make_subplots
import plotly.io
import plotly.express
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

        # Equivalent Code that allows html interactive abilities
        """
        x_value, y_value = zip(*data)

        fig = plotly.express.scatter(
            x=x_value,
            y=y_value,
            title="Clustered Data",
            labels={'x': 'Year', 'y': 'Precipitation'}
        )

        # Customize ticks
        fig.update_layout(
            xaxis=dict(
                tickvals=list(range(2020, 2025)),
                ticktext=[f"08/{year}" for year in range(2020, 2025)]
            ),
            xaxis_title='Date',
            yaxis_title='Precipitation',
            height=600
        )

        # to display in html
        return plotly.io.to_html(fig, full_html=False, include_plotlyjs='cdn')
        """

    @staticmethod
    def plot_anomalies(time_series, anomalies, dates=None):
        fig = go.Figure()
    
    # Convert to pandas Series for easier handling
        ts = pd.Series(time_series)
    
        ts.index = pd.to_datetime(dates)
    
    # Main time series
        fig.add_trace(go.Scatter(
            x=ts.index ,
            y=ts.values,
            mode='lines',
            name='Precipitation',
            line=dict(color='blue', width=2)
        ))
    
    # Anomalies
        if anomalies.any():
            anomaly_series = ts[anomalies]
            fig.add_trace(go.Scatter(
                x=anomaly_series.index,
                y=anomaly_series.values,
                mode='markers',
                name='Anomalies',
                marker=dict(
                    color='red',
                    size=10,
                    line=dict(width=2, color='black')
                ),
                hovertext=[f"Value: {y:.2f}" for y in anomaly_series.values]
        ))
    
    # Rolling mean
        window_size = min(10, len(ts)//4)
        fig.add_trace(go.Scatter(
            x=ts.index,
            y=ts.rolling(window_size).mean(),
            mode='lines',
            name=f'{window_size}-period mean',
            line=dict(color='green', dash='dash')
    ))
    
        fig.update_layout(
            title="Precipitation Anomalies",
            xaxis_title="Date",
            yaxis_title="Precipitation",
            hovermode="x unified"
    )
    
        fig.show()

