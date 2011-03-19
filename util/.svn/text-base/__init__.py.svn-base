import logging
from logging.handlers import SMTPHandler
import random

RANDOM_CHAR_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def random_chars(length):
	return ''.join(RANDOM_CHAR_SET[int(random.random()*len(RANDOM_CHAR_SET))] for i in range(length))
	
_emailLogger = None

def getEmailLogger(toaddrs, name='levityisland', loglevel=logging.DEBUG):
	global _emailLogger
	if not _emailLogger:
		smtpHandler = SMTPHandler('localhost','logging@levityisland.com', toaddrs, '[LI] Log message')
		smtpHandler.setLevel(loglevel)
		smtpHandler.setFormatter(logging.Formatter("%(levelname)s %(asctime)s : %(message)s"))

		_emailLogger = logging.getLogger(name)
		_emailLogger.setLevel(loglevel)
		_emailLogger.addHandler(smtpHandler)

	return _emailLogger
