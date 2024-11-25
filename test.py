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

# output  = {
#    "Global Quote": {
#        "01. symbol": "IBM",
#        "02. open": "223.3500",
#        "03. high": "227.2000",
#        "04. low": "220.8900",
#        "05. price": "222.9700",
#        "06. volume": "5320740",
#        "07. latest trading day": "2024-11-22",
#        "08. previous close": "222.4000",
#        "09. change": "0.5700",
#        "10. change percent": "0.2563%"
#    }
# }
if response.status_code == 200:
    data = response.json()
    price = data.get("Global Quote", {}).get("05. price")
    if price:
        print(f"The price of AAPL is: {price}")
    else:
        print("Price not found in the response.")
else:
    print(f"Request failed with status code {response.status_code}")
