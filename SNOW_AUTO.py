import snowflake.connector
import csv
import tkinter as tk

# Create a function to execute the Snowflake query and generate the CSV file
def generate_csv():
    # Get the user input values
    username = username_entry.get()
    password = password_entry.get()
    account = account_entry.get()
    warehouse = warehouse_entry.get()
    database = database_entry.get()
    schema = schema_entry.get()
    table_name = table_name_entry.get()



    # Set up the Snowflake connection
    conn = snowflake.connector.connect(
        user='Rishabh',
        password='Rish@bh1256',
        account='ba38717.eu-west-2.aws',
        warehouse='PYTHON',
        database='PYTHON',
        schema='PY_TEST'
    )

    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT query on the Snowflake table
    cur.execute(f'SELECT * FROM employees')

    # Retrieve the query results
    rows = cur.fetchall()

    # Get the column names from the cursor description
    col_names = [desc[0] for desc in cur.description]

    # Write the query results to a CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the column names as the first row
        writer.writerow(col_names)

        # Write the query results
        writer.writerows(rows)

    # Close the Snowflake connection
    cur.close()
    conn.close()

# Create a new Tkinter window
window = tk.Tk()
window.title('Snowflake Query to CSV')

# Create labels and text boxes for user input
tk.Label(window, text='Username').grid(row=0, column=0)
username_entry = tk.Entry(window)
username_entry.grid(row=0, column=1)

tk.Label(window, text='Password').grid(row=1, column=0)
password_entry = tk.Entry(window, show='*')
password_entry.grid(row=1, column=1)

tk.Label(window, text='Account Name').grid(row=2, column=0)
account_entry = tk.Entry(window)
account_entry.grid(row=2, column=1)

tk.Label(window, text='Warehouse Name').grid(row=3, column=0)
warehouse_entry = tk.Entry(window)
warehouse_entry.grid(row=3, column=1)

tk.Label(window, text='Database Name').grid(row=4, column=0)
database_entry = tk.Entry(window)
database_entry.grid(row=4, column=1)

tk.Label(window, text='Schema Name').grid(row=5, column=0)
schema_entry = tk.Entry(window)
schema_entry.grid(row=5, column=1)

tk.Label(window, text='Table Name').grid(row=6, column=0)
table_name_entry = tk.Entry(window)
table_name_entry.grid(row=6, column=1)

# Create a button to execute the query and generate the CSV file
tk.Button(window, text='Generate CSV', command=generate_csv).grid(row=7, column=1)

# Run the Tkinter event loop
window.mainloop()
