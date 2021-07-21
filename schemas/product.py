from ma import ma
from models.product import ProductModel
from models.order import OrderModel
from schemas.rate_to_product import RateToProductSchema
from schemas.order import OrderSchema

class ProdcutSchema(ma.SQLAlchemyAutoSchema):
	rate_to_product = ma.Nested(RateToProductSchema, many=True)
	order = ma.Nested(OrderSchema, many=True)
	class Meta:
		model = ProductModel
		dump_only = ("id", )
		include_fk = True
