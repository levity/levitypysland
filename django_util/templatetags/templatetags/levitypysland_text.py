from django import template
from django.utils.html import urlize
from django.utils.safestring import mark_safe
import datetime
import re
import time

register = template.Library()

@register.filter
def startswith(var, prefix):
	return var.startswith(prefix)


@register.filter
def short_date(date_val):
	seconds = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(date_val.timetuple())
	if seconds < 3600 * 12:
		return time.strftime('%I:%M', date_val.timetuple())
	return friendly_date(date_val)


@register.filter
def friendly_date(date_val):
	seconds = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(date_val.timetuple())
	if seconds < 60:
		return '%d second%s ago' % (seconds, 's' if seconds > 1 else '')
	elif seconds < 3600:
		minutes = int(seconds / 60)
		return '%d minute%s ago' % (minutes, 's' if minutes > 1 else '')
	elif seconds < 86400:
		hours = int(seconds / 3600)
		return '%d hour%s ago' % (hours, 's' if hours > 1 else '')
	elif seconds < 86400 * 14:
		days = int(seconds / 86400)
		return '%d day%s ago' % (days, 's' if days > 1 else '')
	elif seconds < 604800 * 8:
		weeks = int(seconds / 604800)
		return '%d week%s ago' % (weeks, 's' if weeks > 1 else '')
	elif seconds < 2592000 * 6:
		months = int(seconds / 2592000)
		return '%d month%s ago' % (months, 's' if months > 1 else '')
	else:
		return time.strftime('%Y-%m-%d', date_val.timetuple())


@register.filter
def ifappend(val, suffix):
	if val:
		return mark_safe(u'%s%s' % (val, suffix))
	return ''


@register.filter
def shorten(text, length):
	if len(text) > length:
		return text[:length-3] + '...'
	else:
		return text
