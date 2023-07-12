# Stock Data Comparison

This Python script allows you to fetch stock symbols and data from the Alpha Vantage API, store the data in a CSV file, and compare and visualize the data using matplotlib.

## Prerequisites

- Python 3.x
- `requests` library
- `matplotlib` library
- CSV file with appropriate headers

## Installation

 1. Clone the repository:

git clone https://github.com/dhruvansh-patel/MyStockComparsion.git

2.Install the required dependencies:

pip install requests matplotlib

#Usage

1.Modify the script:

Replace 'YOUR_API_KEY' in the get_stock_data function with your Alpha Vantage API key.

2.Create and set CSV file

Create a CSV file with pre added headers for the program namely : Symbol', 'Company Name', 'Current Price', 'Price Change', 'Percent Change'.
Set the filename vairable to the path of the CSV file. 	


3. Run the script :

python main.py

4. Follow the prompts:

Enter 'compare' to compare existing stock data or 'fetch' to fetch new data.
If comparing, enter the stock symbols to compare (comma-separated).
If fetching, enter the company name for which you want to fetch stock data.

5.View the results:

If comparing, the script will display graphs comparing the selected stocks' current prices, price changes, and percent changes.
If fetching, the script will display the fetched stock information and save it to the CSV file.


