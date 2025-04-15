import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.helper import country_medal_sport

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Team': ['India', 'India', 'India', 'USA'],
        'NOC': ['IND', 'IND', 'IND', 'USA'],
        'Year': [2008, 2012, 2012, 2012],
        'Sport': ['Shooting', 'Wrestling', 'Shooting', 'Athletics'],
        'Event': ['Event1', 'Event2', 'Event3', 'Event4'],
        'City': ['Beijing', 'London', 'London', 'London'],
        'Medal': ['Gold', 'Bronze', 'Silver', 'Gold'],
        'region': ['India', 'India', 'India', 'USA']
    })

def test_country_pivot_structure(sample_data):
    # This will test if pivot is created without error
    try:
        country_medal_sport(sample_data, country='India')
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
