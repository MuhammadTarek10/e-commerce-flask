import os
import re
from werkzeug.datastructures import FileStorage 

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)

def save_image(image, folder, name=None):
	return IMAGE_SET.save(image, folder, name)

def get_path(filename, folder):
	return IMAGE_SET.path(filename, folder)

def find_image_any_format(filename, folder):
	for _format in IMAGES:
		image = f"{filename}.{_format}"
		image_path = IMAGE_SET.path(filenmae=image, folder=folder)
		if os.path.isfile(image_path):
			return image_path
	return None

def _retrieve_filename(file):
	if isinstance(file, FileStorage):
		return file.filename
	return file

def is_filename_safe(file):
	filename = _retrieve_filename(file)
	allowed_format = "|".join(IMAGES)
	regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
	return re.match(regex, filename) is not None

def get_basename(file):
	filename = _retrieve_filename(file)
	return os.path.split(filename)[1]

def get_extension(file):
	filename = _retrieve_filename(file)
	return os.path.splitext(filename)[1]