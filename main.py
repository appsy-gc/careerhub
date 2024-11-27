# Import packages
import os
from flask import Flask, render_template
from flask_cors import CORS

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
from controllers.cpartner_controller import partners_bp

# Import blueprint from cpartners_controller

def create_app():
    # Initialise
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    print("Server started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Stop flask from ordering data
    app.json.sort_keys = False

    # Initialise SQLAlcemy
    db.init_app(app)
    # Initialise Marshmallow
    ma.init_app(app)
    # Register CLI Controller
    app.register_blueprint(db_commands)
    # Register cpartners controller
    app.register_blueprint(partners_bp)

    # Add a route for the front-end
    @app.route("/")
    def index():
        return render_template("index.html")
    
    # Route for data page
    @app.route("/database")
    def database():
        return render_template("database.html")

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default to 5000
    app.run(host="0.0.0.0", port=port)