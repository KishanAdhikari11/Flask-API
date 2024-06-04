from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
import os

dbname=os.getenv("dbname")
dbpassword=os.getenv("dbpassword")
dbusername=os.getenv("dbusername")
dbhost=os.getenv("dbhost")

print(dbpassword)
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY","secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{dbusername}:{dbpassword}@{dbhost}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
api = Api(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()


api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
