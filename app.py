from flask import Flask
from flask_restful import Api
from flask_jwt import JWT



# just setting database and app
app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database/'
app.config['SQLAlCHEMY_TRACH_MODIFICATIONS'] = False
app.secret_key = 'Tarek'
api = Api(app)




# creating the table
@app.before_first_request
def create_table():
    database.create_all()







if __name__ == '__main__':
    from database import database
    database.init_app(app)
    app.run(port=5000, debug=True)
