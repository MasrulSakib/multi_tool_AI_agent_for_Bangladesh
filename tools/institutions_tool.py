from langchain_core.tools import tool

from .db_utils import run_query

DB_FILENAME = "institutions.db"
TABLE_NAME = "institutions"


@tool
def institutions_db_tool(sql_query: str) -> str:
    """Use this tool to answer questions about Bangladeshi universities,
    colleges, madrasahs, and government educational institutions -
    for example counts, lists, or details by district, division, or
    institution type.

    Input must be a single valid SQLite SELECT query against the
    'institutions' table. If you don't know the exact column names yet,
    first run: SELECT * FROM institutions LIMIT 1;

    Returns the query result as plain text, one row per line.
    """
    return run_query(DB_FILENAME, sql_query)
