from flask import Blueprint, request, jsonify
from ..controllers.admin_controller import AdminController


# Create a blueprint for admin-related routes
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/addbanners', methods=['GET'])
def add_banners():
    print("Received request to add banners")
    data = request.get_json()
    response, status = AdminController.add_banners(data)
    return jsonify(response), status