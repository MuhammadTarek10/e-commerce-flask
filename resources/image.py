import os

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()


class Image(Resource):
	def get(self, filename):
		user_id = 1
		folder = f"user_{user_id}"
		if not image_helper.is_filename_safe(filename):
			return {"message": "illegal filename"}

		try:
			return send_file(image_helper.get_path(filename, folder=folder))
		except FileNotFoundError:
			return {"message": f"image {filename} not found"}


	def delete(self, filename):
		user_id = 1
		folder = f"user_{user_id}"

		if not image_helper.is_filename_safe(filename):
			return {"message": "illegal filename"}

		try:
			os.remove(image_helper.get_path(filename, folder=folder))
			return {"message": f"image {filename} deleted"}
		except FileNotFoundError:
			return {"message": f"image {filename} not found"}
		except:
			return {"message": "delete faild"}


class ImageUpload(Resource):
	def post(self):
		data = image_schema.load(request.files)
		user_id = 1
		folder = f"user_{user_id}"
		print(data['image'])
		try:
			image_path = image_helper.save_image(data['image'], folder=folder)
			basename = image_helper.get_basename(image_path)
			return {"message": f"image uploaded, basename: {basename}"}
		except UploadNotAllowed:
			extension = image_helper.get_extension(data['image'])
			return {"message": f"extension {extension} is not allowed"}