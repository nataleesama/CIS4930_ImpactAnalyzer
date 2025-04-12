import numpy as np
import pandas as pd
from data_processor import normalize
from sklearn.base import BaseEstimator, RegressorMixin
from typing import Tuple
from sklearn.linear_model import HuberRegressor

class CustomPrecipitationPredictor(BaseEstimator, RegressorMixin):
    # Custom Linear Regression Model
    def __init__(self, learning_rate: float = 0.001, n_iterations: int= 10000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weight = 0
        self.bias = 0

    def fit(self, x: np.ndarray, y: np.ndarray) -> 'CustomPrecipitationPredictor':
        # Flatten and find length to loop through
        #x = x.apply(normalize)
        #x = pd.to_datetime(x)
        #x = x.map(lambda d: d.toordinal()).to_numpy()


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
        #x = pd.to_datetime(x)
        #x = x.map(lambda d: d.toordinal()).to_numpy()
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
    
    def custom_clustering(data: np.ndarray, n_clusters: int) -> np.ndarray:
        pass

