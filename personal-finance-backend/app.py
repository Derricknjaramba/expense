from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config  # Make sure to import Config from config.py

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Use the Config class

    db.init_app(app)
    bcrypt.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register routes
    from routes import init_routes
    init_routes(app)

    return app

# Create app and run
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)











