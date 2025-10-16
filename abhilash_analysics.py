import yfinance as yf
import pandas as pd
import os

def download_and_save_stock_data(ticker_list, file_path, period="60d", interval="5m"):
    """
    Downloads historical stock data for a given list of tickers and saves it to a CSV file.
    Note: For 5m interval, Yahoo Finance limits data to the last 60 days.
    """
    print(f"Attempting to download data for: {', '.join(ticker_list)}...")
    print(f"Period: {period}, Interval: {interval}")
    try:
        data = yf.download(
            ticker_list,
            period=period,
            interval=interval,
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )

        if data.empty:
            print("No data downloaded. Check your parameters; intraday data is not available for all tickers.")
            return None
        else:
            print("Successfully downloaded data!")
            
            data.to_csv(file_path)
            
            print(f"Data successfully saved to: {os.path.abspath(file_path)}")
            
            return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# This block runs only when you execute this script directly
if __name__ == "__main__":
    # Define the companies you're interested in
    tickers_to_fetch = ["AAPL", "NVDA", "META", "MSFT", "NFLX", "GOOGL"]
    
    # Updated filename to reflect the new interval
    output_filename = "stock_data_60d_5m.csv"

    # Call the function to download and save the data with the new parameters
    stock_data = download_and_save_stock_data(tickers_to_fetch, output_filename)

    # (Optional) Check if data was returned and print a sample
    if stock_data is not None:
        print("\n--- Quick sample of downloaded data (Apple) ---")
        print(stock_data['AAPL'].tail())