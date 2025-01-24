import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve database configuration from environment variables
db_name = "staging_sept_23"
db_user = "postgres"
db_host = "localhost"
db_port = 5432
db_password = ""  # No password

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Query to fetch actual data from the production_tracking_attachment table
cur.execute("SELECT * FROM core_client LIMIT 2;")  # Example: Fetch 5 rows
rows = cur.fetchall()

# Print the fetched rows
for row in rows:
    print(row)

# Close the connection
cur.close()
conn.close()
