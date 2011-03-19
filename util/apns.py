from APNSWrapper import APNSNotificationWrapper, APNSNotification, APNSAlert, APNSProperty
from binascii import unhexlify

# to create PEM files from Apple-provided certs: 
#	openssl pkcs12 -in devPush.p12 -out devPush.pem -nodes -clcerts

def send_alert(alert_text, token, cert, isDev=False, extra_args=[]):
	wrapper = APNSNotificationWrapper(cert, isDev)
	message = create_message(token, alert_text, extra_args=extra_args)
	wrapper.append(message)
	wrapper.notify()


def send_messages(messages, cert, isDev=False):
	wrapper = APNSNotificationWrapper(cert, isDev)
	for message in messages:
		wrapper.append(message)
	wrapper.notify()


def create_message(token, alert_text=None, sound=True, badge=0, extra_args=[]):
	message = APNSNotification()
	
	if alert_text:
		alert = APNSAlert()
		alert.body(alert_text)	
		message.alert(alert)
	
	for name, val in extra_args:
		message.appendProperty(APNSProperty(name, val))
	
	message.token(unhexlify(token.replace(' ', '')))
	message.badge(badge)
	if sound:
		message.sound()
		
	return message


if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-d','--dev', help="use development service", default=False, action="store_true", dest='isDev')
	parser.add_option('-t','--token', help="the recipient's device token", dest='token')
	parser.add_option('-f','--file', help="a file containing the recipient's device token", dest='tokenfile')
	parser.add_option('-e','--extra', help="extra arguments, e.g.: foo=bar,baz=1. will auto-cast numerical values", dest='extra_args')
	options, args = parser.parse_args()
	
	if not options.token:
		if not options.tokenfile:
			raise Exception("You must specify the recipient's token with either -t or -f")
		else:
			token = open(options.tokenfile).read().strip()
	else:
		token = options.token
	
	extra_args = []
	if options.extra_args:
		for pair in options.extra_args.split(','):
			key, value = pair.split('=')
			try:
				new_value = int(value)
				if new_value != value:
					new_value = float(value)
			except ValueError:
				new_value = value
			extra_args.append((key, value))
		
	if len(args) != 2:
		raise Exception('Incorrect number of positional arguments (expecting: certificate file, message)')
	send_alert(args[1], token, args[0], options.isDev, extra_args)

