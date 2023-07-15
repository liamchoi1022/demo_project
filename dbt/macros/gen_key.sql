{% macro gen_key(column_list) -%}

    cast({{ dbt_utils.generate_surrogate_key(column_list) }} as varchar(32))

{%- endmacro %}