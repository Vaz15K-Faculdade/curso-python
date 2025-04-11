import sqlite3
import duckdb

# Connect to SQLite database
sqlite_connection = sqlite3.connect("banco_sql_python.db")
sqlite_cursor = sqlite_connection.cursor()

# Connect to DuckDB
duck_connection = duckdb.connect("banco_duck.db")

# Get all tables from SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Transfer each table to DuckDB
for table in tables:
    table_name = table[0]
    print(f"Transferring table: {table_name}")
    
    # Get table data and column names from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    # Get column names
    columns = [description[0] for description in sqlite_cursor.description]
    
    if rows:
        # Create table in DuckDB
        columns_def = ", ".join([f'"{col}" VARCHAR' for col in columns])
        duck_connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
        
        # Insert data into DuckDB
        placeholders = ", ".join(["?" for _ in columns])
        for row in rows:
            duck_connection.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

print("Data transfer from SQLite to DuckDB completed successfully!")

# Close connections
sqlite_connection.close()
duck_connection.close()