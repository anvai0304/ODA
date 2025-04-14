import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.helper import most_successful

#  Fixture with medals in multiple sports
@pytest.fixture
def dummy_athlete_data():
    return pd.DataFrame({
        'Name': ['Anvai', 'Anvai', 'Bolt', 'Bolt', 'Bolt'],
        'Sport': ['Wrestling', 'Wrestling', 'Athletics', 'Athletics', 'Athletics'],
        'region': ['India', 'India', 'Jamaica', 'Jamaica', 'Jamaica'],
        'Medal': ['Gold', 'Silver', 'Gold', 'Silver', 'Bronze']
    })

#  Test for Overall
def test_most_successful_overall(dummy_athlete_data):
    result = most_successful(dummy_athlete_data, 'Overall')
    assert not result.empty
    assert 'Anvai' in result['Name'].values
    assert 'Bolt' in result['Name'].values

#  Test for specific sport
def test_most_successful_athletics_only(dummy_athlete_data):
    result = most_successful(dummy_athlete_data, 'Athletics')
    assert not result.empty
    assert all(result['Sport'] == 'Athletics')
    assert 'Bolt' in result['Name'].values
