import unittest
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath('../src'))
from visualizer import Visualizer
from algorithms import CustomPrecipitationPredictor

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.years = [2010, 2011, 2012, 2013, 2014]
        self.precipitations = [0.5, 0.6, 0.4, 0.7, 0.65]
        self.predictions = [0.52, 0.58, 0.42, 0.68, 0.63]
        
        self.cluster_data = [(1.0, 2.0), (1.1, 2.1), (5.0, 5.0), (5.1, 5.1), (1.2, 2.0)]
        self.cluster_labels = [0, 0, 1, 1, 0]
        
        self.time_series = [1.0, 2.0, 1.5, 10.0, 2.0, 1.8, 9.5]  
        self.anomalies = [False, False, False, True, False, False, True]
    #If graphs dont need to be displayed during testing, we add flag show_plots to all test functions

    def test_plot_precipitation_trend(self):
        
        Visualizer.plot_precipitation_trend(self.years, self.precipitations, self.predictions)


    def test_plot_clustered_data(self):
        
        Visualizer.plot_clustered_data(self.cluster_data, self.cluster_labels)


    def test_plot_anomalies_no_anomalies(self):

        z1 = [0.5, 2.0, 1.5, 2.0, 1.8]
        x1 = [0.998633, 1.000000, 0.000000, 0.000684, 0.749829]

        z2 = [0.3, 2.2, 1.7, 1.3, 1.7]
        x2 = [0.992233, 1.000000, 0.000000, 0.022684, 0.742229]

        z3 = [0.7, 1.8, 1.2, 2.1, 1.0]
        x3 = [0.933633, 1.000000, 0.000000, 0.003384, 0.743329]

        model = CustomPrecipitationPredictor()

        # Prepare station data dictionary
        station_data = {
            'Test 1': {
                'values': z1,
                'anomalies': model.detect_anomalies(x1, z1)[0]
            },
            'Test 2': {
                'values': z2,
                'anomalies': model.detect_anomalies(x2, z2)[0]
            },
            'Test 3': {
                'values': z3,
                'anomalies': model.detect_anomalies(x3, z3)[0]
            }
        }

        # Plot combined boxplot with anomalies
        Visualizer.plot_anomalies(station_data)
        

if __name__ == '__main__':
    unittest.main()