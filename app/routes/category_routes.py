from flask import Blueprint, request, jsonify
from app.controllers.category_controller import CategoryController

category_bp =  Blueprint('category', __name__)

@category_bp.route('/getcategory', methods=['GET'])
def get_category():
    try:
        response, status = CategoryController.get_category()
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@category_bp.route('/addcategory', methods=['POST'])
def add_category():
    try:
        catid=request.form.get('catid')
        name=request.form.get('name')
        image=request.files.get('image')

        if not catid or not name or not image:
            return jsonify({"error": "Missing required fields"}), 400
        
        response, status = CategoryController.add_category(catid,name,image)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500