from ma import ma
from models.rate_to_owner import RateToOwnerModel

class RateToOwnerSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = RateToOwnerModel
		load_only = ("id", )
		include_fk = True