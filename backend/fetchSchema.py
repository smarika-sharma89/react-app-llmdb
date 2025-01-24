import psycopg2

# Retrieve database configuration from environment variables
db_name = "staging_sept_23"
db_user = "postgres"
db_host = "localhost"
db_port = 5432
db_password = ""  # No password

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Function to fetch table and column details
def fetch_table_and_column_details():
    try:
        # Connect to PostgreSQL using the database URL
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Query to get the names of all tables and their columns in the public schema
        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public';
        """)

        # Fetch all table details
        columns = cur.fetchall()

        table_details = {}
        for column in columns:
            table_name, column_name, data_type = column
            if table_name not in table_details:
                table_details[table_name] = []
            table_details[table_name].append({
                "column_name": column_name,
                "data_type": data_type
            })

        # Print table details with columns
        print("Tables and Columns in the database:")
        for table, cols in table_details.items():
            print(f"Table: {table}", flush=True)
            for col in cols:
                print(f"  Column: {col['column_name']}, Data Type: {col['data_type']}")
            print()

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print("Failed to fetch table and column details.")
        print("Error:", e)

# Function to fetch foreign key relationships in batches
def fetch_foreign_key_relationships(batch_size=20):
    try:
        # Connect to PostgreSQL using the database URL
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Start with an initial offset
        offset = 0

        while True:
            # Query to get foreign key relationships with LIMIT and OFFSET for pagination
            cur.execute(f"""
                SELECT 
                    conname AS constraint_name,
                    conrelid::regclass AS table_name,
                    a.attname AS column_name,
                    cl.relname AS referenced_table,
                    af.attname AS referenced_column
                FROM 
                    pg_constraint AS c
                JOIN 
                    pg_attribute AS a ON a.attnum = ANY(c.conkey)
                JOIN 
                    pg_class AS cl ON cl.oid = c.confrelid
                JOIN 
                    pg_attribute AS af ON af.attnum = ANY(c.confkey)
                WHERE 
                    c.contype = 'f'  -- Only foreign keys
                LIMIT {batch_size} OFFSET {offset};
            """)

            # Fetch the current batch of foreign key relationships
            relationships = cur.fetchall()

            # If no relationships are returned, break the loop
            if not relationships:
                break

            # Print the fetched foreign key relationships
            print(f"Foreign Key Relationships (Offset {offset}):")
            for relationship in relationships:
                constraint_name, table_name, column_name, referenced_table, referenced_column = relationship
                print(f"Constraint: {constraint_name}, Table: {table_name}, Column: {column_name} "
                      f"references {referenced_table} ({referenced_column})")

            # Increment the offset for the next batch
            offset += batch_size

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print("Failed to fetch foreign key relationships.")
        print("Error:", e)

# TESTING THE FUNCTION
print("Fetching Foreign Key Relationships in Batches:")
fetch_foreign_key_relationships(batch_size=20)

# TESTING SCHEMA DETAILS
# print("Fetching Table and Column Details----------------")
# fetch_table_and_column_details()
