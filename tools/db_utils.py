"""
db_utils.py

This is a small "helper" file used by all three database tools
(institutions_tool.py, hospitals_tool.py, restaurants_tool.py).

It has ONE job: take a SQL query, run it against a SQLite database file,
and turn the result into a simple text string that the AI agent can read.

Why share this code instead of copying it into each tool file?
Because all three tools do the exact same thing (run SQL -> format text),
just against a different .db file. Writing it once here means we only
have to fix bugs in one place.
"""

import os
import sqlite3

# Folder that contains the .db files: bd-multi-tool-agent/data/
# __file__ is the path to this file (tools/db_utils.py). We go up one
# folder (out of tools/) and then into data/.
THIS_FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))   # .../tools
PROJECT_FOLDER = os.path.dirname(THIS_FILE_FOLDER)              # .../bd-multi-tool-agent
DATA_DIR = os.path.join(PROJECT_FOLDER, "data")


def run_query(db_filename, sql_query, max_rows=20):
    """
    Run a SQL query against a SQLite database and return the result as text.

    db_filename: e.g. "hospitals.db"
    sql_query:   a SQL SELECT statement, e.g. "SELECT * FROM hospitals LIMIT 5;"
    max_rows:    how many rows to include in the answer (keeps answers short)
    """
    db_path = os.path.join(DATA_DIR, db_filename)

    # Step 1: make sure the database file actually exists
    if not os.path.exists(db_path):
        return (
            f"Database '{db_filename}' was not found. "
            "Run `python data/prepare_data.py` first to build it."
        )

    # Step 2: try running the SQL query
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # cursor.description holds the column names, but only for queries
        # that return columns (like SELECT). If it's empty, there are no
        # column names to show.
        if cursor.description:
            column_names = [column[0] for column in cursor.description]
        else:
            column_names = []

        connection.close()
    except sqlite3.Error as error:
        return f"SQL error: {error}. Please check the query and column names."

    # Step 3: handle an empty result
    if not rows:
        return "No matching results were found."

    # Step 4: keep only the first `max_rows` rows so the answer stays short
    was_truncated = len(rows) > max_rows
    rows = rows[:max_rows]

    # Step 5: turn the rows into a simple, readable text table
    lines = [", ".join(column_names)]
    for row in rows:
        row_as_text = [str(value) for value in row]
        lines.append(", ".join(row_as_text))

    result_text = "\n".join(lines)
    if was_truncated:
        result_text += f"\n... (showing first {max_rows} rows only)"

    return result_text
