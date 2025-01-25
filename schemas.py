from marshmallow import Schema, fields


# Define schemas for serialization/deserialization and data validation

class PlainItemSchema(Schema):
    id = fields.Integer(dump_only=True) # output only field
    name = fields.String(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name= fields.String(required=True) 
    

class ItemUpdateSchema(Schema): # optional         
        name = fields.String() 
        price = fields.Float()
        

class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required=True)
    store= fields.Nested(PlainStoreSchema, dump_only=True) # nested serialization    
    
    
class StoreSchema(PlainStoreSchema):
    items = fields.Nested(PlainItemSchema, many=True, dump_only=True) # nested serialization