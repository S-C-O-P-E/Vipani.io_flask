from flask import Flask
from .config import DevelopmentConfig
from .extensions import init_extensions

def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_extensions(app)
    
    # Import and register blueprints
    from .routes.user_routes import user_bp
    from .routes.product_routes import product_bp
    from .routes.admin_routes import admin_bp

    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    # app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(product_bp, url_prefix='/api/v1/product')

    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    
    return app