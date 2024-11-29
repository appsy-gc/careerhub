# Import packages
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from dotenv import load_dotenv

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
from controllers.cpartner_controller import partners_bp

def create_app():
    # Initialise
    app = Flask(__name__)
    # Set the secret key from the .env file
    app.secret_key = os.getenv("SECRET_KEY")
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

    @app.context_processor
    def inject_user():
        # Inject `user_logged_in` into all templates
        return {"user_logged_in": "user" in session}

    # Add a route for the front-end
    @app.route("/")
    def index():
        return render_template("index.html")
    

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            # Example credentials (replace with database validation in production)
            if username == "admin" and password == "password123":
                session["user"] = username  # Save login state
                return redirect(url_for("index"))  # Redirect to the home page to refresh the header
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for("login"))

        return render_template("login.html")


    @app.route("/logout")
    def logout():
        session.pop("user", None)  # Remove login state
        return redirect(url_for("index"))
    

    # Route for data page
    @app.route("/database")
    def database():
        if "user" not in session:  # Check if user is logged in
            flash("You must be logged in to access this page.", "error")
            return redirect(url_for("login"))
        
        return render_template("database.html")

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default to 5000
    app.run(host="0.0.0.0", port=port)