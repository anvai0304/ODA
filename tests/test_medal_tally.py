import sys
import os

# Adding project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import pytest
from olympic.helper import fetch_medal_tally

# 👇 Create dummy Olympic dataset
@pytest.fixture
def dummy_df():
    return pd.DataFrame({
        'Team': ['India', 'India', 'USA'],
        'NOC': ['IND', 'IND', 'USA'],
        'Games': ['2008 Summer', '2012 Summer', '2012 Summer'],
        'Year': [2008, 2012, 2012],
        'City': ['Beijing', 'London', 'London'],
        'Sport': ['Shooting', 'Wrestling', 'Swimming'],
        'Event': ['10m Air Rifle', 'Wrestling 66kg', '100m Freestyle'],
        'Medal': ['Gold', 'Silver', 'Bronze'],
        'region': ['India', 'India', 'USA'],
        'Gold': [1, 0, 0],
        'Silver': [0, 1, 0],
        'Bronze': [0, 0, 1]
    })

# ✅ Test for country = India and year = 2012
def test_india_2012(dummy_df):
    result = fetch_medal_tally(dummy_df, year=2012, country="India")
    assert not result.empty
    assert result["Silver"].iloc[0] == 1
    assert result["Gold"].iloc[0] == 0

# ✅ Test for year = 2012 and country = Overall
def test_overall_2012(dummy_df):
    result = fetch_medal_tally(dummy_df, year=2012, country="Overall")
    assert "India" in result["region"].values
    assert "USA" in result["region"].values

# ✅ Test for country = Overall and year = Overall
def test_overall_overall(dummy_df):
    result = fetch_medal_tally(dummy_df, year="Overall", country="Overall")
    assert "India" in result["region"].values
    assert "USA" in result["region"].values
