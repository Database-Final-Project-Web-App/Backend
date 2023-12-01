def TODO(text=""):
	assert("TODO: {}".format(text))

# define constant of logintype
class LOGINTYPE:
	CUSTOMER = 'customer'
	BOOKING_AGENT = 'booking_agent'
	AIRLINE_STAFF = 'airline_staff'

	# check if logintype is valid
	@staticmethod
	def is_valid(logintype):
		return logintype in [LOGINTYPE.CUSTOMER, LOGINTYPE.BOOKING_AGENT, LOGINTYPE.AIRLINE_STAFF]

COOKIE_MAX_AGE = 100000000