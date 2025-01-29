from flask import jsonify
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST


jwt = JWTManager()  # Create the JWTManager instance

@jwt.expired_token_loader
def expired_token_callback(lwt_header,jwt_payload):
    return (
            jsonify({"message":"The token has expired.","error":"token_expired"}),401
        )
    
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
            jsonify(
                {"message":"Signature verification failed.","error":"invalid_token"},401
            )
            
    )
    
@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
            jsonify(
                {
                    "description":"Request does not contain an access token",
                    "error":"authorization_required"
                }
            ),401
    )
    
    
# Function to add custom claims
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    """Add custom claims based on user identity"""
    if identity == "admin":
        return {"role": "admin", "permissions": ["read", "write", "delete"]}
    return {"role": "user", "permissions": ["read"]}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header,jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_callck(jwt_header,jwt_payload):
    return(
        jsonify(
            {"description":"The token has been revoked","error":"token_revoked"}
        ),
        401
        
    )
    
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header,jwt_payload):
    return (
        
        jsonify(
            {
                "description":"The token is not fresh.",
                "error":"fresh_token_required"
            }
        )
        
    )