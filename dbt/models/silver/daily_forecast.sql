{{
    config(
        materialized = 'incremental',
        unique_key = 'id'
    )
}}

select
    {{ gen_key(['lat', 'lon', 'date']) }} id,
    lat::decimal(5,2) latitude,
    lon::decimal(5,2) longitude,
    maxtemp_c::decimal(3,1) max_temp_c,
    maxtemp_f::decimal(3,1) max_temp_f,
    mintemp_c::decimal(3,1) min_temp_c,
    mintemp_f::decimal(3,1) min_temp_f,
    avgtemp_c::decimal(3,1) avg_temp_c,
    avgtemp_f::decimal(3,1) avg_temp_f,
    maxwind_mph::decimal(4,1) max_wind_mph,
    maxwind_kph::decimal(4,1) max_wind_kph,
    totalprecip_mm::decimal(4,1) total_precipitation_mm,
    totalprecip_in::decimal(3,1) total_precipitation_in,
    totalsnow_cm::decimal(4,1) total_snow_cm,
    avgvis_km::decimal(3,1) avg_visibility_km,
    avgvis_miles::decimal(3,1) avg_visibility_miles,
    avghumidity::decimal(4,1) avg_humidity,
    daily_will_it_rain::int::boolean daily_will_it_rain,
    daily_chance_of_rain::smallint daily_chance_of_rain,
    daily_will_it_snow::int::boolean daily_will_it_snow,
    daily_chance_of_snow::smallint daily_chance_of_snow,
    uv::decimal(3,1) uv_index,
    condition_text::varchar(100) weather_condition,
    condition_icon::text weather_condition_icon_url,
    condition_code::smallint weather_condition_code,
    date::date date
from {{ source('bronze', 'daily_forecast') }}