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


    def get_features_and_target(self) -> tuple[np.ndarray,np.ndarray]:
        """Split data into features (year, month) and target
        (precipitation)."""
        # Features
        self.data['date'] = pd.to_datetime(self.data['date']) #from string to date time object
        #then convert to some fraction of a year in progress to another

        precipitation = self.data['value'].astype(int).to_numpy()

        self.data['date_float'] = self.data['date'].apply(partitionDays) #this converts evenly among the 31 days to a float represented as a 'progression' in that year's august

        return self.data['date_float'], precipitation

def partitionDays(dt):
    return dt.year + (dt.day - 1) / 31
    
if __name__ == "__main__":
    processor = DataProcessor("../data/climate_data.json")
    #print(processor.clean_data())
    print(processor.get_features_and_target())
