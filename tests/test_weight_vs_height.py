import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from olympic.helper import weight_vs_height

@pytest.fixture
def athlete_data():
    return pd.DataFrame({
        'Name': ['Anvai', 'Bolt', 'Simone'],
        'region': ['India', 'Jamaica', 'USA'],
        'Sport': ['Wrestling', 'Athletics', 'Gymnastics'],
        'Height': [170, 195, 150],
        'Weight': [70, 85, 50],
        'Medal': [None, 'Gold', 'Bronze']
    })

def test_overall_filtering(athlete_data):
    result = weight_vs_height(athlete_data, sport='Overall')

    # Should include all athletes
    assert result.shape[0] == 3
    assert 'No Medal' in result['Medal'].values

def test_specific_sport_filtering(athlete_data):
    result = weight_vs_height(athlete_data, sport='Athletics')

    assert result.shape[0] == 1
    assert result.iloc[0]['Name'] == 'Bolt'
    assert result.iloc[0]['Sport'] == 'Athletics'
