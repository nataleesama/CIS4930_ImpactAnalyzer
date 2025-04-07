import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from typing import Tuple


class CustomPrecipitationPredictor(BaseEstimator, RegressorMixin):
    def __init__(self, learning_rate: float = 0.01, n_iterations: int= 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias =0
        self.model =LinearRegression()

    def fit(self, x: np.ndarray, y: np.ndarray) -> 'CustomPrecipitationPredictor':
        #using the skLearn linear regression line of best fit, from library
        self.model.fit(x,y)
        return self
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict(x) #from "LinearRegression()"
    
def detect_anomalies(time_series: np.ndarray, window_size: int=10,threshold: float = 2.0) -> np.ndarray:
    """detect anomalies"""
    anomalies = []
    rolling_mean = np.convolve(time_series, np.ones(window_size)/window_size, mode = 'valid')

    for i in range(len(rolling_mean)):
        window_data = time_series[i:i+window_size]
        std = np.std(window_data)
        if std ==0:
            continue
        z_score = (time_series[i+window_size -1]- rolling_mean[i])/std
        if abs(z_score) >threshold:
            anomalies.append(i+window_size -1)
        
    return np.array(anomalies)

def custom_clustering(data: np.ndarray, n_clusters: int) -> np.ndarray:
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_clusters,random_state=42)
    lables = kmeans.fit_predict(data)
    return lables
