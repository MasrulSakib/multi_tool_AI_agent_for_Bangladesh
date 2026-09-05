"""
restaurants_tool.py

Same idea as institutions_tool.py, but this tool answers questions about
the 'restaurants' table instead (name, rating, address, location, etc).
See institutions_tool.py for a full explanation of how @tool works.
"""

from langchain_core.tools import tool

from .db_utils import run_query

DB_FILENAME = "restaurants.db"
TABLE_NAME = "restaurants"


@tool
def restaurants_db_tool(sql_query: str) -> str:
    """Use this tool to answer questions about Bangladeshi restaurants -
    for example lists or details by name, address/area, or rating.

    Input must be a single valid SQLite SELECT query against the
    'restaurants' table. If you don't know the exact column names yet,
    first run: SELECT * FROM restaurants LIMIT 1;

    Returns the query result as plain text, one row per line.
    """
    return run_query(DB_FILENAME, sql_query)
