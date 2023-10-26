import pymysql 

# config
host = "localhost"
user = "root"
password = ""
database = "atrs"

# connect to database
connection = pymysql.connect(
	host=host,
	user=user,
	password=password,
	database=database
)

# execute query
with connection.cursor() as cursor:
	cursor.execute("SELECT * FROM flight;")
	result = cursor.fetchall()
	# result = cursor.fetchone()
	print(result)

# disconnect from database
connection.close()