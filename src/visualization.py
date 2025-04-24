import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_prices(stocks, prices):
    """
    Plot the adjusted closing prices of some stocks.
    """
    plt.figure(figsize=(12, 6))
    for stock in stocks:
        plt.plot(prices.index, prices[stock], label=stock)

    plt.xlabel('Date')
    plt.ylabel('Monthly Adjusted Closing Price')
    plt.title('Monthly Adjusted Closing Price of Selected Stocks')
    plt.legend()
    plt.show()

def plot_adjusted_residuals(risk_adjusted_residuals):
    # Calculate the 10th and 90th percentiles
    decile_1 = np.percentile(risk_adjusted_residuals, 10)
    decile_9 = np.percentile(risk_adjusted_residuals, 90)

    # Histogram of risk-adjusted residuals
    plt.figure(figsize=(8, 6))
    sns.histplot(risk_adjusted_residuals, bins=20, kde=True)
    plt.xlabel('Risk-Adjusted Residuals')
    plt.ylabel('Frequency')
    plt.title('Histogram of Risk-Adjusted Residuals')

    # Add vertical lines for the 10th and 90th percentiles
    plt.axvline(decile_1, color='red', linestyle='--', label='10th Percentile')
    plt.axvline(decile_9, color='blue', linestyle='--', label='90th Percentile')
    plt.legend()

    plt.show()