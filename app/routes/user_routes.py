from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from ..controllers.user_controller import UserController
# from ..controllers.user_controller import register_user

# Create a blueprint for user-related routes
user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    """Welcome to Vipani.io!"""
    return "Welcome to  Vipani.io!"

@user_bp.route('/getuser', methods=['GET'])
def get_user_data():
    user_id = request.args.get('userid')
    user = UserController.get_user(user_id)
    return jsonify(user), 200















# @user_bp.route('/register', methods=['POST'])
# def register():
#     """User registration endpoint"""
#     data = request.get_json()
#     result = register_user(data)
#     return jsonify(result), 201

# @user_bp.route('/login', methods=['POST'])
# def login():
#     """User login endpoint"""
#     data = request.get_json()
#     result = login_user(data)
#     return jsonify(result), 200

# @user_bp.route('/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     """Get user profile (protected route)"""
#     # Implement profile retrieval logic
#     pass