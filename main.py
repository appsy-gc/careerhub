# Import packages
import os
from flask import Flask

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller

# Import blueprint from cpartners_controller

def create_app():
    # Initialise
    app = Flask(__name__)

    print("Server started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQLAlcemy
    db.init_app(app)
    # Initialise Marshmallow
    ma.init_app(app)

    # Register CLI Controller

    # Register cpartners controller


    return app