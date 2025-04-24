import yfinance as yf
import pandas_datareader.data as web
from datetime import datetime, timedelta

def get_stock_data(tickers, start_date, end_date):
    """
    Download stock data for given tickers and date range.
    """
    data = yf.download(tickers, start=start_date, end=end_date, interval='1mo')
    adj_close_data = data['Adj Close']
    adj_close_data.index = adj_close_data.index.date
    return adj_close_data

def get_fama_french_factors(start_date, end_date):
    """
    Download Fama-French factors for given date range.
    """
    ff_factors = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start=start_date, end=end_date)[0]
    ff_factors = ff_factors[["Mkt-RF", "SMB", "HML"]]
    ff_factors.index = ff_factors.index.to_timestamp()
    return ff_factors

if __name__ == "__main__":
    # Example usage
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)  # 3 years of data
    
    stock_data = get_stock_data(tickers, start_date, end_date)
    ff_factors = get_fama_french_factors(start_date, end_date)
    
    print(stock_data.head())
    print(ff_factors.head())