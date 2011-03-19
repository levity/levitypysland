from cStringIO import StringIO
from PIL import ImageOps, Image

def create_thumbnail(image_field, width, height, output_type='JPEG'):
	# in_buffer and out_buffer are necessary because PIL uses parts of the file API that
	# Django's ImageFieldFile does not support.
	in_buffer = StringIO()
	in_buffer.write(image_field.read())
	in_buffer.seek(0)
	thumb = ImageOps.fit(Image.open(in_buffer), (width, height), Image.ANTIALIAS)
	out_buffer = StringIO()
	thumb.save(out_buffer, output_type)
	return out_buffer.getvalue()
