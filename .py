import csv
import pandas as pd
import pyodbc
import sqlalchemy as sq

# Define your Azure SQL Database connection details
server= 'mocksalesserver.database.windows.net'
database = 'mocksalesdev'
username = 'byebye' 
password = 'mockSales2024'    
driver = '{ODBC Driver 17 for SQL Server}'

# Create the connection string
connection_string = f"DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"

#Try conection 
try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print(f"Connection successful! Current date from the database")
except Exception as e:
    print(f"Error connecting to the database: {e}")

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

# Assuming sales_data is a list of dictionaries
df = pd.DataFrame(sales_data)
df['transaction_id'] = df['transaction_id'].astype(str)
df['customer_id'] = df['customer_id'].astype(int)
df['product_id'] = df['product_id'].astype(int)
df['quantity'] = df['quantity'].astype(int)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Perform necessary transformations (e.g., data type conversions, cleaning)
df['date_sale'] = df['timestamp'].dt.date
print(df.dtypes)
# Create the SQLAlchemy engine
db_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
engine = sq.create_engine(db_url)

# Load the DataFrame 'df' into the 'sales' table
data_types = {
    'transaction_id': 'VARCHAR(200)',  
    'customer_id': 'INT',
    'product_id': 'INT',
    'quantity': 'INT',
    'date_sale': 'DATE',  
}
df.to_sql('sales', con=engine, if_exists='replace', index=False)
cursor = conn.cursor()
# Iterate through each row in the DataFrame and insert into the "sales" table
for _, row in df.iterrows():
    cursor.execute(
        f"INSERT INTO sales (transaction_id, customer_id, product_id, quantity, sale_date) "
        f"VALUES (?, ?, ?, ?, ?)",
        row['transaction_id'], row['customer_id'], row['product_id'],
        row['quantity'], row['sale_date']
    )
conn.commit()  
cursor.close()
conn.close()

print("Data loaded successfully into the 'sales' table.")
