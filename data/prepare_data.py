"""
prepare_data.py

This script downloads the three Bangladesh datasets from HuggingFace and
turns each one into its own SQLite database file:

    institutions.db  -> table: institutions
    hospitals.db     -> table: hospitals
    restaurants.db   -> table: restaurants

Run this ONCE, before starting the agent, and make sure you have an
internet connection (it needs to reach huggingface.co):

    python data/prepare_data.py
"""

import os
import re
import sqlite3

from datasets import load_dataset

# The folder this script lives in (bd-multi-tool-agent/data/).
# We'll save the .db files here, right next to this script.
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Each entry is: (HuggingFace dataset repo id, output .db filename, table name)
DATASETS = [
    ("Mahadih534/Institutional-Information-of-Bangladesh", "institutions.db", "institutions"),
    ("Mahadih534/all-bangladeshi-hospitals", "hospitals.db", "hospitals"),
    ("Mahadih534/Bangladeshi-Restaurant-Data", "restaurants.db", "restaurants"),
]


def clean_column_name(column_name):
    """
    Turn a raw CSV header into a clean, SQL-friendly name.

    Example: "Hospital Name!" -> "hospital_name"
    """
    column_name = column_name.strip().lower()
    # Replace anything that isn't a lowercase letter or number with "_"
    column_name = re.sub(r"[^a-z0-9]+", "_", column_name)
    column_name = column_name.strip("_")
    return column_name or "column"


def build_database(repo_id, db_filename, table_name):
    """Download one dataset from HuggingFace and save it as a SQLite table."""

    # Step 1: download the dataset. load_dataset() handles finding and
    # downloading the right files for us - we just give it the repo id.
    print(f"\n[1/3] Downloading '{repo_id}' from HuggingFace...")
    dataset = load_dataset(repo_id, split="train")

    # Step 2: convert it to a pandas DataFrame (a table we can work with
    # easily) and clean up the column names.
    print("[2/3] Cleaning column names...")
    df = dataset.to_pandas()
    df.columns = [clean_column_name(col) for col in df.columns]
    print(f"      {len(df)} rows, columns: {list(df.columns)}")

    # Step 3: write the DataFrame into a SQLite database file.
    # pandas automatically picks sensible SQLite column types for us:
    #   whole numbers -> INTEGER, decimal numbers -> REAL, text -> TEXT
    db_path = os.path.join(DATA_DIR, db_filename)
    print(f"[3/3] Writing to '{db_path}' (table: {table_name})...")
    connection = sqlite3.connect(db_path)
    df.to_sql(table_name, connection, if_exists="replace", index=False)
    connection.close()

    print(f"Done: {db_filename} created.")


def main():
    for repo_id, db_filename, table_name in DATASETS:
        build_database(repo_id, db_filename, table_name)
    print("\nAll 3 databases were created successfully in the data/ folder.")


if __name__ == "__main__":
    main()
