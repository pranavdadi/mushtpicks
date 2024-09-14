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
    'oddsFormat': 'american',  # Use 'american' format for odds
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
            
            bookmakers = game['bookmakers']
            
            # Write odds from each bookmaker
            for bookmaker in bookmakers:
                file.write(f"Bookmaker: {bookmaker['title']}\n")
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        h2h_odds = market['outcomes']
                        team1_price = h2h_odds[0]['price']
                        team2_price = h2h_odds[1]['price']

                        # Add "+" for positive odds
                        if team1_price > 0:
                            team1_price = f"+{team1_price}"
                        if team2_price > 0:
                            team2_price = f"+{team2_price}"

                        file.write(f"Moneyline: {h2h_odds[0]['name']} {team1_price}, {h2h_odds[1]['name']} {team2_price}\n")
                    
                    elif market['key'] == 'spreads':
                        spreads = market['outcomes']
                        team1_price = spreads[0]['price']
                        team2_price = spreads[1]['price']

                        # Add "+" for positive odds
                        if team1_price > 0:
                            team1_price = f"+{team1_price}"
                        if team2_price > 0:
                            team2_price = f"+{team2_price}"

                        file.write(f"Spread: {spreads[0]['name']} {spreads[0]['point']} {team1_price}, {spreads[1]['name']} {spreads[1]['point']} {team2_price}\n")
                    
                    elif market['key'] == 'totals':
                        totals = market['outcomes']
                        total_price = totals[0]['price']

                        # Add "+" for positive odds
                        if total_price > 0:
                            total_price = f"+{total_price}"

                        file.write(f"Total: {totals[0]['name']} {totals[0]['point']} {total_price}\n")
            file.write("\n")
    
    print("NFL odds have been successfully saved to odds.txt.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
