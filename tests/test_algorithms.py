import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.abspath('../src'))
from algorithms import CustomPrecipitationPredictor
from data_processor import DataProcessor

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.test_file = "../data/test_data.json"
        self.processor = DataProcessor(self.test_file)
        self.x, self.y = self.processor.get_features_and_target()
        self.dates = self.x.tolist()
        self.precipitations = self.y.tolist()
        self.test_model = CustomPrecipitationPredictor()

    def test_precipitation_detector(self):
        self.test_model.fit(self.x, self.y)
        test_prediction = self.test_model.predict(self.x)

        print("Predictions may be slightly skewed due to small dataset.")
        for r, p in zip(self.y, test_prediction):
            print(f"Real: {r}, Predicted: {p}")

    def test_detect_anomalies(self):
        anomalies = self.test_model.detect_anomalies(self.x, self.y)[0]
        print(f"Anamolies:\n", anomalies)
"""
    def test_custom_clustering(self):
        data = np.array([[1], [2], [100], [101]])
        labels = custom_clustering(data, n_clusters=2)
        self.assertEqual(len(labels), 4)
        self.assertEqual(len(set(labels)), 2)
"""

if __name__ == '__main__':
    unittest.main()