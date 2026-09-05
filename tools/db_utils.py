import os
import sqlite3

THIS_FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDER = os.path.dirname(THIS_FILE_FOLDER)
DATA_DIR = os.path.join(PROJECT_FOLDER, "data")


def run_query(db_filename, sql_query, max_rows=20):
    """
    Run a SQL query against a SQLite database and return the result as text.

    db_filename: e.g. "hospitals.db"
    sql_query:   a SQL SELECT statement, e.g. "SELECT * FROM hospitals LIMIT 5;"
    max_rows:    how many rows to include in the answer (keeps answers short)
    """
    db_path = os.path.join(DATA_DIR, db_filename)

    if not os.path.exists(db_path):
        return (
            f"Database '{db_filename}' was not found. "
            "Run `python data/prepare_data.py` first to build it."
        )

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        if cursor.description:
            column_names = [column[0] for column in cursor.description]
        else:
            column_names = []

        connection.close()
    except sqlite3.Error as error:
        return f"SQL error: {error}. Please check the query and column names."

    if not rows:
        return "No matching results were found."

    was_truncated = len(rows) > max_rows
    rows = rows[:max_rows]

    lines = [", ".join(column_names)]
    for row in rows:
        row_as_text = [str(value) for value in row]
        lines.append(", ".join(row_as_text))

    result_text = "\n".join(lines)
    if was_truncated:
        result_text += f"\n... (showing first {max_rows} rows only)"

    return result_text
