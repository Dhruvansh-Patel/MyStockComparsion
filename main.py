import requests
import csv
import matplotlib.pyplot as plt

filename = ''

# Function to fetch stock symbols from Alpha Vantage
def get_stock_symbols(company_name):
    # API key and URL
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query'

    # Parameters for API request
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': company_name,
        'apikey': api_key
    }

    # Send GET request to Alpha Vantage API
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Function to fetch stock data based on symbol
def get_stock_data(symbol):
    # API key and URL
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query'

    # Parameters for API request
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': api_key
    }

    # Send GET request to Alpha Vantage API
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Function to check if stock symbol exists in CSV file
def stock_symbol_exists(symbol):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == symbol:
                return True
    return False

# Function to save data to CSV
def save_data_to_csv(data, filename):
    header = ['Symbol', 'Company Name', 'Current Price', 'Price Change', 'Percent Change']

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)

        # Check if the file is empty
        file_empty = file.tell() == 0

        if file_empty:
            writer.writerow(header)

        for stock_info in data:
            symbol = stock_info['01. symbol']

            # Check if the stock symbol already exists
            if stock_symbol_exists(symbol):
                # Remove existing row
                remove_stock_symbol(symbol)

            # Extract other stock data
            # company_name = stock_info['02. name']
            current_price = stock_info['05. price']
            price_change = stock_info['09. change']
            percent_change = stock_info['10. change percent']

            row = [symbol, current_price, price_change, percent_change]
            writer.writerow(row)

# Function to remove stock symbol from CSV file
def remove_stock_symbol(symbol):
    rows = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != symbol:
                rows.append(row)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Function to display stock information
def display_stock_info(stock_info):
    symbol = stock_info['01. symbol']
    # company_name = stock_info['02. name']
    current_price = stock_info['05. price']
    price_change = stock_info['09. change']
    percent_change = stock_info['10. change percent']
    print("------------------------")
    print(f"Symbol: {symbol}")
    print(f"Company Name: {company_name}")
    print(f"Current Price: {current_price}")
    print(f"Price Change: {price_change}")
    print(f"Percent Change: {percent_change}")
    print("------------------------")

# Main program loop
while True:
    # Get user input to choose between comparing stored data or fetching new data
    compare_choice = input("To store new/update stock data type 'get'\n-----------------------\nTo compare existing data type 'compare'\n---------------------\n(Enter 'exit' to quit): ")

    if compare_choice.lower() == 'exit':
        break

    if compare_choice.lower() == 'compare':
        # Read data from CSV file
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                data.append(row)
                

        # Get user input for stocks to compare
        stocks_to_compare = input("Enter stock symbols to compare (comma-separated): ").split(',')

        # Filter data for selected stocks
        filtered_data = [row for row in data if row[0] in stocks_to_compare]

        if len(filtered_data) < len(stocks_to_compare):
            print("Warning: Some symbols do not exist in the stored data.")

        # Extract necessary columns
        symbols = [row[0] for row in filtered_data]
        prices = [float(row[1]) for row in filtered_data]
        price_changes = [float(row[2]) for row in filtered_data]
        percent_changes = [float(row[3].strip('%')) for row in filtered_data]

        # Plotting the graphs for each data point
        plt.figure(figsize=(10, 6))

        # Plot current prices
        plt.subplot(2, 2, 1)
        plt.bar(symbols, prices, color='b')
        plt.xlabel('Stock Symbol')
        plt.ylabel('Current Price')
        plt.title('Current Prices')

        # Plot price changes
        plt.subplot(2, 2, 2)
        plt.bar(symbols, price_changes, color='r')
        plt.xlabel('Stock Symbol')
        plt.ylabel('Price Change')
        plt.title('Price Changes')

        # Plot percent changes
        plt.subplot(2, 2, 3)
        plt.bar(symbols, percent_changes, color='g')
        plt.xlabel('Stock Symbol')
        plt.ylabel('Percent Change')
        plt.title('Percent Changes')

        # Adjust spacing between subplots
        plt.tight_layout()

        plt.show()

    elif compare_choice.lower() == 'get':
    # Fetch new data and compare
     company_name = input("Enter Company Name: ")
     symbol_data = get_stock_symbols(company_name)
    
    else :
        symbol_data = None

    if symbol_data == None :
        print("Invalid choice")
        break

    if 'bestMatches' in symbol_data:
        best_matches = symbol_data['bestMatches']
        if best_matches:
            stock_data = []

            # Display available options for stock symbols
            print("Available stock symbols:")
            for i, match in enumerate(best_matches, 1):
                symbol = match['1. symbol']
                company_name = match['2. name']
                print(f"{i}. {symbol} - {company_name}")

            # Get user input for selecting stock symbol
            symbol_choice = input("Enter the stock symbol you want to store: ")

            # Find the selected stock symbol
            selected_stock = None
            for match in best_matches:
                if match['1. symbol'] == symbol_choice:
                    selected_stock = match
                    break

            if selected_stock:
                symbol = selected_stock['1. symbol']
                company_name = selected_stock['2. name']

                # Fetch stock data using symbol
                stock_data_single = get_stock_data(symbol)

                if 'Global Quote' in stock_data_single:
                    stock_info = stock_data_single['Global Quote']
                    display_stock_info(stock_info)
                    stock_data.append(stock_info)
                    save_data_to_csv(stock_data, filename)
                    print(f"Data saved to {filename}.")
                    break
                else:
                    print(f"No stock data available for symbol: {symbol}")
                    break
            else:
                print("Invalid stock symbol choice.")

        else:
            print("No matching companies found.")
            break
    else:
        print("Stock data not available.")
