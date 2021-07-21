from ma import ma
from models.owner import OwnerModel
from models.store import StoreModel
from schemas.store import StoreSchema
from schemas.rate_to_owner import RateToOwnerSchema


class OwnerSchema(ma.SQLAlchemyAutoSchema):
	rate_to_owner = ma.Nested(RateToOwnerSchema, many=True)
	stores = ma.Nested(StoreSchema, many=True)
	class Meta:
		load_only = ("id", "password", )
		include_fk = True