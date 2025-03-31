import requests
import json

endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
token = "kKyfMZMYhpcxvQUbmfhmpBBfYvvHXaOO"
output = "climate_data.json"

parameters = {
    "datasetid": "GHCND",
    "datatypeid" : "PRCP",                 #Precipitation
    "stationid" : "GHCND:USW00093805",     #Tallahassee Station
    "startdate" : "2024-01-01",
    "enddate" : "2025-01-01",
    "limit" : 100,
    "units" : "metric"
}

headers = {"token": token}

def pullData():
    response = requests.get(endpoint, params=parameters, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open(output, "w") as f:
            json.dump(data, f, indent=4)
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    pullData() 
    