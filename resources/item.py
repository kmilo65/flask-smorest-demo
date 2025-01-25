
import uuid
from flask.views import MethodView # a flask class that allows us to define methods for different HTTP methods
from flask_smorest import Blueprint, abort
from models import ItemModel # importing the ItemModel class from models
from schemas import ItemSchema, ItemUpdateSchema # importing marshmallow schemas for validation and serialization
from sqlalchemy.exc import SQLAlchemyError # Import the SQLAlchemy error class
from db import db

# create a blue print
blp = Blueprint(
    "Items",            # name of the blueprint 
    __name__,           # module where the blueprint is located
    description="Operations on items" # description for API documentation
)

# Defining routes in the blueprint
# The route decorator is used to define a route in the blueprint
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)  # response schema
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema) # Input vdlidatino schema. The order of decorators is important. Deeper goes first
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema) #
    def post(self, item_data):
        item=ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Could not save item to database.") 

        return item 
