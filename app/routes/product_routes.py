from flask import Blueprint, request, jsonify
from ..controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

# @product_bp.route('/', methods=['GET'])
# def index():
#     return "Welcome to Vipani.io!"

@product_bp.route('/get', methods=['GET'])
def get_product():
    product_id = request.args.get('productid')
    print(f"Received product ID: {product_id}")
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    response, status = ProductController.get_product(product_id)
    print(f"Response: {response}, Status: {status}")
    return jsonify(response), status

@product_bp.route('/add', methods=['POST'])
def add_product():
    product_data = request.get_json()
    required_fields = ['productId','producerId', 'name', 'description', 'price', 'available','image','location']
    
    if not all(field in product_data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    response, status = ProductController.add_product(product_data)
    return jsonify(response), status

@product_bp.route('update/<product_id>', methods=['PUT'])
def update_product(product_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No update data provided"}), 400
        
    response, status = ProductController.update_product(product_id, update_data)
    return jsonify(response), status

@product_bp.route('/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    response, status = ProductController.delete_product(product_id)
    return jsonify(response), status














