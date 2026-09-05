"""
institutions_tool.py

In LangChain, the @tool decorator turns a normal Python function into
something an Agent can call. The docstring below is what the agent
reads to decide WHEN to use this tool - it must be descriptive.

This tool answers questions about the 'institutions' table, which holds
Bangladeshi universities, colleges, and government institutions.
"""

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
    # All the real work (running SQL + formatting the result) lives in
    # db_utils.run_query(), so this function just passes the query along.
    return run_query(DB_FILENAME, sql_query)
