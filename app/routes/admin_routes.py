from flask import Blueprint, request, jsonify, send_from_directory
from ..controllers.admin_controller import AdminController

# Create a blueprint for admin-related routes
admin_bp = Blueprint("admin", __name__)

# @admin_bp.route("/addbanner", methods=["POST"])
# def add_banner():
#     """Upload a new banner"""
#     file = request.files.get("file")
#     if not file:
#         return jsonify({"error": "No file uploaded"}), 400

#     response, status = AdminController.add_banner(file)
#     return jsonify(response), status


# @admin_bp.route("/getbanners", methods=["GET"])
# def get_banners():
#     """Retrieve all banners"""
#     response, status = AdminController.get_banners()
#     return jsonify(response), status


# @admin_bp.route("/deletebanner/<banner_id>", methods=["DELETE"])
# def delete_banner(banner_id):
#     """Delete a specific banner"""
#     response, status = AdminController.delete_banner(banner_id)
#     return jsonify(response), status

@admin_bp.route("/addbanner", methods=["POST"])
def add_banner():
    """Upload a new banner"""
    data = request.get_json()
    #print(data)
    response, status = AdminController.add_banner(data)
    return response, status

@admin_bp.route("/getbanners", methods=["GET"])
def get_banners():
    """Retrieve all banners"""
    response, status = AdminController.get_banners()
    return jsonify(response), status


@admin_bp.route("/addbanneridtopdt", methods=["PATCH"])
def add_banner_id_to_product():
    """Add banner ID to product"""
    data = request.get_json()
    response, status = AdminController.add_banner_id_to_product(data)
    return response, status

@admin_bp.route("/images/banners/<filename>")
def serve_banner(filename):
    print("Serving banner:", filename)
    """Serve images directly from the banners folder"""
    return AdminController.serve_banner(filename)


@admin_bp.route("/addcategory", methods=["POST"])
def add_category():
    """Add a new category"""
    data = request.get_json()
    response, status = AdminController.add_category(data)
    return response, status


@admin_bp.route("/getcategories", methods=["GET"])
def get_categories():
    """Retrieve all categories"""
    response, status = AdminController.get_categories()
    return jsonify(response), status

@admin_bp.route("/deletecategory/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    """Delete a specific category"""
    response, status = AdminController.delete_category(category_id)
    return jsonify(response), status


