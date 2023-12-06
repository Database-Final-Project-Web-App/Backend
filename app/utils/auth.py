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
	
	@staticmethod
	def is_equal(logintype1, login_type2):
		if not isinstance(logintype1, str) or not isinstance(login_type2, str):
			return False
		return logintype1.lower() == login_type2.lower()

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
	
	@staticmethod
	def is_equal(permission1, permission2):
		if permission1 is None and permission2 is None:
			return True
		if not isinstance(permission1, str) or not isinstance(permission2, str):
			return False
		return permission1.lower() == permission2.lower()
	
	@staticmethod
	def is_in(item, li):
		if item is None:
			return True
		if not isinstance(item, str):
			return False
		for i in li:
			if PERMISSION.is_equal(item, i):
				return True
		return False

def is_logged_in():
	if 'user' in session:
		return True
	return False

