from ma import ma
from models.store import StoreModel
from models.owner import OwnerModel
from schemas.product import ProductSchema

class StoreSchema(ma.SQLAlchemyAutoSchema):
	products = ma.Nested(ProductSchema, many=True)
	class Meta:
		include_fk = True