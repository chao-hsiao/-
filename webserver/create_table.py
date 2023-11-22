import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Database connection
user = 'root'
password = 'mysecret'
host = 'db'  # or your host
database = 'mydatabase'

# Create a connection to the database
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

# Read CSV file
df = pd.read_csv('../lvr_land_c.csv')

# Insert data into the database
df.to_sql('lvr_land_c', con=engine, if_exists='append', index=False)
