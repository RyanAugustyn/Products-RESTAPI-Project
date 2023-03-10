from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from marshmallow import post_load, fields, ValidationError
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
    id=fields.Integer(primary_key=True)
    name=fields.String()
    description=fields.String()
    price=fields.Float()
    inventory_qualtity=fields.Integer()
    class Meta:
        fields = ("id", "name", "description", "price", "inventory_quantity")
    @post_load
    def create_product(self, data, **kwargs):
        return Product(**data)

product_schema=ProductSchema()
products_schema=ProductSchema(many=True)    

# Resources
class ProductListResource(Resource):
    def get(self):
        all_products=Product.query.all()
        return products_schema.dump(all_products), 200
    def post(self):
        form_data=request.get_json


class ProductResource(Resource):
    def get_by_id(self, product_id):
        product=Product.query.get_or_404(product_id)
        return product_schema.dump(product), 200


# Routes
api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:pk>')