import os
import re
import sqlite3

from datasets import load_dataset

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

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
    column_name = re.sub(r"[^a-z0-9]+", "_", column_name)
    column_name = column_name.strip("_")
    return column_name or "column"


def build_database(repo_id, db_filename, table_name):
    """Download one dataset from HuggingFace and save it as a SQLite table."""

    print(f"\n[1/3] Downloading '{repo_id}' from HuggingFace...")
    dataset = load_dataset(repo_id, split="train")

    print("[2/3] Cleaning column names...")
    df = dataset.to_pandas()
    df.columns = [clean_column_name(col) for col in df.columns]
    print(f"      {len(df)} rows, columns: {list(df.columns)}")

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
