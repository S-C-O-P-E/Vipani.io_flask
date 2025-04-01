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

@user_bp.route('/getallproducers', methods=['GET'])
def get_all_producers():
    """Get all producers endpoint"""
    result = UserController.get_all_producers()
    return jsonify(result)

@user_bp.route('/getuser', methods=['GET'])
def get_user_data():
    user_id = request.args.get('userid')
    user = UserController.get_user(user_id)
    return jsonify(user), 200

@user_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    #print("Registering user with mobile number:", type(data.get('mobile')))
    result = UserController.login_user(data)
    return jsonify(result)

@user_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    result = UserController.register_user(data)
    return jsonify(result)


@user_bp.route('/update-profile', methods=['PATCH'])
def update_profile():
    """Update user profile endpoint"""
    mobile = request.args.get('mobile')
    mobile = int(mobile)
    data = request.get_json()
    result = UserController.update_profile(mobile, data)
    return jsonify(result)

@user_bp.route('/update-producer', methods=['PATCH'])
def update_producer():
    """API endpoint to update the producer of a product"""
    mobile = request.args.get("mobile")
    producer_data = request.form.to_dict()
    file = request.files.get("dp")
    response, status = UserController.update_producer(mobile, producer_data, file)
    return jsonify(response), status

@user_bp.route('/update-location', methods=['PATCH'])
def update_location():
    """Update user location endpoint"""
    mobile = request.args.get('mobile')
    mobile = int(mobile)
    data = request.get_json()
    result = UserController.update_location(mobile,data)
    return jsonify(result)


@user_bp.route('/following', methods=['POST'])
def follow():
    """Follow a user endpoint"""
    data = request.get_json()
    result = UserController.follow_user(data)
    return jsonify(result)

@user_bp.route('/unfollow', methods=['POST'])
def unfollow():
    """Unfollow a user endpoint"""
    data = request.get_json()
    result = UserController.unfollow_user(data)
    return jsonify(result)


@user_bp.route('/create-order', methods=['POST'])
def create_order():
    """Create an order endpoint"""
    mobile = request.args.get('mobile')
    mobile = int(mobile)
    productId = request.get_json()
    result = UserController.create_order(mobile,productId)
    return jsonify(result)


@user_bp.route('/update-payment-status', methods=['PATCH'])
def update_payment_status():
    """Update payment status endpoint"""
    mobile = request.args.get('mobile')
    orderId = request.args.get('orderId')
    data = request.get_json()
    result = UserController.update_payment_status(orderId,mobile, data)
    return jsonify(result)


@user_bp.route('/get-orders-consumer', methods=['GET'])
def get_orders_consumer():
    """Get orders endpoint"""
    mobile = request.args.get('mobile')
    mobile = int(mobile)
    result = UserController.get_orders_consumer(mobile)
    return jsonify(result)

@user_bp.route('/get-orders-producer', methods=['GET'])
def get_orders_producer():
    """Get orders endpoint"""
    mobile = request.args.get('mobile')
    mobile = int(mobile)
    result = UserController.get_orders_producer(mobile)
    return jsonify(result)


















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