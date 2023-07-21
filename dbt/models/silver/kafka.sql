{{
    config(
        materialized = 'incremental',
        unique_key = 'id'
    )
}}

select id,
    title,
    score,
    upvote_ratio,
    content,
    url,
    no_of_comments,
    locked,
    to_timestamp(updated) updated
from {{ source('bronze','kafka') }}
{% if is_incremental() %}
  where to_timestamp(updated) > (select max(updated) from {{ this }})
{% endif %}
