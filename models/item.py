from db import db

class ItemModel(db.Model):
    __tablename__ = "items" # This is the name of the table in the database

    # columns in the table
    id = db.Column(db.Integer, primary_key=True) # autoincrementing primary key
    name = db.Column(db.String(80),unique=True, nullable=False) # unique name and not null
    price = db.Column(db.Float(precision=2),unique=False, nullable=False) # price is not unique and not null
    store_id = db.Column(db.String(80), db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel",back_populates="items") # This is a reference to the StoreModel class

