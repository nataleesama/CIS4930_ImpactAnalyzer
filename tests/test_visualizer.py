import unittest
import numpy as np
from visualizer import Visualizer
import matplotlib.pyplot as plt

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
    '''    
    def tearDown(self):
        if self.show_plots:
            plt.show()
        plt.close('all')
    '''
    def test_plot_precipitation_trend(self):
        
        Visualizer.plot_precipitation_trend(self.years, self.precipitations, self.predictions)


    def test_plot_clustered_data(self):
        
        Visualizer.plot_clustered_data(self.cluster_data, self.cluster_labels)
        

    def test_plot_anomalies(self):
    
        Visualizer.plot_anomalies(self.time_series, self.anomalies)

    def test_plot_anomalies_no_anomalies(self):

        time_series = [1.0, 2.0, 1.5, 2.0, 1.8]
        anomalies = [False, False, False, False, False]
        
        Visualizer.plot_anomalies(time_series, anomalies)

if __name__ == '__main__':
    unittest.main()