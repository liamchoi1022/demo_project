{{
    config(
        materialized = 'incremental',
        unique_key = 'id'
    )
}}

select 
    {{ gen_key(['lat', 'lon']) }} id,
    location_name::varchar(100) location_name,
    region::varchar(100) region,
    country::varchar(100) country,
    lat::decimal(5,2) latitude ,
    lon::decimal(5,2) longitude,
    tz_id::varchar(50) timezone,
    localtime_epoch::integer localtime_epoch,
    updated_time::timestamp local_time
from {{ source('bronze','location') }}
