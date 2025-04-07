import requests
import json

endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
token = "kKyfMZMYhpcxvQUbmfhmpBBfYvvHXaOO"
output = "../data/climate_data.json"

def PullData(startdate, enddate):
    parameters = {
        "datasetid": "GHCND",
        "datatypeid" : "PRCP",                 #Precipitation
        "stationid" : "GHCND:USW00093805",     #Tallahassee Station
        "startdate" : startdate,               
        "enddate" : enddate,
        "limit" : 31,
        "units" : "metric"
    }

    headers = {"token": token}
    response = requests.get(endpoint, params=parameters, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")


def CombineData():
    Data = []

    #Parameters to pull data from the last five years
    #API only allows 1 year increments per pull
    #August: Typically Rainiest Month
    
    Dates =[
        ("2024-08-01", "2024-08-31"),
        ("2023-08-01", "2023-08-31"),
        ("2022-08-01", "2022-08-31"),
        ("2021-08-01", "2021-08-31"),
        ("2020-08-01", "2020-08-31")
    ]

    for startdate, enddate in Dates:
        PulledData = PullData(startdate, enddate)
        Data.extend(PulledData)

    with open(output, "w") as file:
        json.dump(Data, file)


if __name__ == "__main__":
    CombineData()
    