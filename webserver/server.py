from flask import Flask, jsonify, render_template, request
import mysql.connector
import json
import os
# import init

app = Flask(__name__, template_folder='/webserver')

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
            database=db_name,
            allow_local_infile=True
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

# Define a route for the API
@app.route('/', methods=['POST','GET'])
def home():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM taiwan_cities")
            cities = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 出租型態 FROM lvr_land_c")
            rental_types = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('index.html',data={'cities': cities, 'rental_types': rental_types})
        elif request.method == 'POST':
            data = request.json
            selected_city_id = data['selected_city_id']
            cursor.execute("SELECT * FROM taiwan_districts WHERE city_id = %s", (int(selected_city_id),))
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(results)
    else:
        return "Failed to connect to the database", 500

@app.route('/results', methods=['POST'])
def results():
    results = {
        'city': request.form.get('city'),
        'district': request.form.get('district'),
        'lowerprice': request.form.get('lowerprice'),
        'upperprice': request.form.get('upperprice'),
        'lowerarea': request.form.get('lowerarea'),
        'upperarea': request.form.get('upperarea'),
        'rental_type': request.form.get('rental_type'),
        'keyword': request.form.get('keyword')
    }

    # return render_template('results.html',results=data)
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(construct_query(results))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not rows:
            return "No data found for the given parameters.<br>" + construct_query(results)

        # Constructing HTML table
        table_html = "<table border='1'>"
        table_html += "<tr>"
        for header in rows[0].keys():
            table_html += f"<th>{header}</th>"
        table_html += "</tr>"

        for row in rows:
            table_html += "<tr>"
            for cell in row.values():
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"

        return table_html
    else:
        return "Failed to connect to the database", 500

def construct_query(params):
    base_query = "SELECT * FROM lvr_land_c"
    conditions = []

    if params['city']:
        conditions.append(f"lvr_land_c.city_id = {params['city']}")

    if params['district'] != '0':
        conditions.append(f"lvr_land_c.district_id = {params['district']}")

    if params['lowerprice'] and params['upperprice']:
        conditions.append(f"lvr_land_c.總額元 BETWEEN {params['lowerprice']} AND {params['upperprice']}")

    if params['lowerarea'] and params['upperarea']:
        conditions.append(f"lvr_land_c.建物總面積平方公尺 BETWEEN {params['lowerarea']} AND {params['upperarea']}")

    if params['rental_type'] != '0':
        conditions.append(f"lvr_land_c.出租型態 = '{params['rental_type']}'")

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    return base_query


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
