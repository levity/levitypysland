from django.http import HttpResponse
from functools import wraps


def post_required(view_func):
	@wraps(view_func)
	def fn(request, *args, **kwargs):
		if request.POST:
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponse('This URL only responds to POST requests')
	return fn
