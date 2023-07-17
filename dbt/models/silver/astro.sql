{{
    config(
        materialized = 'incremental',
        unique_key = 'id'
    )
}}

select 
    {{ gen_key(['lat', 'lon', 'date']) }} id,
    lat::decimal(5,2) latitude ,
    lon::decimal(5,2) longitude,
    sunrise::time sunrise,
    sunset::time sunset,
    moonrise::time moonrise,
    moonset::time moonset,
    moon_phase::varchar(100) moon_phase,
    moon_illumination::smallint moon_illumination,
    is_moon_up::int::boolean is_moon_up,
    is_sun_up::int::boolean is_sun_up,
    date::date date
from {{ source('bronze','astro') }}
