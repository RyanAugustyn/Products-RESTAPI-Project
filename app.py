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
    img_link=db.Column(db.String(255))

    def __repr__(self):
        return f'{self.name} {self.description} {self.price} {self.inventory_quantity} {self.img_link}'

# Schemas
class ProductSchema(ma.Schema):
    id=fields.Integer(primary_key=True)
    name=fields.String()
    description=fields.String()
    price=fields.Float()
    inventory_quantity=fields.Integer()
    img_link=fields.String()
    class Meta:
        fields = ("id", "name", "description", "price", "inventory_quantity", "img_link")
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
        try:
            incoming_data=request.get_json
            new_product=product_schema.load(incoming_data)
            db.session.add(new_product)
            db.session.commit()
            return product_schema.dump(new_product), 201
        except ValidationError as error:
            return error.messages, 400
    
class ProductResource(Resource):
    def get_by_id(self, product_id):
        product=Product.query.get_or_404(product_id)
        return product_schema.dump(product), 200
    def put(self, product_id):
        product=Product.query.get_or_404(product_id)
        if 'name' in request.json:
            product.name=request.json['name']
        if 'description' in request.json:
            product.description=request.json['description']
        if 'price' in request.json:
            product.price=request.json['price']
        if 'inventory_quantity' in request.json:
            product.inventory_quantity=request.json['inventory_quantity']
        if 'img_link' in request.json:
            product.img_Link=request.json['img_link']
        db.session.commit()
        return product_schema.dump(product)
    def delete(self, product_id):
        product=Product.query.get_or_404(product_id)
        db.session.delete(product)
        return '', 204

# Routes
api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:pk>')