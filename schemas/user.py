from marshmallow import Schema, fields

class UserSchema(Schema):
	class Meta:
		load_only = ("password", "last_name")
		dump_only = ("id", )
	id = fields.Int()
	first_name = fields.Str(required=True)
	last_name = fields.Str(required=True)
	username = fields.Str(required=True)
	password = fields.Str(required=True)
	email = fields.Str(required=True)

