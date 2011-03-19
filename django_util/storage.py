from cStringIO import StringIO
from levitypysland.lib.s3storage import S3Storage
from levitypysland.util import image
from levitypysland.util.text import trim_extension
from PIL import Image, ImageOps

class ImageS3Storage(S3Storage):
	def __init__(self, thumbnails={}, max_size=None):
		"""thumbnails: keys are human-readable names like "small" & "medium"; values are (width, height) tuples.
		max_size: (width, height) tuple (defaults to None). if content exceeds max size, it will be resized.
		"""
		self.thumbnail_sizes = thumbnails
		self.max_size = max_size
		super(ImageS3Storage, self).__init__()
	
	def thumbnail_name(self, size, name):
		width, height = self.thumbnail_sizes[size]
		return '%s_t%dx%d.jpg' % (trim_extension(name), width, height)
	
	def thumbnail_url(self, size, name):
		return self.url(self.thumbnail_name(size, name))
	
	def delete(self, name):
		super(ImageS3Storage, self).delete(name)
		for size in self.thumbnail_sizes.keys():
			thumbnail_name = self.thumbnail_name(size, name)
			if self.exists(thumbnail_name):
				super(ImageS3Storage, self).delete(thumbnail_name)
	
	def content_string(self, content):
		content.open()
		if hasattr(content, 'chunks'):
			content_str = ''.join(chunk for chunk in content.chunks())
		else:
			content_str = content.read()
		return content_str
	
	def _save(self, name, content, thumbnails_only=False):
		content_str = self.content_string(content)
		in_buffer = StringIO()
		in_buffer.write(content_str)
		in_buffer.seek(0)
		img = Image.open(in_buffer)
		
		# first resize the main image if necessary
		if not thumbnails_only:
			if self.max_size and (img.size[0] > self.max_size[0] or img.size[1] > self.max_size[1]):
				resized = ImageOps.fit(img, image.scale_to_fit(img.size, self.max_size), Image.ANTIALIAS)
				out_buffer = StringIO()
				image_type = image.image_type(name)
				args, kwargs = [out_buffer, image_type], {}
				if image_type == 'JPEG': kwargs['quality'] = 95
				resized.save(*args, **kwargs)
				self._put_file(name, out_buffer.getvalue())
				out_buffer.close()
			else:
				self._put_file(name, content_str)
		
		# now create each of the thumbnails
		for size in self.thumbnail_sizes.keys():
			resized = ImageOps.fit(img, self.thumbnail_sizes[size], Image.ANTIALIAS)
			out_buffer = StringIO()
			resized.convert('RGB').save(out_buffer, 'JPEG', quality=95)
			self._put_file(self.thumbnail_name(size, name), out_buffer.getvalue())
			out_buffer.close()

		in_buffer.close()		
		return name
		
	

