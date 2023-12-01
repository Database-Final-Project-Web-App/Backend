def TODO(text=""):
	assert("TODO: {}".format(text))

COOKIE_MAX_AGE = 100000000

# define constant of logintype
class LOGINTYPE:
	CUSTOMER = 'customer'
	BOOKING_AGENT = 'booking_agent'
	AIRLINE_STAFF = 'airline_staff'

	# check if logintype is valid
	@staticmethod
	def is_valid(logintype):
		if logintype is None:
			return 
		return logintype in [LOGINTYPE.CUSTOMER, LOGINTYPE.BOOKING_AGENT, LOGINTYPE.AIRLINE_STAFF]


COMMISION_RATE = 0.1