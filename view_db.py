import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('accounts.db')

# Create a cursor object
cur = conn.cursor()

# Execute a query (replace 'your_table_name' with your actual table name)
cur.execute("SELECT * FROM accounts")

# Fetch all results from the query
rows = cur.fetchall()

# Get column names from the cursor description
column_names = [description[0] for description in cur.description]

# Convert the result to a list of dictionaries (key: column name, value: row data)
result = [dict(zip(column_names, row)) for row in rows]

# Convert the list of dictionaries to JSON
json_result = json.dumps(result, indent=4)

# Print the JSON result
print(json_result)

# Close the cursor and connection
cur.close()
conn.close()