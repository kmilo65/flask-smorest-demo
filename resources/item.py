from flask.views import MethodView # a flask class that allows us to define methods for different HTTP methods
from flask_smorest import Blueprint, abort
from models import ItemModel # importing the ItemModel class from models
from schemas import ItemSchema, ItemUpdateSchema # importing marshmallow schemas for validation and serialization
from sqlalchemy.exc import SQLAlchemyError # Import the SQLAlchemy error class
from db import db
from flask_jwt_extended import jwt_required, get_jwt


# create a blue print
blp = Blueprint(
    "Items",            # name of the blueprint 
    __name__,           # module where the blueprint is located
    description="Operations on items" # description for API documentation
)

# Defining routes in the blueprint
# The route decorator is used to define a route in the blueprint
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)  # response schema
    def get(self, item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema) # Input validation schema. The order of decorators is important. Deeper goes first
    @blp.response(200, ItemSchema)
    def put(self,item_data,item_id):
        # Find the existing item by its identifier (e.g., primary key)
        item=ItemModel.query.get(item_id)
        if item:
            #Update the files of the existing item with the new data
            # Dynamically update fields
            for key, value in item_data.items():
                setattr(item, key, value)
        else:
            item=ItemModel(**item)
            db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema) #
    def post(self, item_data):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="Admin privilege required.")
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Could not save item to database.") 

        return item 
