import teradata

# Set up Teradata connection
udaExec = teradata.UdaExec(appName="Teradata to Snowflake", version="1.0", logConsole=False)
session = udaExec.connect(method="odbc", system="Teradata_Server", username="Teradata_User", password="Teradata_Password")

# Get table structure from Teradata
table_name = "your_teradata_table"
table_structure_query = f"SHOW TABLE {table_name};"
table_structure_result = session.execute(table_structure_query)

# Generate Snowflake table structure query
snowflake_table_name = "your_snowflake_table"
snowflake_table_query = f"CREATE TABLE {snowflake_table_name} (\n"
for row in table_structure_result.fetchall():
    column_name = row[0]
    data_type = row[1]
    snowflake_data_type = ""
    if "INTEGER" in data_type or "BIGINT" in data_type:
        snowflake_data_type = "NUMBER"
    elif "DECIMAL" in data_type or "NUMERIC" in data_type:
        precision = data_type.split("(")[1].split(",")[0]
        scale = data_type.split(",")[1].split(")")[0]
        snowflake_data_type = f"NUMBER({precision},{scale})"
    elif "VARCHAR" in data_type or "CHAR" in data_type:
        size = data_type.split("(")[1].split(")")[0]
        snowflake_data_type = f"VARCHAR({size})"
    elif "DATE" in data_type or "TIMESTAMP" in data_type:
        snowflake_data_type = data_type
    elif "BYTEINT" in data_type:
        snowflake_data_type = "TINYINT"
    elif "SMALLINT" in data_type:
        snowflake_data_type = "SMALLINT"
    elif "FLOAT" in data_type:
        snowflake_data_type = "FLOAT"
    elif "DOUBLE" in data_type:
        snowflake_data_type = "DOUBLE"
    elif "BOOLEAN" in data_type:
        snowflake_data_type = "BOOLEAN"
    elif "BLOB" in data_type:
        snowflake_data_type = "BINARY"
    # Add additional conditions for other data types as needed
    
    if snowflake_data_type:
        snowflake_table_query += f"{column_name} {snowflake_data_type},\n"
snowflake_table_query = snowflake_table_query[:-2]  # Remove trailing comma and newline
snowflake_table_query += ");"

# Write Snowflake table structure query to file
with open("snowflake_table_structure.sql", "w") as f:
    f.write(snowflake_table_query)

print("Snowflake table structure query generated and written to file 'snowflake_table_structure.sql'")