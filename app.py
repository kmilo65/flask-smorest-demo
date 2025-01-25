from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
import os
from db import db
import models # to allow easy access to all models. Models need to be imported to be registered with the database
from pathlib import Path


# Factory pattern
def create_app(db_url=None):
    
    app = Flask(__name__,instance_relative_config=True) # Create the app
    '''
        `instance_relative_config=True` tells the app that the configuration files are in the instance folder
    '''

    app.config["PROPAGATE_EXCEPTIONS"] = True # propagate exceptions to the app
    app.config["API_TITLE"] = "Store REST API whit Flask-Smorest"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/" # This is the root of the API
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # This is the path to the Swagger UI
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # This is the URL where the Swagger UI is hosted
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = (
    db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    
    )# db_url || (Data base according to ENV || SQLite )
    """
     - `db_url`: Optional parameter for overriding the database configuration.
     - Default: SQLite database in the `instance/data.db` file due to `sqlite:///data.db` 
    """
    # Avoid SQLAlchemy warnings
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
    
    # Path to the file
    file_path = "instance/data.db"
  
     # Initialize the database with the app (initialize extensions)
    db.init_app(app)

    # Initialize the API with the app
    api=Api(app)
    
    
    # Check if the database file exists
    db_file = Path(app.instance_path) / "data.db"
    if not db_file.is_file():
            # Ensure the file is created
            with app.app_context():
                db.create_all()


    # Register blueprints
    api.register_blueprint(StoreBlueprint) # Register the StoreBlueprint
    api.register_blueprint(ItemBlueprint)  # Register the ItemBlueprint

    return app

