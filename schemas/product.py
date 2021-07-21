from ma import ma
from models.product import ProductModel

class ProdcutSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ProductModel
