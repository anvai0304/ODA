import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.helper import men_vs_women

@pytest.fixture
def gender_data():
    return pd.DataFrame({
        'Name': ['A', 'B', 'C', 'D'],
        'Sex': ['M', 'F', 'M', 'F'],
        'Year': [2000, 2000, 2004, 2004],
        'region': ['IND', 'IND', 'USA', 'USA']
    })

def test_gender_distribution(gender_data):
    result = men_vs_women(gender_data)

    assert 'Male' in result.columns
    assert 'Female' in result.columns
    assert result['Male'].iloc[0] == 1
    assert result['Female'].iloc[0] == 1
