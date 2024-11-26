import requests
from dotenv import load_dotenv
import os
import time

import database

# Load environment variables from .env file
load_dotenv()
alphavantage_api_key = os.getenv("ALPHA_KEY")

# Define the API endpoint and parameters
url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={alphavantage_api_key}"

# Time the request to the API
start = time.time()

print(database.fetch_data(1)[1])
end = time.time()

# Print the time taken for the request
print(f"Time taken: {end - start} seconds")
