"""
This module provides Database-related utilities, including:
- DB: a class for connecting to a MySQL database
- ARG: a function for generating sql predicate for a given argument and its value
"""
import pymysql
import json
import atexit
import os
import datetime

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

def is_datetime(s: str) -> bool:
	"""
	Check if a string is a valid datetime string
	:param s: the string to be checked
	:return: True if the string is a valid datetime string, False otherwise
	"""
	try:
		datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
		return True
	except ValueError:
		return False

def ARG(arg_name, arg_val):
	"""
	Generate sql predicate for a given argument and its value
	
	:param arg_name: the name of the argument
	:param arg_val: the value of the argument. It can be
		- a value
		- a tuple of two number values, representing a range
		- a tuple of string values, representing a list of values
		- None, representing no constraint
        It can't be
        - a tuple of one / more than two number values
	:return: the sql predicate (as a string) for the argument

	Example:
	>>> ARG("airline_name", None)
	"TRUE"

	>>> ARG("airline_name", "Delta")
	"airline_name = Delta"

	>>> ARG("arr_airport_name", ("PVG", "JFK", "LAX"))
	"arr_airport_name IN ('PVG', 'JFK', 'LAX')"

	>>> ARG("price", (100, 200))
	"price BETWEEN 100 AND 200"

    >>> ARG("price", (100, 200, 300))
    ValueError: For number value, arg_val should be a tuple of two values
	"""

    # if arg_val is None, then no constraint
	if arg_val is None:
		return "TRUE"
	
	# if arg_val is a str, or a not subscriptable data (e.g. int), then it is a value
	if isinstance(arg_val, str) or not hasattr(arg_val, "__getitem__"):
		return "{arg_name} = {arg_val}".format(arg_name=arg_name, arg_val=repr(arg_val))

	# if not str and subscriptable, then it is a tuple

	# if it's a tuple of string, then it's a list of values
	if isinstance(arg_val[0], str):
		return "{arg_name} IN {arg_val}".format(arg_name=arg_name, arg_val=tuple(arg_val))
	
    # otherwise, it's a tuple of numbers, representing a range
    #   As a range, it must be a tuple of two values
	if len(arg_val) != 2:
		raise ValueError("For number value, arg_val should be a tuple of two values")

	#TODO: Deal with datetime


	return "{arg_name} BETWEEN {arg_val[0]} AND {arg_val[1]}".format(arg_name=arg_name, arg_val=arg_val)



if __name__ == "__main__":
    config_file = "config/dummy_config.json"
    # db = DB(config_file)
    # db.connect()

    """
    	flight_num			INT(20),
	airline_name		VARCHAR(100),
	departure_time		DATETIME,
	arrival_time		DATETIME,
	price				NUMERIC(15, 5),		
	status				VARCHAR(10),
	airplane_id			VARCHAR(10),
	arr_airport_name	VARCHAR(100),
	dept_airport_name	VARCHAR(100),
    """

    # Example usage:
	# name each argument in the query template
    query_tempate = """
    SELECT * 
    FROM {table} 
    WHERE {airline_name}
    AND {price}
    AND {status}
    AND {dept_airport_name}
    ;
    """
    query = query_tempate.format(
	    table = "flight",
		airline_name = ARG("airline_name", ("PVG", "JFK", "LAX")),
	    price = ARG("price", (135.5, 200.5)),
	    status = ARG("status", "Upcoming"),
	    dept_airport_name = ARG("dept_airport_name", None)
    )
    print(query)
    # result = db.execute_query(query)
	#
    # if result:
    #     for row in result:
    #         print(row)
	#
    # db.disconnect()

