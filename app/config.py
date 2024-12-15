import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/vipani_db')
    
    # JWT Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # Application Settings
    DEBUG = os.getenv('FLASK_DEBUG', True)
    TESTING = os.getenv('FLASK_TESTING', False)

    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_EXPIRES', 3600)  # 1 hour

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False