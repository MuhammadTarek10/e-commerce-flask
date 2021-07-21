from marshmallow import Schema, fields

class ProductSchema(Schema):
	class Meta:
		load_only = ("id", )
		dump_only = ("name", )

	id = fields.Int()
	name = fields.Str()
	description = fields.Str()
	price = fields.Float(required=True)
	store_id = fields.Int(required=True)
	genre = fields.Str(required=True)
	available = fields.Bool(required=True)