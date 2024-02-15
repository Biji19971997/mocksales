import csv
import pandas as pd
import pyodbc


server= 'mocksalesserver.database.windows.net'
database = 'mocksalesdev'
username = 'byebye' 
password = 'mockSales2024'    
driver = '{ODBC Driver 18 for SQL Server}'

# Create the connection string
connection_string = f"DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Read data from the CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

csv_file_path =r'C:\Users\Biji.Ye\OneDrive - Ascent\Documents\sales_data_mock.csv'
sales_data = read_csv(csv_file_path)

# Creation and insert of rows
df = pd.DataFrame(sales_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime

print (df)

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print(f"Connection successful! Inserting data into the 'sales' table...")
    
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO sales (transaction_id, customer_id, product_id, quantity, sale_date) "
            "VALUES (?, ?, ?, ?, ?)",
            row['transaction_id'], row['customer_id'], row['product_id'],
            row['quantity'], row['timestamp']
        )
    conn.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(f"Error connecting to the database or inserting data: {e}")
finally:
    cursor.close()
    conn.close()