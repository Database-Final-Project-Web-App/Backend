from flask import session

# define constant of logintype
class LOGINTYPE:
	CUSTOMER = 'customer'
	BOOKING_AGENT = 'booking_agent'
	AIRLINE_STAFF = 'airline_staff'

	# check if logintype is valid
	@staticmethod
	def is_valid(logintype):
		return logintype in [LOGINTYPE.CUSTOMER, LOGINTYPE.BOOKING_AGENT, LOGINTYPE.AIRLINE_STAFF]

# define constant for staff permission
class PERMISSION:
	ADMIN = 'Admin'
	OPERATOR = 'Operator'
	NORMAL = 'Normal'
	
	# check if permission is valid
	@staticmethod
	def is_valid(permission):
		return permission in [PERMISSION.ADMIN, PERMISSION.OPERATOR, PERMISSION.NORMAL]
	
def is_logged_in():
	if 'user' in session:
		return True
	return False

