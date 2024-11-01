import requests
import json

# Define the new API endpoint
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/LE/LE0101/LE0101E'
code = ["LE01012021E01", "LE01012021E02"]  # Use relevant content codes from the output you provided

# Define the payload for the API request
payload = {
    "query": [
        {
            "code": "Indikator",
            "selection": {
                "filter": "item",
                "values": code  # Specify the desired content codes
            }
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]  # Include years from 2013 to 2023
            }
        }
    ],
    "response": {
        "format": "json"
    }
}

# Make the API request with the payload
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    data = response.json()
    # Save the data to a file
    with open('api_le0101_2013_2023.txt', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Data saved to api_le0101_2013_2023.txt")
else:
    print(f"Error: {response.status_code}, {response.text}")
