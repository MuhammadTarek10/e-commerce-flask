from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
#from resources.product import Product
#from resources.store import Store
from resources.user import UserRegister



# just setting database and app
app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db/'
app.config['SQLAlCHEMY_TRACH_MODIFICATIONS'] = False
app.secret_key = 'Tarek'
api = Api(app)

jwt = JWT(app, authentication, identity)


# creating the table
@app.before_first_request
def create_table():
    database.create_all()




api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    from database import database
    database.init_app(app)
    app.run(port=5000, debug=True)
