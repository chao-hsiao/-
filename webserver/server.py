from flask import Flask, jsonify, render_template
import mysql.connector
import json
import os

app = Flask(__name__, template_folder='../webserver')

# Retrieve database credentials from environment variables
db_host = os.getenv('MYSQL_HOST')  # Name of the environment variable for the database host
db_user = os.getenv('MYSQL_USERMYSQL_PASSWORD')  # Name of the environment variable for the database user
db_password = os.getenv('MYSQL_PASSWORD')  # Name of the environment variable for the database password
db_name = os.getenv('MYSQL_DB')  # Name of the environment variable for the database name

# Connect to the MySQL database
def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            database=db_name
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

# Define a route for the API
@app.route('/')
def home():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM taiwan_cities;')  # Replace with your actual table name
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html')
    else:
        return "Failed to connect to the database", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
