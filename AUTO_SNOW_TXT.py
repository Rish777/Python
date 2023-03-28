import json
import snowflake.connector
import csv
import tkinter as tk
import os
from Crypto.Cipher import AES
from datetime import date



# Define a secret key for AES encryption
secret_key = b'abcdefghijklmnopqrstuvwxyz012345'

# Create a function to encrypt the data using AES
def encrypt(data):
    # Pad the data to a multiple of 16 bytes
    data = data.ljust((len(data) // 16 + 1) * 16)
    # Create an AES cipher object
    cipher = AES.new(secret_key, AES.MODE_ECB)
    # Encrypt the data
    ciphertext = cipher.encrypt(data)
    return ciphertext

# Create a function to decrypt the data using AES

def decrypt(ciphertext):
    # Create an AES cipher object
    cipher = AES.new(secret_key, AES.MODE_ECB)
    # Decrypt the ciphertext
    data = cipher.decrypt(ciphertext).rstrip(b'\0')
    return data



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
        user=username,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT query on the Snowflake table
    # cur.execute(f'SELECT * FROM table_name')
    # Execute the GET_DDL query
    # cur = conn.cursor()
    # cur.execute("SELECT GET_DDL('TABLE', 'employees')")

    # # Retrieve the DDL statement from the query result
    # ddl_statement = cur.fetchone()[0]

    # List of table names
    tables = ['employees', 'employees_1']

    # Get the current date
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")

    # Open the output file with the current date in the file name
    filename = f'ddl_statements_{date_string}.txt'
    with open(filename, 'a') as f:        # Iterate over the tables and execute the GET_DDL query
        for table in tables:
            # Execute the GET_DDL query for the current table
            cur = conn.cursor()
            cur.execute(f"SELECT GET_DDL('TABLE', '{table}')")

            # Retrieve the DDL statement from the query result
            ddl_statement = cur.fetchone()[0]

            # Write the DDL statement to the output file
            f.write(f"\n\n-- DDL statement for {table} table:\n{ddl_statement}\n")


    # Write the DDL statement to a text file
    # with open('ddl_statement.txt', 'w') as f:
    #     f.write(ddl_statement)


    # Close the Snowflake connection
    f.close()
    cur.close()
    conn.close()

    # Encrypt the user input values and save them to a JSON file
    data = {
        'username': encrypt(username.encode()).hex(),
        'password': encrypt(password.encode()).hex(),
        'account': encrypt(account.encode()).hex(),
    }
    with open('config.json', 'w') as f:
        json.dump(data, f)



# Create a function to reset the text fields
def reset_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    account_entry.delete(0, tk.END)
    warehouse_entry.delete(0, tk.END)
    database_entry.delete(0, tk.END)
    schema_entry.delete(0, tk.END)
    table_name_entry.delete(0, tk.END)
    try:
        os.remove('config.json')
    except:
        pass

    

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

# Create a button to rest
tk.Button(window, text='Reset', command=reset_fields).grid(row=7, column=0)

# Load the saved configuration values and pre-fill the username, password, and account fields
try:
    with open('config.json', 'r') as f:
        data = json.load(f)
        username = decrypt(bytes.fromhex(data['username'])).decode()
        password = decrypt(bytes.fromhex(data['password'])).decode()
        account = decrypt(bytes.fromhex(data['account'])).decode()
        username_entry.insert(0, data['username'])
        password_entry.insert(0, data['password'])
        account_entry.insert(0, data['account'])
except:
    pass

# Run the Tkinter event loop
window.mainloop()
