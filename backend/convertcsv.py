import pandas as pd
import sqlite3

def csv_to_sqlite(csv_file, db_file, table_name):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table from the DataFrame
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database {db_file} created successfully with table {table_name}.")

if __name__ == "__main__":
    csv_file = 'IMDB Dataset.csv'  # Replace with your CSV file path
    db_file = 'database.db'  # Replace with your desired database file name
    table_name = 'imdb_reviews'  # Replace with your desired table name

    csv_to_sqlite(csv_file, db_file, table_name)
