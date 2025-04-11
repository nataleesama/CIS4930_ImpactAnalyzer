import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from typing import Tuple


class CustomPrecipitationPredictor(BaseEstimator, RegressorMixin):
    def __init__(self, learning_rate: float = 0.01, n_iterations: int= 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias =0

    def fit(self, x: np.ndarray, y: np.ndarray) -> 'CustomPrecipitationPredictor':
        #using the skLearn linear regression line of best fit, from library
        self.model.fit(x,y)
        return self
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict(x) #from "LinearRegression()"
    
    def getSlope(self, x:np.array) -> float:
        """custom predication algorithm"""
        #data needs to translated and captured properly from api call PRE this funciton, then pass in such list
        x, y = x[:,0], x[:,1]
        n = len(x)
        num = n * np.sum(x * y) - np.sum(x) * np.sum(y)
        den = n * np.sum(x**2) - np.sum(x)**2
        return num / den if den != 0 else float('inf')
    
    def detect_anomalies(self, list:np.array, trend =0, threshold = 1) -> np.ndarray:
        """detect anomalies"""
        if trend ==0:
            trend = self.getSlope(x)
        x, y = list[:,0], list[:,1]
        mean_x, mean_y = np.mean(x), np.mean(y)
        intercept = mean_y - trend * mean_x  #pointslope

        outliers = []
        for i, (xi, yi) in enumerate(list):
            expected_y = trend * xi + intercept
            if abs(yi - expected_y) > threshold:
                outliers.append((xi, yi))
        return outliers
    
    def custom_clustering(data: np.ndarray, n_clusters: int) -> np.ndarray:
        pass

