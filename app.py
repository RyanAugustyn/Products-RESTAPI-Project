from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    price=db.Column(db.Float)
    inventory_quantity=db.Column(db.Integer)



# Schemas
class ProductSchema(ma.Schema):
    #id=fields.Integer(primary_key=True)
    pass


# Resources
class ProductListResource(Resource):
    def get(self):
        all_products=Product.query.all()


class ProductResource(Resource):
    pass


# Routes
api.add_resource(ProductListResource, 'api/products')
api.add_resource(ProductResource, 'api/products/<int:pk>')