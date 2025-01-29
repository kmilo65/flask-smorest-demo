import uuid
from flask.views import MethodView # a flask class that allows us to define methods for different HTTP methods
from flask_smorest import Blueprint, abort
from models import UserModel # importing the ItemModel class from models
from schemas import UserSchema # importing marshmallow schemas for validation and serialization
from sqlalchemy.exc import SQLAlchemyError # Import the SQLAlchemy error class
from db import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt,create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST



# create a blue print
blp = Blueprint(
    "Users",            # name of the blueprint 
    __name__,           # module where the blueprint is located
    description="Operations on Users" # description for API documentation
)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema) # Input validation schema. The order of decorators is important. Deeper goes first
    def post(self,user_data):
        userModel=UserModel(**user_data)
        
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,message="A user with that username already exists.!!")
        
        user=UserModel(
            username=userModel.username,
            password=pbkdf2_sha256.hash(userModel.password)      
        )
        
        db.session.add(user)
        db.session.commit()    
        
        return {"message":"User created successfully"}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):     
        user=UserModel.query.filter(
            UserModel.username==user_data["username"]
        ).first()
        # Validating user exists
        if not user:
            abort(404,message="A user with that username does not exists.!!")     
        # Validating entering password 
        if pbkdf2_sha256.verify(user_data["password"],user.password):
            # create token for user
            access_token=create_access_token(identity=user.username,fresh=True)
            refresh_token=create_refresh_token(identity=user.username)
            return {"token": access_token,"refresh_token":refresh_token},200
        else:
            abort(401,message="Invalid password")
        
        
    
@blp.route("/user/<int:user_id>")    
class User(MethodView):
    @blp.response(200,UserSchema)
    def get (self, user_id):
        user=UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"},200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_refresh_token(identity=current_user,fresh=False)
        # if only one refresh token use the code below
        # jti=get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"access_token":new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out."}   
    