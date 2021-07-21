from ma import ma
from models.rate_to_product import RateToProductModel


class RateToProductSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = RateToProductModel
		load_only = ("id", )
		include_fk = True