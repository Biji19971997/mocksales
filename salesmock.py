import csv
import os
from faker import Faker

# Initialize Faker for generating realistic data
fake = Faker()

# Define the number of mock transactions
num_transactions = 100

# Generate mock data
sales_data = []
for _ in range(num_transactions):
    transaction_id = fake.uuid4()
    customer_id = fake.random_int(min=100, max=999)
    product_id = fake.random_int(min=1, max=100)
    quantity = fake.random_int(min=1, max=10)
    timestamp = fake.date_time_between(start_date='-1y', end_date='now')

    sales_data.append({
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'product_id': product_id,
        'quantity': quantity,
        'timestamp': timestamp,
    })

# Define the folder path where you want to save the CSV file
output_folder = r'C:\Users\Biji.Ye\OneDrive - Ascent\Documents'

# Create the full file path
csv_file_path = os.path.join(output_folder, 'sales_data_mock.csv')

# Write mock data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['transaction_id', 'customer_id', 'product_id', 'quantity', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sales_data)

print(f"Mock data saved to {csv_file_path}")