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


def is_logged_in():
    if 'user' in session:
        return True
    return False

