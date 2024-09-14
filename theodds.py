import requests
import json

# Function to convert decimal odds to American odds
def decimal_to_american(decimal_odds):
    if decimal_odds >= 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return round(american_odds)

# Step 1: Define the API endpoint and your API key
api_key = '483f35b5745eef23dcb36c470e5abec1'
url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'

# Step 2: Set up the parameters for the API request
params = {
    'apiKey': api_key,
    'regions': 'us',  # Get US-based sportsbooks
    'markets': 'h2h,spreads,totals',  # Get moneyline (h2h), spreads, and totals
    'oddsFormat': 'decimal',  # Using decimal odds to convert them to American
    'dateFormat': 'iso',  # Use ISO date format
}

# Step 3: Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    odds_data = response.json()  # Parse the response into JSON format
    
    # Debugging step: Print the structure of the response
    print(json.dumps(odds_data, indent=4))  # Print the response in a readable format

    # Step 4: Save the odds to a text file with decimal-to-American conversion
    with open('odds.txt', 'w') as file:
        for game in odds_data:
            # Extract teams and bookmakers
            bookmakers = game['bookmakers']
            
            # Write odds from each bookmaker
            for bookmaker in bookmakers:
                file.write(f"Bookmaker: {bookmaker['title']}\n")
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        h2h_odds = market['outcomes']
                        # Convert to American odds
                        team_1_odds = decimal_to_american(h2h_odds[0]['price'])
                        team_2_odds = decimal_to_american(h2h_odds[1]['price'])
                        file.write(f"Moneyline: {h2h_odds[0]['name']} {team_1_odds}, {h2h_odds[1]['name']} {team_2_odds}\n")
                    elif market['key'] == 'spreads':
                        spreads = market['outcomes']
                        team_1_spread_odds = decimal_to_american(spreads[0]['price'])
                        team_2_spread_odds = decimal_to_american(spreads[1]['price'])
                        file.write(f"Spread: {spreads[0]['name']} {spreads[0]['point']} {team_1_spread_odds}, {spreads[1]['name']} {spreads[1]['point']} {team_2_spread_odds}\n")
                    elif market['key'] == 'totals':
                        totals = market['outcomes']
                        over_odds = decimal_to_american(totals[0]['price'])
                        file.write(f"Total: {totals[0]['name']} {totals[0]['point']} {over_odds}\n")
            file.write("\n")
    
    print("NFL odds have been successfully saved to odds.txt.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
