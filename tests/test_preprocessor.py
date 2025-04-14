import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.preprocessor import preprocess

# 🔧 Minimal dummy data
@pytest.fixture
def dummy_data():
    df = pd.DataFrame({
        'Name': ['Anvai', 'Anvai', 'Bolt'],
        'Sex': ['M', 'M', 'M'],
        'Age': [24, 24, 27],
        'Season': ['Summer', 'Winter', 'Summer'],
        'NOC': ['IND', 'IND', 'USA'],
        'Medal': ['Gold', 'Silver', 'Bronze']
    })

    regions = pd.DataFrame({
        'NOC': ['IND', 'USA'],
        'region': ['India', 'USA']
    })

    return df, regions

def test_preprocessing_filters(dummy_data):
    df, regions = dummy_data
    result = preprocess(df, regions)

    # Should only keep Summer rows
    assert all(result['Season'] == 'Summer')

    # Merge should succeed (Winter row dropped)
    assert 'region' in result.columns
    assert result.shape[0] == 2

    # One-hot columns created
    assert 'Gold' in result.columns
    assert 'Silver' in result.columns
    assert 'Bronze' in result.columns
