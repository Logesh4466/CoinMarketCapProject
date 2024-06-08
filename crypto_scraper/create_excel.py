import requests
import pandas as pd
import json  # Import the json module

# Define the URL for starting a scraping job
url = 'http://127.0.0.1:8000/api/taskmanager/scraping_status/b4e310d0-c8b5-4f2b-b65d-567ed383b705'

# Define the coin data
data = {'coin': 'ethereum'}

# Send a POST request to start scraping
response = requests.get(url, json=data)

# Check if the request was successful (status code 2xx)
if response.ok:
    # Extract JSON data from the response
    json_data = response.json()
    
    # Convert JSON data to a string
    json_string = json.dumps(json_data, indent=4)  # Convert JSON data to a string with indentation
    
    # Create a DataFrame with a single row containing the JSON string
    df = pd.DataFrame([json_string], columns=['JSON Data'])
    
    # Define the filepath for the Excel file
    excel_filepath = 'output.xlsx'

    # Write the DataFrame to an Excel file
    df.to_excel(excel_filepath, index=False)
    
    print(f"Excel file created successfully: {excel_filepath}")
else:
    print("Failed to receive a successful response from the server")
