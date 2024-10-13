import requests
import json

# Set the API endpoint
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/NR/NR0103/NR0103A/NR0103ENS2010T01Kv'

# Define the parameters for the API request
params = {
    "query": [
        {
            "code": "Anvandningstyp",
            "selection": {
                "filter": "item",
                "values": ["BNPM"]
            }
        },
        {
            "code": "ContentsCode",
            "selection": {
                "filter": "item",
                "values": ["NR0103BV", "NR0103BW", "NR0103BX"]
            }
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": [
                    '2013K1', '2013K2', '2013K3', '2013K4',
                    '2014K1', '2014K2', '2014K3', '2014K4',
                    '2015K1', '2015K2', '2015K3', '2015K4',
                    '2016K1', '2016K2', '2016K3', '2016K4',
                    '2017K1', '2017K2', '2017K3', '2017K4',
                    '2018K1', '2018K2', '2018K3', '2018K4',
                    '2019K1', '2019K2', '2019K3', '2019K4',
                    '2020K1', '2020K2', '2020K3', '2020K4',
                    '2021K1', '2021K2', '2021K3', '2021K4',
                    '2022K1', '2022K2', '2022K3', '2022K4',
                    '2023K1', '2023K2'
                ]
            }
        }
    ],
    "response": {
        "format": "json"
    }
}

# Make the API request using POST
response = requests.post(url, json=params)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()
        BNP_data = data['data']

        # Initialize the dictionary to hold the values
        value_dict = {}

        # Iterate through each item in the BNP_data
        for item in BNP_data:
            key = item['key']  # Get the key
            values = item['values']  # Get the corresponding values
            
            # Extract the key name (e.g., "BNPM") and the corresponding values
            key_name = key[0]  # For example, "BNPM"
            year_quarter = key[1]  # E.g., "2013K1"
            year = year_quarter[:4]  # Extract year (first four characters)
            quarter = year_quarter[4:]  # Extract quarter (K1, K2, etc.)
            bnp_value = values[0]  # Löpande priser, mnkr
            bnp_percentage = values[2]  # BNP percentage

            # Store the values in the dictionary
            if key_name not in value_dict:
                value_dict[key_name] = {}
            if year not in value_dict[key_name]:
                value_dict[key_name][year] = {}
            value_dict[key_name][year][quarter] = {
                "value": bnp_value,
                "percentage": bnp_percentage
            }

        # Print the year, quarter, BNP value, and BNP percentage
        print("Year, Quarter, BNP Values and Percentages:")
        for key_name, years in value_dict.items():
            for year, quarters in years.items():
                for quarter, data in quarters.items():
                    print(f"Year: {year}, Quarter: {quarter}, BNP Value: {data['value']} mnkr, BNP Percentage: {data['percentage']}")

        # Optionally, save the structured data to a file
        with open('gnp_api.txt', 'w') as file:
            file.write(json.dumps(value_dict, indent=4, ensure_ascii=False))

    except json.JSONDecodeError:
        print("Response content is not valid JSON.")
        print("Response text:", response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")
