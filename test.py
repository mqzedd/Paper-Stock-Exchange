import requests
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()
alphavantage_api_key = os.getenv("ALPHA_KEY")

# Define the API endpoint and parameters
url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={alphavantage_api_key}"

# Time the request to the API
start = time.time()
response = requests.get(url)
end = time.time()

# Print the time taken for the request
print(f"Time taken: {end - start} seconds")

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
