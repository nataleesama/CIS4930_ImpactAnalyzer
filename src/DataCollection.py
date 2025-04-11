import requests
import json
from pathlib import Path
from collections import defaultdict

# Configuration
endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
token = "kKyfMZMYhpcxvQUbmfhmpBBfYvvHXaOO"  # Replace with your token

stations = {
    "tallahassee": "GHCND:USW00093805",
    "nyc": "GHCND:USW00094728",
    "la": "GHCND:USW00023174"
}

datatypes = ["PRCP", "TMAX", "TMIN"]  # Precipitation, Max Temp, Min Temp

def pull_data(station_id: str, datatype: str, startdate: str, enddate: str) -> list:
    """Pull specific datatype for one station and date range"""
    params = {
        "datasetid": "GHCND",
        "datatypeid": datatype,
        "stationid": station_id,
        "startdate": startdate,
        "enddate": enddate,
        "limit": 31,
        "units": "metric"
    }
    headers = {"token": token}
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {datatype} for {station_id}: {str(e)}")
        return []

def combine_by_date(records: list) -> dict:
    """Combine different datatypes for the same date"""
    combined = defaultdict(dict)
    for record in records:
        date = record["date"][:10]  # YYYY-MM-DD
        combined[date][record["datatype"]] = record["value"]
    return combined

def save_station_data(data: dict, station_name: str):
    """Save combined data to single JSON file per station"""
    output_dir = Path("../data/stations_combined")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{station_name}.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} days to {output_file}")

def collect_all_data():
    date_ranges = [
        ("2020-08-01", "2020-08-31"),
        ("2021-08-01", "2021-08-31"),
        ("2022-08-01", "2022-08-31"),
        ("2023-08-01", "2023-08-31"),
        ("2024-08-01", "2024-08-31")
    ]

    for station_name, station_id in stations.items():
        all_records = []
        
        # Pull all datatypes
        for datatype in datatypes:
            for start, end in date_ranges:
                all_records.extend(pull_data(station_id, datatype, start, end))
        
        # Combine by date and save
        if all_records:
            combined_data = combine_by_date(all_records)
            save_station_data(combined_data, station_name)

if __name__ == "__main__":
    collect_all_data()