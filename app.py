from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
# from resources.product import Product, ProductList, ProductGenre, ProductPrice
# from resources.store import Store, StoreList
from resources.user import UserRegister, UserList, User
from resources.owner import OwnerRegister, OwnerList
# from resources.rate_to_product import RateToPoduct
# from resources.rate_to_owner import RateToOwner
# from resources.order import Order
from ma import ma
 
# just setting database and app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db/"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Tarek"
api = Api(app)

jwt = JWT(app, authentication, identity)


# creating the tables
@app.before_first_request
def create_table():
    database.create_all()


api.add_resource(UserRegister, "/user/register")
api.add_resource(UserList, "/users")
api.add_resource(OwnerRegister, "/owner/register")
api.add_resource(OwnerList, "/owners")
# api.add_resource(Product, "/product/<string:name>")
# api.add_resource(ProductList, "/products")
# api.add_resource(ProductGenre, "/genre/<string:genre>")
# api.add_resource(ProductPrice, "/price/<float:price>")
# api.add_resource(Store, "/store/<string:name>")
# api.add_resource(StoreList, "/stores")
# api.add_resource(RateToPoduct, "/rate_product/<float:rate>")
# api.add_resource(RateToOwner, "/rate_owner/<float:rate>")
# api.add_resource(Order, "/order")
api.add_resource(User, "/user/<int:user_id>")



if __name__ == "__main__":
    from database import database

    database.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
