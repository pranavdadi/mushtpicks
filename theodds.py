import requests
import json

# Step 1: Define the API endpoint and your API key
api_key = '483f35b5745eef23dcb36c470e5abec1'
url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'

# Step 2: Set up the parameters for the API request
params = {
    'apiKey': api_key,
    'regions': 'us',  # Get US-based sportsbooks
    'markets': 'h2h,spreads,totals',  # Get moneyline (h2h), spreads, and totals
    'oddsFormat': 'decimal',  # Can be 'decimal' or 'american'
    'dateFormat': 'iso',  # Use ISO date format
}

# Step 3: Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    odds_data = response.json()  # Parse the response into JSON format
    
    # Debugging step: Print the structure of the response
    print(json.dumps(odds_data, indent=4))  # Print the response in a readable format

    # Step 4: Save the odds to a text file
    with open('odds.txt', 'w') as file:
        for game in odds_data:
            # Print the game to see its structure
            print(game)
            
            # You can adjust this based on the printed structure
            # teams = game['teams']  # Adjust this line based on the actual data structure
            
            bookmakers = game['bookmakers']
            # file.write(f"Game: {teams[0]} vs {teams[1]}\n")  # Uncomment and adjust after structure is confirmed
            
            # Write odds from each bookmaker
            for bookmaker in bookmakers:
                file.write(f"Bookmaker: {bookmaker['title']}\n")
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        h2h_odds = market['outcomes']
                        file.write(f"Moneyline: {h2h_odds[0]['name']} {h2h_odds[0]['price']}, {h2h_odds[1]['name']} {h2h_odds[1]['price']}\n")
                    elif market['key'] == 'spreads':
                        spreads = market['outcomes']
                        file.write(f"Spread: {spreads[0]['name']} {spreads[0]['point']} {spreads[0]['price']}, {spreads[1]['name']} {spreads[1]['point']} {spreads[1]['price']}\n")
                    elif market['key'] == 'totals':
                        totals = market['outcomes']
                        file.write(f"Total: {totals[0]['name']} {totals[0]['point']} {totals[0]['price']}\n")
            file.write("\n")
    
    print("NFL odds have been successfully saved to odds.txt.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
