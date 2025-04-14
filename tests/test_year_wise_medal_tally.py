import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.helper import year_wise_medal_tally

# 🧪 Create dummy data
@pytest.fixture
def dummy_data():
    return pd.DataFrame({
        'Team': ['India', 'India', 'USA'],
        'NOC': ['IND', 'IND', 'USA'],
        'Year': [2012, 2016, 2016],
        'City': ['London', 'Rio', 'Rio'],
        'Sport': ['Wrestling', 'Shooting', 'Swimming'],
        'Event': ['66kg', '10m Air Rifle', '100m Freestyle'],
        'region': ['India', 'India', 'USA'],
        'Medal': ['Silver', 'Gold', 'Bronze']
    })

def test_year_medals_india(dummy_data):
    df = dummy_data
    result = year_wise_medal_tally(df, country="India")
    assert not result.empty
    assert result.shape[0] == 2  # India has medals in 2 different years
    assert 2012 in result["Year"].values
    assert 2016 in result["Year"].values

def test_year_medals_usa(dummy_data):
    df = dummy_data
    result = year_wise_medal_tally(df, country="USA")
    assert result.shape[0] == 1
    assert result["Medal"].iloc[0] == 1
