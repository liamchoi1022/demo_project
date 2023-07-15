import sys

sys.path.append("/Users/liamchoi/Desktop/demo_project/scripts/src")

import requests, json
import pandas as pd
#from sqlalchemy import create_engine
#import psycopg2

#import call_weather_api
from call_weather_api import *
from requests.exceptions import HTTPError

def test_call_weather_api():

    #test key error
    key = "123"
    location = "M2M"

    try:
        result = extract_from_api(key,location)
    except Exception as e:
        assert e.args[0] == "403"

    #test output format
    key = "4b711529dbd04dc595351103231207"
    weather = extract_from_api(key,location)
    assert type(weather) == dict
    
    output = transform(weather)

    assert len(output) == 5
    assert list(output.keys()) == ["location_df", "weather_history_df", "daily_forecast_df", "astro_df", "hourly_forecast_df"]
