{{
    config(
        materialized = 'incremental',
        unique_key = 'id'
    )
}}


select
    {{ gen_key(['lat', 'lon', 'last_updated_epoch']) }} id,
    lat::decimal(5,2) latitude,
    lon::decimal(5,2) longitude,
    last_updated_epoch::int last_updated_epoch,
    last_updated::timestamp last_updated,
    temp_c::decimal(3,1) temp_c,
    temp_f::decimal(3,1) temp_f,
    is_day::int::boolean is_day,
    wind_mph::decimal(4,1) wind_mph,
    wind_kph::decimal(4,1) wind_kph,
    wind_degree::smallint wind_degree,
    wind_dir::varchar(3) wind_dir,
    pressure_mb::decimal(6,1) pressure_mb,
    pressure_in::decimal(5,2) pressure_in,
    precip_mm::decimal(5,1) precipitation_mm,
    precip_in::decimal(3,1) precipitation_in,
    humidity::smallint humidity,
    cloud::smallint cloud_cover_percent,
    feelslike_c::decimal(3,1) feels_like_c,
    feelslike_f::decimal(4,1) feels_like_f,
    vis_km::decimal(3,1) visibility_km,
    vis_miles::decimal(3,1) visibility_miles,
    uv::decimal(3,1) uv_index,
    gust_mph::decimal(4,1) gust_mph,
    gust_kph::decimal(4,1) gust_kph,
    condition_text::varchar(100) weather_condition,
    condition_icon weather_condition_icon_url,
    condition_code::smallint weather_condition_code
from {{ source('bronze', 'weather_history') }}