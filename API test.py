import requests
import json
import pandas as pd

# Define the API endpoint
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/PR/PR0101/PR0101A/KPItotM'

# Define the start and end years
start_year = 2013
end_year = 2023

# List of ContentsCode to test individually, including the code for annual change

for code in contents_codes:
    # Prepare the JSON payload for the specified years and single ContentsCode
    payload = {
        "query": [
            {
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": [f"{year}M{month:02d}" for year in range(start_year, end_year + 1) for month in range(1, 13)]  # From 2013 to 2023, all months
                }
            },
            {
                "code": "ContentsCode",
                "selection": {
                    "filter": "item",
                    "values": [code]  # Test one code at a time
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    # Print the payload
    #print(f"Payload for ContentsCode {code}:")
    #print(json.dumps(payload, indent=2, ensure_ascii=False))

    # Make a POST request to fetch the data
    response = requests.post(url, json=payload)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the JSON response

        data = response.json()
        dimensions = data['dimension']
        tids = dimensions['Tid']['category']['index']
        values = data['value']

        # Create a mapping of months to their respective values
        month_value_map = {}
        
        for month_code, index in tids.items():
            month_value_map[month_code] = values[index]

        # Print the mapping
        print("Month to Value Mapping:")
        for month, value in month_value_map.items():
            print(f"{month}: {value}")

    else:
        print(f"Error for ContentsCode {code}: {response.status_code}")
        print(response.text)  # Print response text for further debugging
