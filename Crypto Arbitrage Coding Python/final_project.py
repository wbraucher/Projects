#note: Asked GBT to help with serveral of the specific Alpaca commands used in this file since I am unfamiliar with the syntax.
#Importing Libraries
import requests
import json
import os
import networkx as nx
import csv
import datetime

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

#Alpaca Set up (API, Trading, etc)
API_KEY = 'PKXI6P27X9CGDXDZI4T0'
SECRET_KEY = 'd4BPVYBtHzNMmUxCzn4FXdk4NIyK1hfVqgqcacWI'
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
available_assets = [asset.symbol for asset in trading_client.get_all_assets() if asset.asset_class == 'crypto']

#Setting up the directory to have files put into final project folder and respective folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
TRADES_FOLDER = os.path.join(BASE_DIR, 'trades')
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(TRADES_FOLDER, exist_ok=True)

#Setting up URL for grabbing coin exchange rates
url = "https://api.coingecko.com/api/v3/simple/price?ids=aave,avalanche,basic-attention-token,bitcoin-cash,bitcoin,curve-dao-token,dogecoin,polkadot,ethereum,the-graph,chainlink,litecoin,maker,shiba-inu,sushiswap,uniswap,tezos,yearn-finance&vs_currencies=aave,bat,btc,bch,link,crv,doge,eth,ltc,mkr,dot,shib,xtz,grt,uni,yfi%22"
response = requests.get(url)
data = response.json()

#Creating a dictionary for all my coin ID and Names
id_to_symbol = {
    'aave': 'aave',
    'basic-attention-token': 'bat',
    'bitcoin': 'btc',
    'bitcoin-cash': 'bch',
    'chainlink': 'link',
    'curve-dao-token': 'crv',
    'dogecoin': 'doge',
    'ethereum': 'eth',
    'litecoin': 'ltc',
    'maker': 'mkr',
    'polkadot': 'dot',
    'shiba-inu': 'shib',
    'tezos': 'xtz',
    'the-graph': 'grt',
    'uniswap': 'uni',
    'yearn-finance': 'yfi'
}

#Saving exchange rates to data folder using specific format
def save_exchange_rates(data, timestamp):
    filename = os.path.join(DATA_FOLDER, f"currency_pair_{timestamp.strftime('%Y.%m.%d:%H.%M')}.txt")
    with open(filename, mode='w') as f:
        for from_currency, rates in data.items():
            for to_currency, rate in rates.items():
                f.write(f"{from_currency},{to_currency},{rate}\n")

#Adding a timestamp for each currency pair for data folder
timestamp = datetime.datetime.now()   
save_exchange_rates(data, timestamp)

 
#create directed graph
g = nx.DiGraph()
edges = []

#build edges from API by looping through dictionary of coins and exchange rates and converts coin ID to their symbol like BTC
for coin_id, exchange_rates in data.items():
    from_currency = id_to_symbol[coin_id]

    #loop through all conversion rates for the current currency
    for to_currency, rate in exchange_rates.items():

         #skip if the conversion is itself
        if from_currency != to_currency:
            edge = (from_currency, to_currency, rate)
            edges.append(edge)


#add all edges to graph
g.add_weighted_edges_from(edges)

#function to compute the total weight of a path by multiplying
def compute_path_weight(graph, path):
    weight = 1.0
    for i in range(len(path) - 1):
        weight *= graph[path[i]][path[i + 1]]['weight']
    return weight

#Submitting a trade order through Alpaca using USD and skipping if it is not available on Alpaca
def submit_trade(from_currency, to_currency, usd_amount):
    symbol = f"{to_currency.upper()}/USD"
    if symbol not in available_assets:
        print(f"Skipping trade for {symbol}: Not available on Alpaca.")
        return

    #Creating a market order to buy a specific crypto with 100 dollars. 
    order_data = MarketOrderRequest(
        symbol=symbol,
        notional=usd_amount,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )
    
    #Submitting the market order through Alpaca and confirming the order
    trading_client.submit_order(order_data)
    print(f"Submitted order: BUY ${usd_amount:.2f} of {symbol}")
    


#Logging the trade details into a CSV file inside the trades folder
def log_trade(from_currency, to_currency, amount_usd, timestamp):
    filename = os.path.join(TRADES_FOLDER, f'trades_{timestamp.date()}.csv')
    file_exists = os.path.isfile(filename)
    
    # Open the CSV file for today's date
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If file is new, write header row
        if not file_exists:
            writer.writerow(['timestamp', 'from_currency', 'to_currency', 'amount_usd'])
        
        #Append trade details
        writer.writerow([timestamp, from_currency.upper(), to_currency.upper(), f"{amount_usd:.2f}"])


#Execute a cycle trade starting with USD, buying the first crypto, then buying the second crypto and so on.
#Note: Crypto to Crypto exchange doesn't work automatically through Alpaca yet so we can't exchange the crypto and sell it.
#So I just used USD to simuulate what it would be like if we could.

def execute_cycle_trade(path):
    starting_usd = 100
    timestamp = datetime.datetime.now()
    print(f"Starting chained trade with ${starting_usd:.2f} USD.")

    #Buy first crypto with USD
    from_currency = path[0]
    to_currency = path[1]
    symbol = f"{to_currency.upper()}/USD"

    #Check to see if the cryptocurrency is available for trading on Alpaca and submitting a market order if available. If not then it will skip and exit the cycle early.
    if symbol in available_assets:
        submit_trade(from_currency, to_currency, starting_usd)
        log_trade(from_currency, to_currency, starting_usd, timestamp)
        print(f"Bought {to_currency.upper()} with ${starting_usd:.2f} USD.")
    else:
        print(f"Skipping trade for {to_currency.upper()} (not available on Alpaca).")
        return


#function to find arbitrage opportunities between all pairs of currency
def find_arbitrage_opportunities(graph, currencies):
    best_opportunity = None
    worst_opportunity = None
    best_factor_global = float('-inf')
    worst_factor_global = float('inf')
    cycles_traded = 0

    timestamp = datetime.datetime.now()
    
    #looping through all combinations of my source and target currencies
    for from_currency in currencies:
        for to_currency in currencies:
            if from_currency == to_currency:
                continue
            
            #finding all forward and backwards simple paths
            forward_paths = list(nx.all_simple_paths(graph, source=from_currency, target=to_currency))
            backward_paths = list(nx.all_simple_paths(graph, source=to_currency, target=from_currency))


            #skip if there aren't complete paths
            if not forward_paths or not backward_paths:
                continue

            #Initialize variables to track the best arbitrage opportunity 
            best_factor_pair = float('-inf')
            best_forward_path = None
            best_backward_path = None

            #loop through all forward paths
            for f_path in forward_paths:
                f_weight = compute_path_weight(graph, f_path)

                #loop through all backwards paths
                for b_path in backward_paths:
                    b_weight = compute_path_weight(graph, b_path)

                    #Calculate the combined weight factor
                    weight_factor = f_weight * b_weight

                    #Update the best arbitrage opportunity for a pair if the current weight factor is higher
                    if weight_factor > best_factor_pair:
                        best_factor_pair = weight_factor
                        best_forward_path = f_path
                        best_backward_path = b_path

            #Print the best arbitrage weight factor found between the currencies
            print(f"\n--- {from_currency.upper()} to {to_currency.upper()} ---")
            print(f"Best weight factor: {best_factor_pair:.6f}")

            #If arbitrage exists then submit trades along the best forward path. Otherwise say that there is no arbitrage.
            if best_factor_pair > 1:
                print("Arbitrage detected! Submitting a trade.")
                for i in range(len(best_forward_path) - 1):
                    submit_trade(best_forward_path[i], best_forward_path[i + 1], 100)
                    log_trade(best_forward_path[i], best_forward_path[i + 1], 100, timestamp)
                cycles_traded += 1
            else:
                print("No arbitrage.")

            #Update the overall worst arbitrage opportunity if the current one is smaller
            if best_factor_pair < worst_factor_global:
                worst_factor_global = best_factor_pair
                worst_opportunity = (best_forward_path, best_backward_path)

            #Update the overall best arbitrage opportunity if the current one is greater
            if best_factor_pair > best_factor_global:
                best_factor_global = best_factor_pair
                best_opportunity = (best_forward_path, best_backward_path)

    #Print the summary of the smallest and largest overall arbitrage weight factors found
    print(f"\nSmallest global weight factor: {worst_factor_global:.6f}")
    print(f"Paths: {worst_opportunity[0]} {worst_opportunity[1]}\n")
    print(f"Largest global weight factor: {best_factor_global:.6f}")
    print(f"Paths: {best_opportunity[0]} {best_opportunity[1]}")

    #Create a summary dictionary
    summary = {
        "timestamp": str(timestamp),
        "total_currency_pairs": sum(len(v) for v in data.values()),
        "trades_made": cycles_traded,
        "greatest_weight_factor": best_factor_global,
        "smallest_weight_factor": worst_factor_global,
    }

    #Save the summary dictionary of today's trading activity into results.json
    results_path = os.path.join(BASE_DIR, 'results.json')
    with open(results_path, 'w') as f:
        json.dump(summary, f, indent=4)


#calling the function to search for arbitrage
find_arbitrage_opportunities(g, list(g.nodes))