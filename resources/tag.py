import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, StoreModel, ItemModel

from schemas import TagSchema, TagAndItemSchema

blp=Blueprint("Tags",__name__,description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(cls,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()
        
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(cls,store_id,tag_data):
        if TagModel.query.filter_by(name=tag_data["name"],store_id=store_id).first():
            abort(400,message="Tag already exists in store")
        tag=TagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )
        return tag
    
    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(cls,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
 
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagAndItem(MethodView):
    @blp.response(200,TagAndItemSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)
        try:
            db.session.commit()
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
            
        return tag
    
    # unlinking an item from a tag
    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        item.tags.remove(tag)
        try:
            db.session.commit()
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
            
        return {"message":"Item removed from Tag", "item":item,"tag":tag}
        
    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(cls,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202,
        description="Delete a tag if not item is tagged with it",
        example={"message":"Tag deleted successfully"}
        
    )
    @blp.alt_response(404,description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if there are items tagged with the tag. In this case, the tag is not deleted"
    )
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id) 
        '''
        if tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted successfully"}
        '''
        
        try: 
            db.session.delete(tag)
            db.session.commit()
        except IntegrityError:
            abort(400,message="Tag is linked to an item")
            
        return {"message":"Tag deleted successfully"}
    