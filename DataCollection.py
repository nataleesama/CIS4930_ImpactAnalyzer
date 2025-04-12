import requests
import json

endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
token = "kKyfMZMYhpcxvQUbmfhmpBBfYvvHXaOO"
#output = "../data/climate_data.json"

def PullData(quantity, startdate, enddate, stationId): #add another measurement for multidimensional data
    parameters = {
        "datasetid": "GHCND",
        "datatypeid" : "PRCP",
        "stationid" : f"GHCND:{stationId}",
        "startdate" : startdate,               
        "enddate" : enddate,
        "limit" : quantity,
        "units" : "metric"
    }

    headers = {"token": token}
    response = requests.get(endpoint, params=parameters, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")


def CombineData(quantity, stationId,output):
    #Parameters to pull data from the last five years
    #API only allows 1 year increments per pull
    Dates =[
        ("2024-01-01", "2024-12-31"),
        ("2023-01-01", "2023-12-31"),
        ("2022-01-01", "2022-12-31"),
        ("2021-01-01", "2021-12-31"),
        ("2020-01-01", "2020-12-31") #capturing the whole year over the course of 5 years
    ]

    Data = []

    for startdate, enddate in Dates:
        PulledData = PullData(quantity, startdate, enddate,stationId=stationId)
        if PulledData:
            Data.extend(PulledData)
        else:
            print("Data Retrieval Failed")

    with open(output, "w") as file:
        json.dump(Data, file)


if __name__ == "__main__":
    #CombineData(365, stationId="USW00093805",output="../data/tallahasseeData.json") #tallahassee
    #CombineData(365, stationId="USW00012839",output="../data/miamiData.json") #miami
    #CombineData(365, stationId="USW00012815",output="../data/orlandoData.json") #jupiter
    CombineData(5, stationId="USW00093805",output="../data/test_data.json")
    CombineData(365, stationId="USW00014922", output="../data/minneapolisData.json")  # Minneapolis-St Paul Airport
    CombineData(365, stationId="USW00023183", output="../data/phoenixData.json")  # Phoenix Sky Harbor Airport
    pass