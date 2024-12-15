from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()

def init_extensions(app):
    """Initialize all extensions for the Flask application"""
    try:
        # Get MongoDB URI
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/vipani_db')
        db_name = os.getenv('MONGO_DBNAME', 'vipani')
        
        # Set configuration
        app.config['MONGO_URI'] = mongo_uri
        app.config['MONGO_DBNAME'] = db_name
        
        # Create direct client for debugging
        client = MongoClient(mongo_uri)
        db = client[db_name]
        
        # Ensure users collection exists
        if 'userdatas' not in db.list_collection_names():
            db.create_collection('userdatas')
            print("Created 'users' collection")
        
        # Print available collections
        print("Available collections:", db.list_collection_names())
        
        # Initialize PyMongo
        mongo.init_app(app)
        
        # Initialize other extensions
        bcrypt.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)
        
    except Exception as e:
        print(f"MongoDB initialization error: {e}")
        raise