# import package
import africastalking


# Initialize SDK
username = "notifygrace"    # use 'sandbox' for development in the test environment
api_key = "14dcc0e2209e0909ab03e60f1262adb41413e213b096d4e83707f0c5b018f36b"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

def Sendmessage(message,numbers):
	africastalking.initialize(username, api_key)
	# Initialize a service
	sms = africastalking.SMS

	response = sms.send(message, numbers)
	return response