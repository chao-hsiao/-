from flask import Flask, jsonify, render_template, request, redirect, url_for,  session
import mysql.connector
import json
import os

app = Flask(__name__, template_folder='/webserver')
app.secret_key = 'secret'

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
        cursor.execute("SELECT * FROM taiwan_cities")
        cities = cursor.fetchall()
        cursor.execute("SELECT DISTINCT 出租型態 FROM lvr_land_c")
        rental_type = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html',data={'cities': cities, 'rental_type': rental_type})
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

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(construct_query(results))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not rows:
            return render_template("no_data_found_page.html", data=construct_query(results))

        # Constructing HTML table
        table_html = "<link rel='stylesheet' href='static/style.css'>"
        table_html += "<table border='1'>"
        table_html += "<tr>"
        table_html += "<th>Action</th>"  # Header for the delete button column
        for header in rows[0].keys():
            table_html += f"<th>{header}</th>"
        table_html += "</tr>"

        for row in rows:
            row_id = row['serial_number'] + row['土地位置建物門牌']
            row_id1 = row['serial_number']
            row_id2 = row['土地位置建物門牌']
            table_html += f"<tr id='row-{row_id}'>"
            table_html += f"<td><button type='button' id='deleteButton' class='button delete-button' button onclick='deleteRow(`{row_id1}`,`{row_id2}`)'>Delete</button><br>"  # Delete button
            table_html += f"<button type='button' id='modify-button' class='button modify-button' button onclick='modifyRow(`{row_id1}`,`{row_id2}`)'>Modify</button></td>"  # Modify button
            for cell in row.values():
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        table_html += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'></script>"
        table_html += "<script src='static/scripts_del_mod.js'></script>"

        return table_html
    else:
        return "Failed to connect to the database", 500

def construct_query(params):
    base_query = "SELECT * FROM lvr_land_c"
    conditions = []

    if params['city']:
        conditions.append(f"lvr_land_c.city_id = {params['city']}")

    if params['district'] != '':
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

@app.route('/getDistrictOptions', methods=['POST'])
def getDistrictOptions():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        selected_id = data['selected_id']
        cursor.execute("SELECT * FROM taiwan_districts WHERE city_id = %s", (int(selected_id),))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(results)
    else:
        return "Failed to connect to the database", 500

@app.route('/add_item', methods=['POST','GET'])
def add_item():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM taiwan_cities")
            cities = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 出租型態 FROM lvr_land_c")
            rental_type = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 都市土地使用分區 FROM lvr_land_c")
            land_using_type_for_urban = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 非都市土地使用分區 FROM lvr_land_c")
            land_using_type_for_non_urban = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 非都市土地使用編定 FROM lvr_land_c")
            non_urban_land_classification = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 建物型態 FROM lvr_land_c")
            building_type = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 車位類別 FROM lvr_land_c")
            parking_type = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('add_data.html',data={
                'cities': cities, 
                'rental_type': rental_type, 
                'land_using_type_for_urban': land_using_type_for_urban,
                'land_using_type_for_non_urban': land_using_type_for_non_urban,
                'non_urban_land_classification': non_urban_land_classification,
                'building_type': building_type,
                'parking_type': parking_type
                })
        elif request.method == 'POST':
            data = request.json
            selected_id = data['selected_id']
            if data['case'] == 1:
                cursor.execute(f"SELECT DISTINCT serial_number FROM lvr_land_c WHERE district_id = {selected_id}")
            elif data['case'] == 2:
                cursor.execute(f"SELECT DISTINCT 建築完成日期, 主要建材, 總層數 FROM lvr_land_c_build WHERE serial_number = '{selected_id}'")

            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(results)
    else:
        return "Failed to connect to the database", 500

def f(s):
    if len(s) == 1:
        return '0' + s
    return s

@app.route('/upload', methods=['POST'])
def upload():
    upload = {
        'city_id': request.form.get('city'),
        'district_id': request.form.get('district'),
        '出租型態': request.form.get('rental_type'),
        '交易標的': request.form.get('transaction_object'),
        '土地位置建物門牌': request.form.get('address'),
        '土地面積平方公尺': request.form.get('land_area'),
        '都市土地使用分區': request.form.get('land_using_type_for_urban'),
        '非都市土地使用分區': request.form.get('land_using_type_for_non_urban'),
        '非都市土地使用編定': request.form.get('non_urban_land_classification'),
        'rent_year': request.form.get('rent_year'),
        'rent_month': request.form.get('rent_month'),
        'rent_day': request.form.get('rent_day'),
        'land': request.form.get('land'),
        'building': request.form.get('building'),
        'park': request.form.get('park'),
        '租賃層次': request.form.get('floor'),
        '總樓層數': request.form.get('t_floor'),
        '建物型態': request.form.get('building_type'),
        '主要用途': request.form.get('main_use'),
        '主要建材': request.form.get('main_material'),
        'finish_year': request.form.get('finish_year'),
        'finish_month': request.form.get('finish_month'),
        'finish_day': request.form.get('finish_day'),
        '建物總面積平方公尺': request.form.get('t_area'),
        '建物現況格局_房': request.form.get('room'),
        '建物現況格局_廳': request.form.get('living'),
        '建物現況格局_衛': request.form.get('toilet'),
        '建物現況格局_隔間': request.form.get('cubicle'),
        '有無管理組織': request.form.get('has_org') if request.form.get('has_org') else '0',
        '有無附傢俱': request.form.get('has_furniture') if request.form.get('has_furniture') else '0',
        '總額元': request.form.get('t_cost'),
        '車位類別': request.form.get('parking_type'),
        '車位面積平方公尺': request.form.get('p_area'),
        '車位總額元': request.form.get('p_t_cost'),
        '車位所在樓層': request.form.get('p_floor'),
        'under': request.form.get('under') if request.form.get('under') else 0,
        '備註': request.form.get('note'),
        '有無管理員': request.form.get('has_security') if request.form.get('has_security') else '0',
        '有無電梯': request.form.get('has_lift') if request.form.get('has_lift') else '0',
        '附屬設備': request.form.get('other_equipment'),
        'serial_number': request.form.get('serial_number') if request.form.get('serial_number') else request.form.get('serial_number_input')
    }

    upload['租賃年月日'] = f(upload['rent_year']) + f(upload['rent_month']) + f(upload['rent_day'])
    upload['建築完成年月日'] = f(upload['finish_year']) + f(upload['finish_month']) + f(upload['finish_day'])
    upload['租賃筆棟數'] = '土地' + upload['land'] + '建物' + upload['building'] + '車位' + upload['park']
    upload['單價元平方公尺'] = str(int(upload['總額元']) // int(upload['建物總面積平方公尺']))
    upload['租賃層次'] = arabic_to_chinese(int(upload['租賃層次'])) + '層'
    try:
        upload['車位所在樓層'] = '地下' + arabic_to_chinese(int(upload['車位所在樓層'])) + '樓' if int(upload['under']) else arabic_to_chinese(int(upload['車位所在樓層'])) + '樓'
    except ValueError:
        upload['車位所在樓層'] = ""

    upload_park = {
        'serial_number': upload['serial_number'],
        '車位類別': upload['車位類別'],
        '車位價格': upload['車位總額元'],
        '車位面積平方公尺': upload['車位面積平方公尺'],
        '車位所在樓層' : upload['車位所在樓層'],
    }

    del upload['車位所在樓層']
    del upload['rent_year'] 
    del upload['rent_month']
    del upload['rent_day']
    del upload['finish_year']
    del upload['finish_month']
    del upload['finish_day']
    del upload['land']
    del upload['building']
    del upload['park']
    del upload['under']

    upload = {k: v for k, v in upload.items() if v != "" and v != None}
    upload_park = {k: v for k, v in upload_park.items() if v != "" and v != None}

    connection = get_db_connection()
    if connection:
        is_exist = False
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT serial_number from lvr_land_c_build")
        sn = cursor.fetchall()
        for row in sn:
            if upload['serial_number'] == row['serial_number']:
                is_exist = True
                break

        queries = []
        columns = ', '.join(upload.keys())
        values = "'" + "', '".join(upload.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c ({columns}) VALUES ({values});")

        columns = ', '.join(upload_park.keys())
        values = "'" + "', '".join(upload_park.values()) + "'"
        if columns != "":
            queries.append(f"INSERT IGNORE INTO lvr_land_c_park ({columns}) VALUES ({values});")

        if not is_exist:
            session.clear()
            session['upload'] = upload
            session['queries'] = queries
            cursor.close()
            connection.close()
            return redirect(url_for("cont"))

        for query in queries:
            cursor.execute(query)

        connection.commit()
        cursor.close()
        connection.close()
        return render_template('alert_msg.html',msg=True)
    else:
        return "Failed to connect to the database", 500

@app.route('/cont', methods=['POST','GET'])
def cont():
    if request.method == 'POST':
        upload = session.get('upload', {})
        queries = session.get('queries', {})
        session.clear()

        upload_build = {
            'serial_number': upload['serial_number'],
            '建物移轉面積平方公尺': request.form.get('building_transfer_area'),
            '主要用途': request.form.get('main_use'),
            '主要建材': upload['主要建材'],
            '建築完成日期': upload['建築完成年月日'][:-4] + '年' + upload['建築完成年月日'][-4:-2] + '月' + upload['建築完成年月日'][-2:]  + '日',
            '總層數': arabic_to_chinese(int(upload['總樓層數']))
        }
        upload_land = {
            'serial_number': upload['serial_number'],
            '土地位置': request.form.get('land_location'),
            '土地移轉面積平方公尺': request.form.get('land_transfer_area'),
            '使用分區或編定': request.form.get('land_use_partition'),
            '地號': request.form.get('land_number')
        }

        columns = ', '.join(upload_build.keys())
        values = "'" + "', '".join(upload_build.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c_build ({columns}) VALUES ({values});")
            
        columns = ', '.join(upload_land.keys())
        values = "'" + "', '".join(upload_land.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c_land ({columns}) VALUES ({values});")

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            for query in queries:
                cursor.execute(query)
            
            connection.commit()
            cursor.close()
            connection.close()
            return render_template('alert_msg.html',msg=True)
        else:
            return "Failed to connect to the database", 500
    
    return render_template('add_data_cont.html')


def arabic_to_chinese(arabic_number):
    chinese_digits = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    chinese_tens = {10: '十'}

    if arabic_number < 10:
        return chinese_digits[arabic_number]
    elif arabic_number < 20:
        return chinese_tens[10] + chinese_digits.get(arabic_number % 10, '')
    elif arabic_number >=100:
        return '一百'
    else:
        tens, ones = divmod(arabic_number, 10)
        return chinese_digits[tens] + chinese_tens[10] + chinese_digits.get(ones, '')

@app.route('/delete_item', methods=['POST'])
def delete_item():
    # Logic to delete an item from the database
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        data = request.json
        row_id1 = data['id1']
        row_id2 = data['id2']

        sql = f"DELETE FROM lvr_land_c WHERE serial_number = '{row_id1}' AND 土地位置建物門牌 = '{row_id2}';"
        cursor.execute(sql)

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True})
    else:
        return "Failed to connect to the database", 500


@app.route('/modify_item', methods=['POST'])
def modify_item():
    # Logic to modify an item in the database
    return jsonify({'status': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)









from flask import Flask, jsonify, render_template, request, redirect, url_for,  session
import mysql.connector
import json
import os

app = Flask(__name__, template_folder='/webserver')
app.secret_key = 'secret'

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
        cursor.execute("SELECT * FROM taiwan_cities")
        cities = cursor.fetchall()
        cursor.execute("SELECT DISTINCT 出租型態 FROM lvr_land_c")
        rental_type = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html',data={'cities': cities, 'rental_type': rental_type})
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
        table_html = "<link rel='stylesheet' href='static/style.css'>"
        table_html += "<table border='1'>"
        table_html += "<tr>"
        table_html += "<th>Action</th>"  # Header for the delete button column
        for header in rows[0].keys():
            table_html += f"<th>{header}</th>"
        table_html += "</tr>"

        for row in rows:
            row_id = row['serial_number'] + row['土地位置建物門牌']
            row_id1 = row['serial_number']
            row_id2 = row['土地位置建物門牌']
            table_html += f"<tr id='row-{row_id}'>"
            table_html += f"<td><button type='button' id='deleteButton' class='button delete-button' button onclick='deleteRow(`{row_id1}`,`{row_id2}`)'>Delete</button><br>"  # Delete button
            table_html += f"<button type='button' id='modify-button' class='button modify-button' button onclick='modifyRow(`{row_id1}`,`{row_id2}`)'>Modify</button></td>"  # Modify button
            for cell in row.values():
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        table_html += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'></script>"
        table_html += "<script src='static/scripts_del_mod.js'></script>"

        return table_html
    else:
        return "Failed to connect to the database", 500

def construct_query(params):
    base_query = "SELECT * FROM lvr_land_c"
    conditions = []

    if params['city']:
        conditions.append(f"lvr_land_c.city_id = {params['city']}")

    if params['district'] != '':
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

@app.route('/getDistrictOptions', methods=['POST'])
def getDistrictOptions():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        data = request.json
        selected_id = data['selected_id']
        cursor.execute("SELECT * FROM taiwan_districts WHERE city_id = %s", (int(selected_id),))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(results)
    else:
        return "Failed to connect to the database", 500

@app.route('/add_item', methods=['POST','GET'])
def add_item():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        if request.method == 'GET':
            cursor.execute("SELECT * FROM taiwan_cities")
            cities = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 出租型態 FROM lvr_land_c")
            rental_type = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 都市土地使用分區 FROM lvr_land_c")
            land_using_type_for_urban = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 非都市土地使用分區 FROM lvr_land_c")
            land_using_type_for_non_urban = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 非都市土地使用編定 FROM lvr_land_c")
            non_urban_land_classification = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 建物型態 FROM lvr_land_c")
            building_type = cursor.fetchall()
            cursor.execute("SELECT DISTINCT 車位類別 FROM lvr_land_c")
            parking_type = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('add_data.html',data={
                'cities': cities, 
                'rental_type': rental_type, 
                'land_using_type_for_urban': land_using_type_for_urban,
                'land_using_type_for_non_urban': land_using_type_for_non_urban,
                'non_urban_land_classification': non_urban_land_classification,
                'building_type': building_type,
                'parking_type': parking_type
                })
        elif request.method == 'POST':
            data = request.json
            selected_id = data['selected_id']
            if data['case'] == 1:
                cursor.execute(f"SELECT DISTINCT serial_number FROM lvr_land_c WHERE district_id = {selected_id}")
            elif data['case'] == 2:
                cursor.execute(f"SELECT DISTINCT 建築完成日期, 主要建材, 總層數 FROM lvr_land_c_build WHERE serial_number = '{selected_id}'")

            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(results)
    else:
        return "Failed to connect to the database", 500

def f(s):
    if len(s) == 1:
        return '0' + s
    return s

@app.route('/upload', methods=['POST'])
def upload():
    upload = {
        'city_id': request.form.get('city'),
        'district_id': request.form.get('district'),
        '出租型態': request.form.get('rental_type'),
        '交易標的': request.form.get('transaction_object'),
        '土地位置建物門牌': request.form.get('address'),
        '土地面積平方公尺': request.form.get('land_area'),
        '都市土地使用分區': request.form.get('land_using_type_for_urban'),
        '非都市土地使用分區': request.form.get('land_using_type_for_non_urban'),
        '非都市土地使用編定': request.form.get('non_urban_land_classification'),
        'rent_year': request.form.get('rent_year'),
        'rent_month': request.form.get('rent_month'),
        'rent_day': request.form.get('rent_day'),
        'land': request.form.get('land'),
        'building': request.form.get('building'),
        'park': request.form.get('park'),
        '租賃層次': request.form.get('floor'),
        '總樓層數': request.form.get('t_floor'),
        '建物型態': request.form.get('building_type'),
        '主要用途': request.form.get('main_use'),
        '主要建材': request.form.get('main_material'),
        'finish_year': request.form.get('finish_year'),
        'finish_month': request.form.get('finish_month'),
        'finish_day': request.form.get('finish_day'),
        '建物總面積平方公尺': request.form.get('t_area'),
        '建物現況格局_房': request.form.get('room'),
        '建物現況格局_廳': request.form.get('living'),
        '建物現況格局_衛': request.form.get('toilet'),
        '建物現況格局_隔間': request.form.get('cubicle'),
        '有無管理組織': request.form.get('has_org') if request.form.get('has_org') else '0',
        '有無附傢俱': request.form.get('has_furniture') if request.form.get('has_furniture') else '0',
        '總額元': request.form.get('t_cost'),
        '車位類別': request.form.get('parking_type'),
        '車位面積平方公尺': request.form.get('p_area'),
        '車位總額元': request.form.get('p_t_cost'),
        '車位所在樓層': request.form.get('p_floor'),
        'under': request.form.get('under') if request.form.get('under') else 0,
        '備註': request.form.get('note'),
        '有無管理員': request.form.get('has_security') if request.form.get('has_security') else '0',
        '有無電梯': request.form.get('has_lift') if request.form.get('has_lift') else '0',
        '附屬設備': request.form.get('other_equipment'),
        'serial_number': request.form.get('serial_number') if request.form.get('serial_number') else request.form.get('serial_number_input')
    }

    upload['租賃年月日'] = f(upload['rent_year']) + f(upload['rent_month']) + f(upload['rent_day'])
    upload['建築完成年月日'] = f(upload['finish_year']) + f(upload['finish_month']) + f(upload['finish_day'])
    upload['租賃筆棟數'] = '土地' + upload['land'] + '建物' + upload['building'] + '車位' + upload['park']
    upload['單價元平方公尺'] = str(int(upload['總額元']) // int(upload['建物總面積平方公尺']))
    upload['租賃層次'] = arabic_to_chinese(int(upload['租賃層次'])) + '層'
    try:
        upload['車位所在樓層'] = '地下' + arabic_to_chinese(int(upload['車位所在樓層'])) + '樓' if int(upload['under']) else arabic_to_chinese(int(upload['車位所在樓層'])) + '樓'
    except ValueError:
        upload['車位所在樓層'] = ""

    upload_park = {
        'serial_number': upload['serial_number'],
        '車位類別': upload['車位類別'],
        '車位價格': upload['車位總額元'],
        '車位面積平方公尺': upload['車位面積平方公尺'],
        '車位所在樓層' : upload['車位所在樓層'],
    }

    del upload['車位所在樓層']
    del upload['rent_year'] 
    del upload['rent_month']
    del upload['rent_day']
    del upload['finish_year']
    del upload['finish_month']
    del upload['finish_day']
    del upload['land']
    del upload['building']
    del upload['park']
    del upload['under']

    upload = {k: v for k, v in upload.items() if v != "" and v != None}
    upload_park = {k: v for k, v in upload_park.items() if v != "" and v != None}

    connection = get_db_connection()
    if connection:
        is_exist = False
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT serial_number from lvr_land_c_build")
        sn = cursor.fetchall()
        for row in sn:
            if upload['serial_number'] == row['serial_number']:
                is_exist = True
                break

        queries = []
        columns = ', '.join(upload.keys())
        values = "'" + "', '".join(upload.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c ({columns}) VALUES ({values});")

        columns = ', '.join(upload_park.keys())
        values = "'" + "', '".join(upload_park.values()) + "'"
        if columns != "":
            queries.append(f"INSERT IGNORE INTO lvr_land_c_park ({columns}) VALUES ({values});")

        if not is_exist:
            session.clear()
            session['upload'] = upload
            session['queries'] = queries
            cursor.close()
            connection.close()
            return redirect(url_for("cont"))

        for query in queries:
            cursor.execute(query)

        connection.commit()
        cursor.close()
        connection.close()
        return render_template('alert_msg.html',msg=True)
    else:
        return "Failed to connect to the database", 500

@app.route('/cont', methods=['POST','GET'])
def cont():
    if request.method == 'POST':
        upload = session.get('upload', {})
        queries = session.get('queries', {})
        session.clear()

        upload_build = {
            'serial_number': upload['serial_number'],
            '建物移轉面積平方公尺': request.form.get('building_transfer_area'),
            '主要用途': request.form.get('main_use'),
            '主要建材': upload['主要建材'],
            '建築完成日期': upload['建築完成年月日'][:-4] + '年' + upload['建築完成年月日'][-4:-2] + '月' + upload['建築完成年月日'][-2:]  + '日',
            '總層數': arabic_to_chinese(int(upload['總樓層數']))
        }
        upload_land = {
            'serial_number': upload['serial_number'],
            '土地位置': request.form.get('land_location'),
            '土地移轉面積平方公尺': request.form.get('land_transfer_area'),
            '使用分區或編定': request.form.get('land_use_partition'),
            '地號': request.form.get('land_number')
        }

        columns = ', '.join(upload_build.keys())
        values = "'" + "', '".join(upload_build.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c_build ({columns}) VALUES ({values});")
            
        columns = ', '.join(upload_land.keys())
        values = "'" + "', '".join(upload_land.values()) + "'"
        if columns != "":
            queries.append(f"INSERT INTO lvr_land_c_land ({columns}) VALUES ({values});")

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            for query in queries:
                cursor.execute(query)
            
            connection.commit()
            cursor.close()
            connection.close()
            return render_template('alert_msg.html',msg=True)
        else:
            return "Failed to connect to the database", 500
    
    return render_template('add_data_cont.html')


def arabic_to_chinese(arabic_number):
    chinese_digits = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    chinese_tens = {10: '十'}

    if arabic_number < 10:
        return chinese_digits[arabic_number]
    elif arabic_number < 20:
        return chinese_tens[10] + chinese_digits.get(arabic_number % 10, '')
    elif arabic_number >=100:
        return '一百'
    else:
        tens, ones = divmod(arabic_number, 10)
        return chinese_digits[tens] + chinese_tens[10] + chinese_digits.get(ones, '')

@app.route('/delete_item', methods=['POST'])
def delete_item():
    # Logic to delete an item from the database
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        data = request.json
        row_id1 = data['id1']
        row_id2 = data['id2']

        sql = f"DELETE FROM lvr_land_c WHERE serial_number = '{row_id1}' AND 土地位置建物門牌 = '{row_id2}';"
        cursor.execute(sql)

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True})
    else:
        return "Failed to connect to the database", 500


@app.route('/modify_item', methods=['POST'])
def modify_item():
    # Logic to modify an item in the database
    return jsonify({'status': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)









