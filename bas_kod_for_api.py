import requests

# Define the API endpoint
url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/NR/nr0001/'
# Make a GET request to fetch metadata
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")