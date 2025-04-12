import pandas as pd
import numpy as np
import datetime

class DataProcessor:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """Load climate data from JSON file."""
        data = pd.read_json(self.file_path)
        return data


    def clean_data(self) -> pd.DataFrame:
        """Remove rows with missing values and normalize precipitation
        data."""
        # Remove Rows with Missing Values 
        # Specifically in the precipitation column
        self.data.dropna(subset=['value'], inplace=True)
        self.data = self.data[self.data['value'] != 0.0] #remove all entries with no precipitation
        # if dropped, fix indexing
        self.data.reset_index(drop=True, inplace=True)

        # Min-Max Normalization
        # normalized = (x - min) / (max - min)
        min_precip = self.data['value'].min()
        max_precip = self.data['value'].max()

        # Find normalized value for each data row
        # Creates new column: 'normalized'
        self.data['normalized'] = self.data['value'].map(lambda x: (x - min_precip) / (max_precip - min_precip)) 
        
        #self.data['date'] = self.data['date'].apply(partitionDays)
        
        #min_date = self.data['date'].min()
        #max_date = self.data['date'].max()
        
        #self.data['normalizedDates'] = self.data['date'].map(lambda x: (x - min_date) / (max_date - min_date)) 

        x_ordinal = self.data['date'].map(lambda d: d.toordinal())

        # Step 2: Normalize
        min_date = x_ordinal.min()
        max_date = x_ordinal.max()

        self.data['datenormalized'] = x_ordinal.map(lambda d: (d - min_date) / (max_date - min_date))
        

        return self.data

    def unnormalized_date(self)->np.ndarray:
        year = [int(d.year) for d in self.data['date']]
        return year

    def get_features_and_target(self) -> tuple[np.ndarray,np.ndarray]: #this is what returns [DateArray, Precipitation values]
        """Split data into features (year, month) and target
        (precipitation)."""
        # Ensure No Empty Data
        self.clean_data()
        # Features
        #self.data['date'] = pd.to_datetime(self.data['date']) #from string to date time object
        #then convert to some fraction of a year in progress to another

        precipitation = self.data['normalized'].astype(float).to_numpy()
        dates = self.data['datenormalized'].astype(float).to_numpy()

        self.data['date'] = self.data['date'].to_numpy()
        self.data['dateFloat'] = self.data['date'].apply(partitionDays)
        
        return self.data['dateFloat'], precipitation #data in datetime formate 2024-01-10, preciptation

    def get_precipitation(self):
        return self.data['value']
        #return dates, precipitation #data in datetime formate 2024-01-10, preciptation

def normalize(dt):
    dt_series = pd.Series(dt)
    min_date = dt_series.min()
    max_date = dt_series.max()

    normalized = dt_series.map(lambda x: (x - min_date) / (max_date - min_date))
       
def partitionDays(dt):
    start_of_year = dt.replace(month=1, day=1)
    end_of_year = dt.replace(month=12, day=31)
    days_in_year = (end_of_year - start_of_year).days + 1
    day_of_year = (dt - start_of_year).days + 1
    return dt.year + (day_of_year - 1) / days_in_year

if __name__ == "__main__":
    #orlandoProcessor = DataProcessor("../data/orlandoData.json")
    #miamiProcessor = DataProcessor("../data/miamiData.json")
    tallahasseeProcessor = DataProcessor("../data/tallahasseeData.json")
    #print(processor.clean_data())
    #print(orlandoProcessor.get_features_and_target())
    print(tallahasseeProcessor.get_features_and_target())
   

