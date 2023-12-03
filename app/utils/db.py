"""
This module provides Database-related utilities, including:
- DB: a class for connecting to a MySQL database
- ARG: a function for generating sql predicate for a given argument and its value
"""
import pymysql
import json
import atexit
import os
from datetime import datetime, timedelta

from app.utils.auth import LOGINTYPE, PERMISSION

from flask import current_app, jsonify 

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
                database=self.config['database'],
            )
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, sql_query, cursor_type="list"):
        try:
            if not self.connection:
                self.connect()
            if cursor_type == "list":
                cursor = self.connection.cursor()
            elif cursor_type == "dict":
                cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            else:
                raise ValueError(f"Invalid cursor_type: {cursor_type}")
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pymysql.Error as e:
            print(f"Error executing SQL query: {e}")
            return None
    
    def commit(self):
        self.connection.commit()


def is_datetime(s: str) -> bool:
    """
    Check if a string is a valid datetime string
    :param s: the string to be checked
    :return: True if the string is a valid datetime string, False otherwise
    """
    try:
        floor_datetime(s)
        return True
    except ValueError:
        return False

def floor_datetime(s: str) -> str:
    """
    Floor YMD, YMDH, YMDHM, YMDHMS to the nearest smaller YMDHMS
    i.e. largest YMDHMS that is <= s

    floor_datetime is idempotent, i.e. floor_datetime(floor_datetime(s)) == floor_datetime(s)

    :param s: the datetime string to be floored
    :return: the floored datetime string

    Example:
    >>> floor_datetime("2020-01-23")
    "2020-01-23 00:00:00"

    >>> floor_datetime("2020-01-23 11")
    "2020-01-23 11:00:00" 
    
    >>> floor_datetime("2020-01-23 11:34")
    "2020-01-01 11:34:00"

    >>> floor_datetime("2020-01-23 11:34:56")
    "2020-01-01 11:34:56"
    """
    # is it YMD?
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s + " 00:00:00"
    except ValueError:
        pass

    # is it YMDH?
    try:
        datetime.strptime(s, "%Y-%m-%d %H")
        return s + ":00:00"
    except ValueError:
        pass

    # is it YMDHM?
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M")
        return s + ":00"
    except ValueError:
        pass

    # is it YMDHMS?
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return s
    except ValueError:
        pass

    raise ValueError("Invalid datetime string: {s}".format(s=s))


def ceil_datetime(s: str) -> str:
    """
    Ceil YMD, YMDH, YMDHM, YMDHMS to the nearest larger YMDHMS
    i.e. smallest YMDHMS that is >= s 

    ceil_datetime is idempotent, i.e. ceil_datetime(ceil_datetime(s)) == ceil_datetime(s)

    :param s: the datetime string to be ceiled
    :return: the ceiled datetime string

    Example:
    >>> ceil_datetime("2020-01-23")
    "2020-01-23 23:59:59"

    >>> ceil_datetime("2020-01-23 11")
    "2020-01-23 11:59:59"

    >>> ceil_datetime("2020-01-23 11:34")
    "2020-01-01 11:34:59"

    >>> ceil_datetime("2020-01-23 11:34:56")
    "2020-01-01 11:34:56" 
    """
    # is it YMD?
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s + " 23:59:59"
    except ValueError:
        pass

    # is it YMDH?
    try:
        datetime.strptime(s, "%Y-%m-%d %H")
        return s + ":59:59"
    except ValueError:
        pass

    # is it YMDHM?
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M")
        return s + ":59"
    except ValueError:
        pass

    # is it YMDHMS?
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return s
    except ValueError:
        pass

    raise ValueError("Invalid datetime string: {s}".format(s=s))


def date2datetime_range(s):
    """
    Convert a date string to a datetime range tuple

    :param s: the date string to be converted
    :return: a datetime range tuple

    Example:
    >>> date2datetime_range("2020-01-23")
    ("2020-01-23 00:00:00", "2020-01-23 23:59:59")
    """
    if s is None:
        return None 
    return (floor_datetime(s), ceil_datetime(s))

def V_ARG(arg_type: str, arg_val):
    """
    Arg for INSERT query. More restricted than WHERE_ARG

    :param arg_type: the type of the argument. It can be
        - "string"
        - "number"
        - "datetime"

    :param arg_val: the value of the argument. For each type, it can be
        - "string"
            - a string value, representing a value
            - None, representing no value
        - "number"
            - a number value, representing a value
            - None, representing no value
        - "datetime"
            - a datetime string, representing a value
            - None, representing no value
    """

    if arg_type == "string":
        if arg_val is None:
            return "NULL"
        return "'{}'".format(arg_val)

    elif arg_type == "number":
        if arg_val is None:
            return "NULL"
        return arg_val

    elif arg_type == "datetime":
        if arg_val is None:
            return "NULL"
        if not is_datetime(arg_val):
            raise ValueError("For datetime value, arg_val should be a datetime string, but got {arg_val}".format(arg_val=arg_val))
        return "\"{}\"".format(floor_datetime(arg_val))

    return None

def KV_ARG(arg_name: str, arg_type: str, arg_val, mode="general"):
    """
    Generate sql predicate for a given argument and its value
    
    :param arg_name: the name of the argument

    :param arg_type: the type of the argument. It can be
        - "string"
        - "number"
        - "datetime"

    :param arg_val: the value of the argument. For each type, it can be
        - "string"
            - a string value, representing a value
            - a tuple of string values, representing a list of values
            - None, representing no constraint
        - "number"
            - a number value, representing a value
            - a tuple of two number values, representing a range
            - None, representing no constraint
        - "datetime"
            - a datetime string, representing a value
            - a tuple of two datetime strings, representing a range
                In this tuple, if one entry is None, then it represents no constraint
                e.g. 
                ("2020-01-01 00:00:00", "2020-01-02 00:00:00") represents a range from 2020-01-01 00:00:00 to 2020-01-02 00:00:00
                ("2020-01-01 00:00:00", None) represents a range from 2020-01-01 00:00:00 to infinity
                (None, "2020-01-01 00:00:00") represents a range from -infinity to 2020-01-01 00:00:00
                (None, None) represents no constraint
            - None, representing no constraint
    :return: the sql predicate (as a string) for the argument

    Example:
    >>> ARG("airline_name", "string", None)
    "TRUE"

    >>> ARG("airline_name", "string", "Delta")
    "airline_name = Delta"

    >>> ARG("arr_airport_name", "string", ("PVG", "JFK", "LAX"))
    "arr_airport_name IN ('PVG', 'JFK', 'LAX')"

    >>> ARG("price", "number", 100)
    "price = 100"

    >>> ARG("price", "number", (100, 200))
    "price BETWEEN 100 AND 200"

    >>> ARG("price", "number", (100, 200, 300))
    ValueError: For number value, arg_val should be a tuple of two values

    >>> ARG("arrival_date", "datetime", None)
    "TRUE"

    >>> ARG("arrival_date", "datetime", "2020-01-02 10:23")
    "arrival_date BETWEEN '2020-01-02 10:23:00' AND '2020-01-02 10:23:59'"

    >>> ARG("arrival_date", "datetime", ("2020-01-02 10:23", "2020-01-02 11"))
    "arrival_date BETWEEN '2020-01-02 10:23:00' AND '2020-01-02 11:59:59'"

    """
    if mode not in ["general", "restricted"]:
        raise ValueError("mode should be either 'general' or 'restricted'")
    
    if arg_type == "string":
        if arg_val is None:
            return "TRUE"

        if isinstance(arg_val, str):
            return "{arg_name} = '{arg_val}'".format(arg_name=arg_name, arg_val=arg_val)

        if mode == "restricted":
            raise ValueError("For string value, arg_val should be a string, but got {arg_val}".format(arg_val=arg_val))

        try:
            arg_val = tuple(arg_val)
        except TypeError:
            raise ValueError("For string value, arg_val should be a string or a tuple of string values, but got {arg_val}".format(arg_val=arg_val)) 

        if isinstance(arg_val[0], str):
            return "{arg_name} IN {arg_val}".format(arg_name=arg_name, arg_val=arg_val)
        raise ValueError("For string value, arg_val should be a string or a tuple of string values, but got {arg_val}".format(arg_val=arg_val))

    elif arg_type == "number":
        if arg_val is None:
            return "TRUE"

        if isinstance(arg_val, (int, float)):
            return "{arg_name} = {arg_val}".format(arg_name=arg_name, arg_val=repr(arg_val))

        if mode == "restricted":
            raise ValueError("For number value, arg_val should be a number, but got {arg_val}".format(arg_val=arg_val))

        try:
            arg_val = tuple(arg_val)
        except TypeError:
            raise ValueError("For number value, arg_val should be a number or a tuple of two number values, but got {arg_val}".format(arg_val=arg_val))

        if len(arg_val) != 2:
            raise ValueError("For number value, arg_val should be a tuple of two values, but got {arg_val}".format(arg_val=arg_val))
        return "{arg_name} BETWEEN {arg_val[0]} AND {arg_val[1]}".format(arg_name=arg_name, arg_val=arg_val)
        
    elif arg_type == "datetime":
        if arg_val is None:
            return "TRUE"

        if isinstance(arg_val, str):
            if not is_datetime(arg_val):
                raise ValueError("For datetime value, arg_val should be a datetime string, but got {arg_val}".format(arg_val=arg_val))
            arg_val = (floor_datetime(arg_val), ceil_datetime(arg_val))

        if mode == "restricted":
            return "{arg_name} = \"{arg_val}\"".format(
                arg_name=arg_name, 
                arg_val=floor_datetime(arg_val)
                )

        try:
            arg_val = tuple(arg_val)
        except TypeError:
            raise ValueError("For datetime value, arg_val should be a datetime string or a tuple of two datetime strings, but got {arg_val}".format(arg_val=arg_val))
        if len(arg_val) != 2:
            raise ValueError("For datetime value, arg_val should be a tuple of two values, but got {arg_val}".format(arg_val=arg_val))

        if not (is_datetime(arg_val[0]) and is_datetime(arg_val[1])):
            raise ValueError("For datetime value, arg_val should be a datetime string or a tuple of two datetime strings, but got {arg_val}".format(arg_val=arg_val))
        return "{arg_name} BETWEEN \"{arg_val_min}\" AND \"{arg_val_max}\"".format(
            arg_name=arg_name, 
            arg_val_min=floor_datetime(arg_val[0]),
            arg_val_max=ceil_datetime(arg_val[1])
            )

    return None


# Determine whether a user exists
def user_exists(db, username, logintype, db_kwargs={"cursor_type": "list"}):
    user_exists_query = \
    """
    SELECT *
    FROM {logintype}
    WHERE {username}
    """
    # Determine whether a valid logintype: customer, booking_agent, airline_staff
    if not LOGINTYPE.is_valid(logintype):
        raise Exception("You must choose a correct logintype. Your input logintype is {}".format(logintype))
    

    user_exists_query = user_exists_query.format(
        logintype=logintype,
        username=KV_ARG("username", "string", username),
    )

    result = db.execute_query(user_exists_query, **db_kwargs)
    if result:
        return True, result 
    return False, None 

# Check if there are tickets left for a flight
def ticket_left(db, flight_num, airline_name):
    ticket_left_query_template = \
	"""
	WITH flight_seat AS
	(SELECT flight_num, airline_name, airplane_id, seat_num
	FROM flight NATURAL JOIN airplane)
	SELECT seat_num - COUNT(ticket_id) AS ticket_left, airline_name, flight_num, airplane_id, seat_num
	FROM flight_seat NATURAL JOIN ticket
	WHERE {flight_num}
    AND {airline_name}
	GROUP BY airline_name, flight_num, airplane_id
	"""

    ticket_left_query = ticket_left_query_template.format(
		flight_num=KV_ARG("flight_num", "number", flight_num, mode="restricted"),
        airline_name=KV_ARG("airline_name", "string", airline_name, mode="restricted"),
	)

    ticket_left = db.execute_query(ticket_left_query)
    if ticket_left is None:
        return False
    return True

# find the airline a staff works for
def find_airline_for_staff(db, username):
    find_airline_query_template = \
    """
    SELECT airline_name
    FROM airline_staff
    WHERE username = {username}
    """
    find_airline_query = find_airline_query_template.format(
        username=KV_ARG("username", "string", username)
    )
    airline_name = db.execute_query(find_airline_query)
    return airline_name[0]["airline_name"]

# find the permission of a staff
def find_permission(db, username):
    find_permission_query_template = \
    """
    SELECT permission
    FROM airline_staff_permission
    WHERE username = {username}
    """
    find_permission_query = find_permission_query_template.format(
        username=KV_ARG("username", "string", username)
    )
    permission = db.execute_query(find_permission_query)
    return permission[0]["permission"]

# is value in table
def is_value_in_table(db, table, column, value, datatype):
    is_value_in_table_query_template = \
    """
    SELECT *
    FROM {table}
    WHERE {column} = {value}
    """
    is_value_in_table_query = is_value_in_table_query_template.format(
        table=table,
        column=column,
        value=V_ARG(datatype, value)
    )
    result = db.execute_query(is_value_in_table_query)
    breakpoint();
    if result is None:
        return jsonify({
            "status": 'error',
            "message": "Internal error"
        }), 500
    if len(result) > 0:
        return True
    return False

if __name__ == "__main__":
    # config_file = "config/dummy_config.json"
    # db = DB(config_file)
    # db.connect()

    """
    -- flight table
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
    AND {arrival_time}
    ;
    """
    query = query_tempate.format(
        table = "flight",
        airline_name = KV_ARG("airline_name", "string", "Delta"),
        price = KV_ARG("price", "number", (100, 200)),
        status = KV_ARG("status", "string", None),
        dept_airport_name = KV_ARG("dept_airport_name", "string", ("PVG", "JFK", "LAX")), 
        arrival_time = KV_ARG("arrival_time", "datetime", ("2020-01-02 10:23", "2020-01-02 11"))
    )
    print(query)

    # result = db.execute_query(query)
    #
    # if result:
    #     for row in result:
    #         print(row)
    #
    # db.disconnect()

