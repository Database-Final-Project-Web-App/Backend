import pymysql
import json
import atexit
import os 

class DB:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        self.config = self.load_config(config_path)
        self.connection = None
        print(self.config)

        # On exit, disconnect
        atexit.register(self.disconnect)

    def load_config(self, config_file_path):
        try:
            with open(config_file_path, 'r') as file:
                config = json.load(file)
                return config
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading configuration from {config_file_path}: {e}")
            return None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, sql_query):
        try:
            if not self.connection:
                self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
            return result
        except pymysql.Error as e:
            print(f"Error executing SQL query: {e}")
            return None




if __name__ == "__main__":
    config_file = "config/dummy_config.json"
    db = DB(config_file)
    db.connect()
    
    # Example usage:
	# name each argument in the query template
    query_template = "SELECT * FROM {table} WHERE status='{status}';"
    query = query_template.format(
        table="flight",
		status="Upcoming"
	)
    result = db.execute_query(query)

    if result:
        for row in result:
            print(row)

    db.disconnect()