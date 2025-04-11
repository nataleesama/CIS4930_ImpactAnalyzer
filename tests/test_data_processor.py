import unittest
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath('../src'))
from data_processor import DataProcessor #this should be in source
from DataCollection import CombineData, PullData

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.test_file = "../data/test_data.json"
        self.processor = DataProcessor(self.test_file)

    def test_load_data(self):
        print(f"Load Data Test:\n{self.processor.load_data()}\n\n")

    def test_clean_data(self):
        print(f"Before Clean:\n{self.processor.data}\n\n")
        self.processor.clean_data()
        print(f"After Clean:\n{self.processor.data}\n\n")

    def test_get_features_and_target(self):
        x, y = self.processor.get_features_and_target()
        dates = x.tolist()
        precips = y.tolist()
        print(f"Features:\n{dates}\n")
        print(f"Target:\n{precips}\n")

if __name__ == '__main__':
    unittest.main()

