import datetime
from django.db import models

class BigIntegerField(models.IntegerField):
	empty_strings_allowed = False
	def get_internal_type(self):
		return "BigIntegerField"
	def db_type(self):
		return 'bigint'


class DatedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	edited = models.DateTimeField(editable=False)
	class Meta:
		abstract = True
	def save(self, force_insert=False, force_update=False, preserve_edit_time=False):
		if not preserve_edit_time:
			self.edited = datetime.datetime.now()
		return super(DatedModel, self).save(force_insert=force_insert, force_update=force_update)


