from django import forms
from django.core.files.uploadhandler import FileUploadHandler, StopUpload
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.encoding import force_unicode


def render_response(req, *args, **kwargs):
	"render_to_response, with RequestContext included by default"
	kwargs['context_instance'] = RequestContext(req)
	return render_to_response(*args, **kwargs)


def json_response(data):
	return HttpResponse(simplejson.dumps(data), mimetype="text/plain")


def compressed_form_errors(form):
	return ' '.join([' '.join([unicode(v) for v in l]) for l in form.errors.values()])


def anon_messages(request):
	"""context processor that sets "anon_messages" in the context to be the
	contents of request.session['anon_messages']. like request.user.message_set
	for anonymous users.
	"""
	context = {}
	if 'anon_messages' in request.session:
		messages = request.session['anon_messages']
		del request.session['anon_messages']
		context['anon_messages'] = messages
	return context


def create_anon_message(message, request):
	if 'anon_messages' not in request.session:
		request.session['anon_messages'] = []
	request.session['anon_messages'].append(message)


class PresetModelForm(forms.ModelForm):
	"""a model form that pre-sets some attributes of the instances it
	creates/edits based on the "presets" constructor parameter, which is
	a dictionary.
	
	doesn't work quite right with GenericForeignKey. you have to specify
	the content_type and object_id rather than the content_object, because
	setattr() doesn't call GenericForeignKey.__set__() so things don't
	get set up right.
	"""
	def __init__(self, *args, **kwargs):
		self.presets = kwargs.pop('presets')
		super(PresetModelForm, self).__init__(*args, **kwargs)
	
	def save(self, commit=True):
		for name, value in self.presets.items():
			setattr(self.instance, name, value)
		item = super(PresetModelForm, self).save(commit=False)
		if commit:
			item.save()
			if hasattr(self, 'save_m2m'):
				self.save_m2m()
		return item


class SizeLimitUploadHandler(FileUploadHandler):
	"""an upload handler that aborts the upload if the number of bytes received
	exceeds a set limit."""
	def __init__(self, *args, **kwargs):
		self.max_kbytes = kwargs.pop('max_kbytes')
		self.kbytes_read = 0
		self.successful, self.started, self.canceled = False, False, False
		super(SizeLimitUploadHandler, self).__init__(*args, **kwargs)
	
	def new_file(self, field_name, file_name, content_type, content_length, charset):
		super(SizeLimitUploadHandler, self).new_file(field_name, file_name, content_type, content_length, charset)
		self.started = True
	
	def receive_data_chunk(self, raw_data, start):
		self.kbytes_read += len(raw_data) / 1024
		if self.kbytes_read > self.max_kbytes:
			self.canceled = True
			raise StopUpload(connection_reset=True)
		return raw_data
	
	def file_complete(self, file_size):
		self.successful = True
		return None


class RadioFieldListRenderer(forms.widgets.RadioFieldRenderer):
	"""Use this renderer with a RadioSelect if you want to place radio buttons
	individually rather than all at once. In the template, place them like this:
		{{ form.field_name.as_widget.0 }}
		{{ form.field_name.as_widget.1 }} ...
	where the numbers are indices in the field's list of choices.
	
	The widgets will still display their original labels, so give them blank
	labels when defining the choices list if you want to specify your own.
	"""
	def render(self):
		"""Outputs a list for this set of radio fields."""
		return [force_unicode(w) for w in self]


def get_session_from_id(session_id):
	"given a django session id, e.g. from a server error email, get the session object."
	import base64, cPickle
	from django.contrib.sessions.models import Session
	from django.contrib.auth.models import User
	data = cPickle.loads(base64.decodestring(Session.objects.get(session_key=session_id).session_data)[:-32])
	return data, User.objects.get(pk=data['_auth_user_id'])


def notify_admins(subject, message):
	from django.core.mail import send_mail
	from django.conf import settings
	send_mail(subject, message, 'django@levityisland.com', [a[1] for a in settings.ADMINS])

	