def load_weather_to_bronze(postal_code:str = "M2M") -> str:

    import requests, json
    import pandas as pd
    from sqlalchemy import create_engine
    import psycopg2
    import configparser

    config = configparser.ConfigParser()
    config.read("/opt/airflow/scripts/config.ini")

    key = config['WeatherAPI']['key']
    #q = "M2M"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={postal_code}"

    print(f"Receive input postal code = {postal_code}")

    response = requests.get(url=url)
    try:
        status_code = response.status_code
        if status_code != 200:
            raise requests.exceptions.HTTPError(403)
        else:
            weather = json.loads(response.text)
    except requests.exceptions.HTTPError:
        return (f"http response code: {status_code}")

    output = {}

    location_df = pd.json_normalize(weather['location'], sep="_")
    location_df.rename(columns={"name":"location_name", "localtime":"updated_time"}, inplace=True)
    
    output["location_df"] = location_df

    weather_history_df = pd.json_normalize(weather["current"], sep="_")
    weather_history_df = pd.merge(location_df[["lat","lon"]],weather_history_df, how="cross")
    output["weather_history_df"] = weather_history_df

    
    forecast_day = weather["forecast"]["forecastday"][0]
    date = forecast_day['date']
    date_epoch = forecast_day['date_epoch']

    
    daily_forecast_df = pd.json_normalize(forecast_day["day"], sep="_")
    daily_forecast_df["date"] = date
    daily_forecast_df = pd.merge(location_df[["lat", "lon"]], daily_forecast_df, how="cross")
    output["daily_forecast_df"] = daily_forecast_df

    
    astro_df = pd.json_normalize(forecast_day["astro"], sep="_")
    astro_df["date"] = date
    astro_df = pd.merge(location_df[["lat", "lon"]], astro_df, how="cross")
    output["astro_df"] = astro_df

    
    hourly_forecast_df = pd.json_normalize(forecast_day["hour"], sep="_")
    hourly_forecast_df = pd.merge(location_df[["lat", "lon"]], hourly_forecast_df, how="cross")
    output["hourly_forecast_df"] = hourly_forecast_df

    user = "airflow"
    password = "airflow"
    host = "172.18.0.10"
    database = "demo_project"
    schema = "bronze"
    conn = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{database}",
                                pool_recycle=3600, echo=True)

    table_list = []
    for table in output:
        output[table].to_sql(schema=schema, name=table.replace("_df",""), con=conn, if_exists="replace")
        table_list.append(table.replace("_df",""))

    return f"the following table has been loaded to bronze: {', '.join(table_list)}"

