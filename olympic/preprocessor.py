import pandas as pd

# Logging
from utils.logger_config import get_logger

logger = get_logger('preprocessor')

# Function for data processing
def preprocess(df, regions_df):

    logger.info('Preprocessing started')
    logger.debug(f'Initial rows: {len(df)}')

    # Summer Olympics
    df = df[df['Season'] == 'Summer']
    logger.debug(f'Rows after season filter: {len(df)}')

    # Merge with region dataset
    df = df.merge(regions_df, on='NOC', how='inner')
    logger.debug(f'Rows after merging with region data: {len(df)}')

    # Drop duplicates
    df = df.drop_duplicates()
    logger.info('Duplicates dropped')

    # One Hot Encoding for medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    logger.info('Applied one-hot encoding on medals')
    
    return df