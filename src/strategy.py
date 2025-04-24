import numpy as np
import pandas as pd
import statsmodels.api as sm

def fit_ff_models(returns_df, ff_data, stocks):
    # Add a constant to the Fama-French factors for the regression
    ff_factors = sm.add_constant(ff_data[["Mkt-RF", "SMB", "HML"]])

    # Initialize a dictionary to store the regression models for each stock
    ff_models = {}

    # Iterate over each stock and perform the Fama-French regression
    for stock in stocks:
        # Create a DataFrame for the regression with the stock returns and Fama-French factors
        df = pd.DataFrame(
            {
                "Return": returns_df[stock],
                "alpha": ff_factors["const"],
                "Mkt-RF": ff_factors["Mkt-RF"],
                "SMB": ff_factors["SMB"],
                "HML": ff_factors["HML"],
            }
        )
        # Drop rows with missing values (mainly affects the first row due to lag in monthly returns calculation)
        df = df.dropna()
        # Perform ordinary least squares (OLS) regression and store the model in the dictionary
        ff_models[stock] = sm.OLS(
            df["Return"], df[["alpha", "Mkt-RF", "SMB", "HML"]]
        ).fit()

    return ff_models

def calculate_residuals(returns_df, ff_models, ff_factors, stocks):
    """
    Calculate the residuals of the Fama-French regression for the given stocks.
    """
    # Select the last 12 months of return and factor data
    last_returns = returns_df.iloc[-12:, :]
    last_factors = ff_factors.iloc[-12:, :]

    # Create a DataFrame to store the residuals
    residual_df = pd.DataFrame(index=last_returns.index)

    # Initialize a list to store the residual columns
    residual_columns = []

    # Iterate over the available stocks and calculate residuals from the Fama-French regression
    for stock in stocks:
        # Get the Fama-French regression coefficients for the stock
        coef = ff_models[stock].params
        # Calculate the residuals
        residuals = (
            last_returns[stock]
            - coef["Mkt-RF"] * last_factors["Mkt-RF"]
            - coef["SMB"] * last_factors["SMB"]
            - coef["HML"] * last_factors["HML"]
        )
        residual_columns.append(residuals)

    residual_df = pd.concat(residual_columns, axis=1)
    residual_df.columns = stocks

    # Return the DataFrame with residuals from the Fama-French regression
    return residual_df

def calculate_adjusted_residuals(residual_df):
    # Calculate risk-adjusted residuals for the available stocks and sort them from lowest to highest
    risk_adjusted_residuals = (residual_df.mean() / residual_df.var()).sort_values()
    return risk_adjusted_residuals

def create_portfolio(risk_adjusted_residuals, top_pct=10, bottom_pct=10):
    """
    Create a long-short portfolio based on momentum scores.
    """
    # Filter the risk-adjusted residuals above the (100 - top_pct) percentile
    buy = risk_adjusted_residuals[
        risk_adjusted_residuals > np.percentile(risk_adjusted_residuals, 100 - top_pct)
    ]

    # Filter the risk-adjusted residuals below the bottom_pct percentile
    sell = risk_adjusted_residuals[
        risk_adjusted_residuals < np.percentile(risk_adjusted_residuals, bottom_pct)
    ]

    return buy, sell