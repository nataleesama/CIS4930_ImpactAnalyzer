import pandas as pd
import numpy as np
import datetime

class DataProcessor:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """Load climate data from CSV file."""
        data = pd.read_json(self.file_path)
        return data


    def clean_data(self) -> pd.DataFrame:
        """Remove rows with missing values and normalize precipitation
        data."""
        # Remove Rows with Missing Values 
        # Specifically in the precipitation column
        self.data.dropna(subset=['value'], inplace=True) 

        # Min-Max Normalization
        # normalized = (x - min) / (max - min)
        min_precip = self.data['value'].min()
        max_precip = self.data['value'].max()

        # Find normalized value for each data row
        # Creates new column: 'normalized'
        self.data['normalized'] = self.data['value'].map(lambda x: (x - min_precip) / (max_precip - min_precip)) 

        return self.data


    def get_features_and_target(self) -> tuple[np.ndarray,np.ndarray]: #this is what returns [DateArray, Precipitation values]
        """Split data into features (year, month) and target
        (precipitation)."""
        # Features
        self.data['date'] = pd.to_datetime(self.data['date']) #from string to date time object
        #then convert to some fraction of a year in progress to another

        precipitation = self.data['value'].astype(int).to_numpy()

        self.data['date'] = self.data['date'].to_numpy()

        return self.data['date'], precipitation #data in datetime formate 2024-01-10, preciptation
    
if __name__ == "__main__":
    #orlandoProcessor = DataProcessor("../data/orlandoData.json")
    #miamiProcessor = DataProcessor("../data/miamiData.json")
    tallahasseeProcessor = DataProcessor("../data/tallahasseeData.json")
    #print(processor.clean_data())
    #print(orlandoProcessor.get_features_and_target())
    #print(miamiProcessor.get_features_and_target())
    print(tallahasseeProcessor.get_features_and_target())
