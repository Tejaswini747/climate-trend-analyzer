import pandas as pd

def clean_data(df):
    df = df.copy()

    # Convert date
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort values
    df = df.sort_values('Date')

    # Fill missing values
    df = df.fillna(method='ffill')

    return df