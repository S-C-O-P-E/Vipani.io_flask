from flask import jsonify, send_from_directory
from ..extensions import mongo
import os
from werkzeug.utils import secure_filename
from bson import ObjectId

# Folder to save banners
UPLOAD_FOLDER = "images/banners"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_file_path(filename):
    """Get correct file path"""
    return os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}

def allowed_file(filename):
    """Check if file has a valid extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

class AdminController:
    # @classmethod
    # def add_banner(cls, file):
    #     """Handle file upload and save banner details in DB"""
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         filepath = get_file_path(filename)
    #         file.save(filepath)  # Save file to server

    #         # Create ObjectId
    #         banner_id = ObjectId()

    #         # Generate accessible image URL
    #         server_url = "https://vipani-io-flask.onrender.com"
    #         image_url = f"{server_url.rstrip('/')}/api/v1/admin/images/banners/{filename}"

    #         # Save to MongoDB
    #         banner = {
    #             "_id": banner_id,
    #             "bannerId": str(banner_id),
    #             "filename": filename,
    #             "filepath": filepath,
    #             "imageUrl": image_url  # Added image URL
    #         }
    #         mongo.db.banners.insert_one(banner)

    #         banner["_id"] = str(banner["_id"])  # Convert ObjectId for JSON response
    #         return {"message": "Banner added successfully", "banner": banner}, 201

    #     return {"error": "Invalid file type"}, 400

    # @classmethod
    # def get_banners(cls):
    #     """Retrieve all banners"""
    #     banners = list(mongo.db.banners.find({}, {"_id": 0}))  # Exclude MongoDB _id
    #     return {"banners": banners}, 200

    # @classmethod
    # def delete_banner(cls, banner_id):
    #     """Delete a banner by ID"""
    #     banner = mongo.db.banners.find_one({"bannerId": banner_id})
    #     if not banner:
    #         return {"error": "Banner not found"}, 404

    #     # Delete file from server
    #     filepath = banner.get("filepath")
    #     if filepath and os.path.exists(filepath):
    #         os.remove(filepath)

    #     # Delete from MongoDB
    #     mongo.db.banners.delete_one({"bannerId": banner_id})

    #     return {"message": "Banner deleted successfully"}, 200

    @classmethod
    def add_banner(cls, banner):
        existing_banner = mongo.db.banners.find_one({"bannerId": banner["bannerId"]})
        #print("existing",existing_banner)
        
        if existing_banner:
            if "_id" in existing_banner:
                del existing_banner["_id"]
            return {"error": "Banner already exists", "banner": existing_banner}, 409
        mongo.db.banners.insert_one(banner)
        if "_id" in banner:
            del banner["_id"]
        return {"message": "Banner added successfully", "banner": banner}, 201
    
    @classmethod
    def get_banners(cls):
        banners = list(mongo.db.banners.find({}, {"_id": 0}))
        return {"banners": banners}, 200
    
    @classmethod
    def add_banner_id_to_product(cls, data):
        product = mongo.db.productdata.find_one({"productId": data["productId"]})
        if not product:
            return {"error": "Product not found"}, 404
        product["bannerid"].append(data["bannerid"])
        mongo.db.productdata.update_one({"productId": data["productId"]}, {"$set": product})
        return {"message": "Banner ID added to product successfully"}, 200
        

    @classmethod
    def serve_banner(cls, filename):
        """Serve images directly from banners folder"""
        return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename)
    
    @classmethod
    def add_category(cls, data):
        """Add a new category"""

        #check if category already exists
        existing_category = mongo.db.categorydata.find_one({"catid": data["catid"]})
        #print(existing_category)
        if "_id" in existing_category:
            del existing_category["_id"]
        if existing_category:
            return {"error": "Category already exists","category" : existing_category}, 400

        mongo.db.categorydata.insert_one(data)  # Insert data into MongoDB

        # Remove MongoDB's auto-generated _id before returning response
        if "_id" in data:
            del data["_id"]

        return {"message": "Category added successfully", "category": data}, 201
    
    @classmethod
    def get_categories(cls):
        """Retrieve all categories"""
        categories = list(mongo.db.categorydata.find({}, {"_id": 0}))  # Exclude MongoDB _id

        return {"categories": categories}, 200
    
    @classmethod
    def delete_category(cls, catid):
        """Delete a category by ID"""
        category = mongo.db.categorydata.find_one({"catid": catid})
        if not category:
            return {"error": "Category not found"}, 404
        # Delete from MongoDB
        mongo.db.categorydata.delete_one({"catid": catid})
        return {"message": "Category deleted successfully"}, 200
