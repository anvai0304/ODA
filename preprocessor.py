import pandas as pd


# Function for data processing
def preprocess(df, regions_df):

    # Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region dataset
    df = df.merge(regions_df, on='NOC', how='inner')

    # Drop duplicates
    df = df.drop_duplicates()

    # One Hot Encoding for medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    
    return df