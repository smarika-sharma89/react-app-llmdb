from sqlalchemy import create_engine, MetaData

# Retrieve database configuration from environment variables
db_name = "staging_sept_23"
db_user = "postgres"
db_host = "localhost"
db_port = 5432
db_password = ""  # No password

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Connect to your PostgreSQL database
engine = create_engine(db_url)
metadata = MetaData()
metadata.reflect(bind=engine)


# Extract schema details with foreign key relationships
tables = {}
for table_name, table in metadata.tables.items():
    # Initialize the structure for each table
    tables[table_name] = {
        "columns": [col.name for col in table.columns],
        "relationships": [],  # This will hold the foreign key relationships
    }

    # Process foreign key constraints
    for col in table.columns:
        for fk in col.foreign_keys:
            tables[table_name]["relationships"].append(
                {
                    "column": col.name,
                    "referred_table": fk.column.table.name,
                    "referred_column": fk.column.name,
                }
            )

# print(tables)
# pretty print the output in json

import json

json_format= json.dumps(tables, indent=4)
# print(json_format)


# Print schema details with relationships
for table, details in tables.items():
    print(f"Table: {table}")
    print("Columns:", details["columns"])
    print("Relationships:")
    for relationship in details["relationships"]:
        print(
            f"  - {relationship['column']} references {relationship['referred_table']}({relationship['referred_column']})"
        )
    print()


descriptions = []
for table_name, details in tables.items():
    description = f"Table {table_name} with columns {', '.join(details['columns'])}."
    descriptions.append(description)

    for relationship in details["relationships"]:
        description = f"Column {relationship['column']} references {relationship['referred_table']}({relationship['referred_column']})."
        descriptions.append(description)

# print("\n".join(descriptions))

import openai

openai.api_key = "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"

embeddings = []

for description in descriptions:
    response = openai.Embedding.create(
        input=description, model="text-embedding-3-small"
    )
    embeddings.append(response["data"][0]["embedding"])

# Store embeddings for each description
embeddings = []

# Generate embeddings
for description in descriptions:
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",  # Confirm model name
            input=[description],  # Ensure input is in list format
        )
        # Append embedding from the response
        embeddings.append(response["data"][0]["embedding"])
    except Exception as e:
        print(f"Error processing description '{description}': {e}")

print(embeddings)





