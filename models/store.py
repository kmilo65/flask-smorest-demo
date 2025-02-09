from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # with cascade when delete a store, all the items in the store will be deleted as well
    items = db.relationship("ItemModel", back_populates="store",lazy="dynamic")
    tags=db.relationship("TagModel",back_populates="store",lazy="dynamic")
    

    


