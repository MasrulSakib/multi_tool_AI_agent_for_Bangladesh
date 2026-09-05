"""
hospitals_tool.py

Same idea as institutions_tool.py, but this tool answers questions about
the 'hospitals' table instead (facility type, agency, location, etc).
See institutions_tool.py for a full explanation of how @tool works.
"""

from langchain_core.tools import tool

from .db_utils import run_query

DB_FILENAME = "hospitals.db"
TABLE_NAME = "hospitals"


@tool
def hospitals_db_tool(sql_query: str) -> str:
    """Use this tool to answer questions about Bangladeshi hospitals,
    clinics, and health facilities - for example counts, lists, or
    details by district, division, facility type, or managing agency.

    Input must be a single valid SQLite SELECT query against the
    'hospitals' table. If you don't know the exact column names yet,
    first run: SELECT * FROM hospitals LIMIT 1;

    Returns the query result as plain text, one row per line.
    """
    return run_query(DB_FILENAME, sql_query)
