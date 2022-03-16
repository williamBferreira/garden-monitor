#!/usr/bin/python3
import MySQLdb, datetime, http.client, json, os
import io
import gzip


def gunzip_bytes(bytes_obj):
    in_ = io.BytesIO()
    in_.write(bytes_obj)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
        gunzipped_bytes_obj = fo.read()

    return gunzipped_bytes_obj.decode()

class mysql_database:
    def __init__(self):
        credentials_file = os.path.join(os.path.dirname(__file__), "../config/credentials.mysql")
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        for key, value in credentials.items(): #remove whitespace
            credentials[key] = value.strip()

        self.connection = MySQLdb.connect(user=credentials["USERNAME"], password=credentials["PASSWORD"], database=credentials["DATABASE"])
        self.cursor = self.connection.cursor()

    def execute(self, query, params = []):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


    def https_post(self, data, attempts = 3):
        attempt = 0
        headers = self.default_data.copy()
        headers.update(self.credentials)
        headers.update(data)

        #headers = dict(self.default_data.items() + self.credentials.items() + data.items())
        success = False
        response_data = None

        while not success and attempt < attempts:
            try:
                self.conn.request("POST", self.path, None, headers)
                response = self.conn.getresponse()
                response_data = response.read()
                print("Response status: %s, Response reason: %s, Response data: %s" % (response.status, response.reason, response_data))
                success = response.status == 200 or response.status == 201
            except Exception as e:
                print("Unexpected error", e)
            finally:
                attempt += 1

        return response_data if success else None

    def __del__(self):
        self.connection.close()

class weather_database:
    def __init__(self):
        self.db = mysql_database()
        self.insert_template = "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE, INTERNAL_TEMPERATURE, EXTERNAL_TEMPERATURE, AIR_PRESSURE, HUMIDITY, SOIL_MOISTURE, CREATED) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        self.update_template =  "UPDATE WEATHER_MEASUREMENT SET REMOTE_ID=%s WHERE ID=%s;"
        self.upload_select_template = "SELECT * FROM WEATHER_MEASUREMENT WHERE REMOTE_ID IS NULL;"
                
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_none(self, val):
        return val if val != None else "NULL"

    def insert(self, ambient_temperature, internal_temperature, external_temperature, air_pressure, humidity, soil_moisture, created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        params = ( ambient_temperature,
            internal_temperature,
            external_temperature,
            air_pressure,
            humidity,
            soil_moisture,
            created )
        print(self.insert_template % params)
        self.db.execute(self.insert_template, params)
