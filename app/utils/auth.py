from flask import session

# define constant of logintype
class LOGINTYPE:
	CUSTOMER = 'customer'
	BOOKING_AGENT = 'booking_agent'
	AIRLINE_STAFF = 'airline_staff'

	# check if logintype is valid
	@staticmethod
	def is_valid(logintype: str):
		if not isinstance(logintype, str):
			return False
		return logintype.lower() in [
			LOGINTYPE.CUSTOMER.lower(), 
			LOGINTYPE.BOOKING_AGENT.lower(), 
			LOGINTYPE.AIRLINE_STAFF.lower()
			]

# define constant for staff permission
class PERMISSION:
	ADMIN = 'Admin'
	OPERATOR = 'Operator'
	NORMAL = None
	
	# check if permission is valid
	@staticmethod
	def is_valid(permission: str):
		if not isinstance(permission, str):
			# None is valid, it's the permission of normal staff
			if permission is None:
				return True
			return False
		return permission.lower() in [
			PERMISSION.ADMIN.lower(), 
			PERMISSION.OPERATOR.lower(), 
			None,
			]
	
def is_logged_in():
	if 'user' in session:
		return True
	return False

