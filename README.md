Poor Man's Flight Searcher

A Python application designed to query the Amadeus API for the cheapest flight prices across a broad date range, making it easier to find the most economical travel times.

Features
1. Amadeus API Integration: Uses the Amadeus SDK for flight data access.
2. Cheapest Date Search: Queries the Flight Lowest Price Search API (/v1/shopping/flight-dates) to find the most cost-effective travel windows
3. Flexible Duration: Supports searching for a range of trip durations (e.g., 7 to 14 days).
4. Structured Output: Saves API results to a JSON file for easy analysis and subsequent processing.

Setup and Installation
Follow these steps to set up the project locally and configure access to the Amadeus API.
1. Prerequisites
You must have Python 3.10+ installed on your system.
2. API Key Configuration
This application requires credentials for the Amadeus Self-Service APIs.
- Get Keys: Sign up for an Amadeus developer account and obtain your API Key (Client ID) and API Secret (Client Secret).
- Create .env file: In the root directory of the project, create a file named .env and add your credentials:

Code snippet# .env file content
AMADEUS_API_KEY="YOUR_CLIENT_ID_GOES_HERE"
AMADEUS_API_SECRET="YOUR_CLIENT_SECRET_GOES_HERE"

3. Environment Setup
It is highly recommended to use a virtual environment to manage dependencies.
- Create Venv: python3 -m venv .venv
- Activate Venv: source .venv/bin/activate
- Upgrade pip: python -m pip install --upgrade pip
- Install Dependencies: pip install -r requirements.txt

Usage
Once the environment is set up and activated, you can run the flight search logic from the main script.
1. Modify Search Parameters
All search parameters (Origin, Destination, Date Range, Duration) are currently hardcoded in the main execution file.

Open src/config/settings.py and modify the params:
params = {
    ORIGIN = 'xxx' # Requires IATA code
    DESTINATION = "xxx" # Requires IATA code
    START_DATE = "2025-11-22" # Date format: YYYY-MM-DD
    END_DATE: str = "2026-01-01" # Date format: YYYY-MM-DD, must be after START_DATE
    DEPARTURE_DATE_RANGE = "2025-12-01,2025-12-31" # Date format with comma separator: YYYY-MM-DD,YYYY-MM-DD
    DURATION: str = "12,14" # Two integers with comma separator
    CURRENCY: str = "MYR"
    NONSTOP: bool = True
    ADULTS: int = 1 # No. of adults
    MAX_PRICE: int = 1_300 # Price ceiling willing to pay
}

2. Execute the Search
Run the main script from the project root: python3 src/flight_searcher.py
3. View Results
The script will:
- Authenticate with the Amadeus API using the keys from .env.
- Send the request to the cheapest date search endpoint.
- Save the raw response data to: data/raw_cheapest_flights.json # Hardcoded name, change in flight_searcher.py
