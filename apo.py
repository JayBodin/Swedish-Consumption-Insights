import requests

# Define the API endpoint
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/PR/PR0101/PR0101A/KPItotM'

# Define the start and end years
start_year = 2013
end_year = 2023

# List of ContentsCode to test individually, including the code for annual change
contents_codes = ["000004VV", "000004VT"]  # KPI and annual change codes

# Dictionary to hold combined month-value mappings
combined_month_value_map = {}

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
        for month_code, index in tids.items():
            if month_code not in combined_month_value_map:
                combined_month_value_map[month_code] = {}
            combined_month_value_map[month_code][code] = values[index]

    else:
        print(f"Error for ContentsCode {code}: {response.status_code}")
        print(response.text)  # Print response text for further debugging

# Print the combined month to value mapping
print("Month to Value Mapping:")
for month, values in combined_month_value_map.items():
    kpi_value = values.get("000004VT")  # KPI value
    yearly_change_value = values.get("000004VV")  # Yearly change value
    print(f"{month}: KPI: {kpi_value}, Yearly Change: {yearly_change_value}")
