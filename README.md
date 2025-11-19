Poor Man's Flight Searcher

A Python application designed to query the Amadeus API for the cheapest flight prices across a broad date range, making it easier to find the most economical travel times.

Features
1. Amadeus API Integration
2. Cheapest Date Search
3. Flexible Duration: API is currently bugged.

Setup and Installation
1. Prerequisites: Python 3.10+
2. API Key Configuration (requires Amadeus Self-Service APIs)
- Sign up for an Amadeus developer account, obtain API Key and API Secret.
- Create .env file to add credentials.
- - AMADEUS_API_KEY="YOUR_CLIENT_ID_GOES_HERE"
- - AMADEUS_API_SECRET="YOUR_CLIENT_SECRET_GOES_HERE"

3. Environment Setup
- Create Venv: python3 -m venv .venv
- Activate Venv: source .venv/bin/activate
- Upgrade pip: python -m pip install --upgrade pip
- Install Dependencies: pip install -r requirements.txt

Usage
1. Modify Search Parameters in src/config/settings.py
2. Execute: python3 src/flight_searcher.py
3. Expected output: Authentication > send request > save raw response to JSON.
