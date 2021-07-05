from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.product import Product, ProductList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserList



# just setting database and app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db/'
app.config['SQLALCEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Tarek'
api = Api(app)

jwt = JWT(app, authentication, identity)


# creating the tables
@app.before_first_request
def create_table():
    database.create_all()




api.add_resource(UserRegister, "/register")
api.add_resource(Product, "/product/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(UserList, "/users")
api.add_resource(ProductList, "/products")
api.add_resource(StoreList, "/stores")


if __name__ == '__main__':
    from database import database
    database.init_app(app)
    app.run(port=5000, debug=True)
