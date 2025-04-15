import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from typing import Tuple
from sklearn.linear_model import HuberRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import warnings
import os

class CustomPrecipitationPredictor(BaseEstimator, RegressorMixin):
    # Custom Linear Regression Model
    def __init__(self, learning_rate: float = 0.01, n_iterations: int= 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weight = 0
        self.bias = 0

    def fit(self, x: np.ndarray, y: np.ndarray) -> 'CustomPrecipitationPredictor':
        # Flatten and find length to loop through
        x = pd.to_datetime(x)
        x = x.map(lambda d: d.toordinal()).to_numpy()
        n = len(x)

        for i in range(self.n_iterations):
            # Linear Regression Prediction Formula: y = wx + b
            # predict the corresponding y value
            predicted_y = self.weight * x + self.bias

            # Determine how to improve weight based on error
            # Error = difference between predicted y and actual y
            update_w = (-2 / n) * np.sum((y - predicted_y) * x)

            # Determine how to improve bias based on error
            update_b = (-2 / n) * np.sum(y - predicted_y)

            # Make Improvements
            # Update/"train" weight
            self.weight -= self.learning_rate * update_w
            # Updated/"train" bias
            self.bias -= self.learning_rate * update_b
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        # return prediction post linear regression training
        x = pd.to_datetime(x)
        x = x.map(lambda d: d.toordinal()).to_numpy()
        return self.weight * x + self.bias
    
    def getSlope(self, x:np.array) -> float:
        """custom predication algorithm"""
        #data needs to translated and captured properly from api call PRE this funciton, then pass in such list
        x, y = x[:,0], x[:,1]
        n = len(x)
        num = n * np.sum(x * y) - np.sum(x) * np.sum(y)
        den = n * np.sum(x**2) - np.sum(x)**2
        return num / den if den != 0 else float('inf')
    
    def detect_anomalies(self, x: np.ndarray, y: np.ndarray, num_std_dev: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
        # Convert dates to ordinals
        x_ord = pd.to_datetime(x).map(lambda d: d.toordinal()).to_numpy()

        # Fit to log(y+1) to handle precipitation distribution
        y_log = np.log1p(y)
        X = x_ord.reshape(-1, 1)

        # Robust linear regression
        model = HuberRegressor().fit(X, y_log)
        pred = model.predict(X)
        residuals = y_log - pred

        # Calculate threshold based on absolute errors
        mad = np.median(np.abs(residuals - np.median(residuals)))
        threshold = num_std_dev * 1.4826 * mad  # Convert MAD to SD

        anomalies = np.abs(residuals) > threshold
        return anomalies, y
    
    def custom_clustering(self, station_data: dict, n_clusters: int = 3) -> dict:
        """
        Robust climate clustering with error handling and dimension matching
        
        Args:
            station_data: {
                'station_name': {
                    'values': precipitation_array,
                    'dates': date_array (optional)
                }
            }
            n_clusters: Number of climate zones (default: 3)
            
        Returns:
            Dictionary with cluster assignments and metrics
        """
        # Feature extraction
        stations = []
        feature_matrix = []
        coordinates = []
        for station, data in station_data.items():
            precip = np.array(data['values'])
            
            # 1. Handle empty/zero precipitation cases
            if len(precip) == 0:
                raise ValueError(f"Station {station} has no precipitation data")
                
            # 2. Calculate robust percentiles (handle zeros)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                percentiles = np.nanpercentile(precip, [10, 25, 50, 75, 90])
                
            # 3. Wet day characteristics
            wet_days = precip[precip > 0]
            features = [
                *percentiles,
                np.nanmean(wet_days) if len(wet_days) > 0 else 0,  # Intensity
                len(wet_days)/len(precip)  # Frequency
            ]
            stations.append(station)
            feature_matrix.append(features)
            coordinates.append(data['coordinates'])
        # Convert to numpy array with safe normalization
        features = np.array(feature_matrix)
        
        # Handle constant features (std=0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            features_norm = (features - np.nanmean(features, axis=0)) 
            stds = np.nanstd(features, axis=0)
            stds[stds == 0] = 1  # Avoid division by zero
            features_norm /= stds
        
        # Adjusted weights to match current 7 features (5 percentiles + 2 wet day metrics)
        weights = np.array([0.2, 0.15, 0.25, 0.15, 0.2,  # Percentiles
                            0.3, 0.25])  # Intensity and frequency
        
        # Distance matrix computation
        n = len(stations)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                diff = features_norm[i] - features_norm[j]
                dist = np.sqrt(np.sum(weights * diff**2))
                dist_matrix[i,j] = dist
                dist_matrix[j,i] = dist
        
        # Validation
        assert weights.shape[0] == features_norm.shape[1], \
            f"Weights dim {weights.shape} != Features dim {features_norm.shape[1]}"
        
        # Clustering
        cluster_model = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric='precomputed',  # The critical fix
        linkage='average',
        compute_full_tree='auto'
        )
    
        labels = cluster_model.fit_predict(dist_matrix)
    
        return {
            'labels': labels,
            'stations': stations,
            'coordinates': np.array(coordinates),
            'features': features_norm,
            'distance_matrix': dist_matrix,
            'feature_names': [
                'P10', 'P25', 'P50', 'P75', 'P90',
                'Precip Intensity',
                'Wet Day Frequency'
        ]
    }

