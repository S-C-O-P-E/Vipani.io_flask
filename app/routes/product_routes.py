from flask import Blueprint, request, jsonify, send_from_directory
from ..controllers.product_controller import ProductController
import os   

product_bp = Blueprint("product", __name__)

# UPLOAD_FOLDER = "images/products"
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @product_bp.route('/', methods=['GET'])
# def index():
#     return "Welcome to Vipani.io!"


@product_bp.route('/add', methods=['POST'])
def add_product():
    """API endpoint to add a new product"""
    mobile = request.form.get("mobile")  # Mobile number from request
    product_data = request.form.to_dict()  # Convert form data to dictionary
    files = request.files.getlist("files")  # Get multiple files

    # Required fields for validation
    required_fields = [ 'name', 'description', 'price', 'available']
    
    if not all(field in product_data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    response, status = ProductController.add_product(mobile, product_data, files)
    return jsonify(response), status

@product_bp.route('/getall', methods=['GET'])
def get_products():
    """API endpoint to get all products"""
    response, status = ProductController.get_products()
    return jsonify(response), status

@product_bp.route('/getproductbyid', methods=['GET'])
def get_product():
    """API endpoint to get a product by ID"""
    product_id = request.args.get('productId')
    response, status = ProductController.get_product(product_id)
    return jsonify(response), status

@product_bp.route("/images/products/<filename>")
def serve_product_media(filename):
    #print("Serving product media:", filename)
    """Serve product images/videos from server"""
    return ProductController.serve_product_media(filename)


@product_bp.route('/getproductsbybannerid', methods=['POST'])
def get_products_by_banner_id():
    """API endpoint to get products by banner ID"""
    data = request.get_json()
    response, status = ProductController.get_products_by_banner_id(data)
    return jsonify(response), status


@product_bp.route('/getproductsbycategory', methods=['POST'])
def get_products_by_category():
    """API endpoint to get products by category"""
    data = request.get_json()
    response, status = ProductController.get_products_by_category(data)
    return jsonify(response), status


@product_bp.route('/addtowishlist', methods=['POST'])
def add_to_wishlist():
    """API endpoint to add a product to the wishlist"""
    data = request.get_json()
    response, status = ProductController.add_to_wishlist(data)
    return jsonify(response), status


@product_bp.route('/getwishlist', methods=['GET'])
def get_wishlist():
    """API endpoint to get the wishlist"""
    mobile = request.args.get("mobile")
    response, status = ProductController.get_wishlist(mobile)
    return jsonify(response), status

@product_bp.route('/removefromwishlist', methods=['DELETE'])
def remove_from_wishlist():
    """API endpoint to remove a product from the wishlist"""
    data = request.get_json()
    response, status = ProductController.remove_from_wishlist(data)
    return jsonify(response), status

@product_bp.route('/getproductsnearuser', methods=['GET'])
def get_products_near_user():
    """API endpoint to get products sorted by proximity to the user"""
    mobile = request.args.get("mobile")
    if not mobile:
        return jsonify({"error": "Mobile number is required"}), 400

    response, status = ProductController.get_products_near_user(mobile)
    return jsonify(response), status


@product_bp.route('/latest-arrivals', methods=['GET'])
def get_latest_arrivals():
    """API endpoint to get the latest arrivals"""
    response, status = ProductController.get_latest_arrivals()
    return jsonify(response), status
















