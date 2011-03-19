from levitypysland.util.text import file_extension

def scale_to_fit(larger_size, target_size):
	divisor = max(float(larger_size[0]) / target_size[0], float(larger_size[1]) / target_size[1])
	return (larger_size[0] / divisor, larger_size[1] / divisor)


class UnsupportedImageFormat(Exception):
	pass


def image_type(filename):
	"""Given a filename, return its image type for passing into PIL."""
	extension = file_extension(filename).lower()
	if extension in ('jpg', 'jpeg'):
		return 'JPEG'
	if extension == 'gif':
		return 'GIF'
	if extension == 'png':
		return 'PNG'
	raise UnsupportedImageFormat()