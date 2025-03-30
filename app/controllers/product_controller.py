from ..extensions import mongo
from bson.json_util import dumps
import json
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from bson import ObjectId
from math import radians, sin, cos, sqrt, atan2

# Define the folder for storing product images/videos
UPLOAD_FOLDER = "images/products"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(filename):
    """Get correct file path"""
    return os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")

class ProductController:

    @classmethod
    def add_product(cls, mobile, product_data, files):
        try:
            products_collection = mongo.db.productdata
            users_collection = mongo.db.userdatas  # Collection for user details
            productId = ObjectId()
            product_data["productId"] = str(productId)
            # Check if productId already exists
            if products_collection.find_one({"productId": product_data["productId"]}):
                return {"error": "Product ID already exists"}, 409

            print(mobile,type(mobile))
            mobile = int(mobile)
            product_data["price"] = int(product_data["price"])
            product_data["available"] = bool(product_data["available"])
            print('id', product_data["bannerid"])
            # Fetch user location using mobile number
            user = users_collection.find_one({"mobile": mobile})
            print(user)
            if not user:
                return {"error": "User not found"}, 404

            product_data["location"] = user["location"]
            product_data["latitude"] = user["latitude"]
            product_data["longitude"] = user["longitude"]
            product_data["bannerid"] = []

            # Save files and generate URLs
            file_urls = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = get_file_path(filename)
                    file.save(filepath)  # Save file

                    server_url = "https://vipani-io-flask.onrender.com"
                    file_url = f"{server_url.rstrip('/')}/api/v1/product/images/products/{filename}"
                    print(file_url)
                    file_urls.append(file_url)

            # Store file URLs in product data
            product_data["media"] = file_urls  # Store images/videos URLs

            # Insert into MongoDB
            products_collection.insert_one(product_data)

            print(product_data)
        
            if "_id" in product_data:
                del product_data["_id"]

            return {"message": "Product added successfully", "product": product_data}, 201

        except Exception as e:
            return {"error": str(e)}, 500
        
    @classmethod
    def get_product(cls, product_id):
        try:
            print(product_id)
            products_collection = mongo.db.productdata
            product = products_collection.find_one({"productId": product_id}, {"_id": 0})
            if product:
                return product, 200
            else:
                return {"error": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @classmethod
    def get_products(cls):
        try:
            products_collection = mongo.db.productdata
            products = list(products_collection.find({}, {"_id": 0}))
            products = json.loads(dumps(products))
            return products, 200

        except Exception as e:
            return {"error": str(e)}, 500
        

    
    @classmethod
    def serve_product_media(cls, filename):
        return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename)
    

    @classmethod
    def get_products_by_banner_id(cls, data):
        try:
            products_collection = mongo.db.productdata
            bannerid = data.get("bannerid")
            products = list(products_collection.find({"bannerid": bannerid}, {"_id": 0}))
            products = json.loads(dumps(products))
            return products, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @classmethod
    def get_products_by_category(cls, data):
        try:
            products_collection = mongo.db.productdata
            category = data.get("catid")
            products = list(products_collection.find({"catid": category}, {"_id": 0}))
            products = json.loads(dumps(products))
            return products, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

    @classmethod
    def add_to_wishlist(cls, data):
        try:
            products_collection = mongo.db.productdata
            users_collection = mongo.db.userdatas
            productId = data.get("productId")
            mobile = data.get("mobile")
            user = users_collection.find_one({"mobile": mobile})
            if not user:
                return {"error": "User not found"}, 404
            product = products_collection.find_one({"productId": productId})
            if not product:
                return {"error": "Product not found"}, 404
            list = user.get("wishlist", [])
            if productId in list:
                return {"error": "Product already in wishlist"}, 409
            list.append(productId)
            users_collection.update_one({"mobile": mobile}, {"$set": {"wishlist": list}})   
            return {"message": "Product added to wishlist"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @classmethod
    def get_wishlist(cls, mobile):
        try:
            users_collection = mongo.db.userdatas
            mobile = int(mobile)
            user = users_collection.find_one({"mobile": mobile})
            print(user)
            if not user:
                return {"error": "User not found"}, 404
            wishlist = user.get("wishlist", [])
            return {"wishlist": wishlist}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    
    @classmethod
    def remove_from_wishlist(cls, data):
        try:
            products_collection = mongo.db.productdata
            users_collection = mongo.db.userdatas
            productId = data.get("productId")
            mobile = data.get("mobile")
            user = users_collection.find_one({"mobile": mobile})
            if not user:
                return {"error": "User not found"}, 404
            product = products_collection.find_one({"productId": productId})
            if not product:
                return {"error": "Product not found"}, 404
            list = user.get("wishlist", [])
            if productId not in list:
                return {"error": "Product not in wishlist"}, 404
            list.remove(productId)
            users_collection.update_one({"mobile": mobile}, {"$set": {"wishlist": list}})
            return {"message": "Product removed from wishlist"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

    #poximity listing
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate the distance between two lat/lon points using the Haversine formula"""
        R = 6371  # Radius of Earth in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon2

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c  # Distance in km

    @classmethod
    def get_products_near_user(cls, mobile):
        try:
            users_collection = mongo.db.userdatas
            products_collection = mongo.db.productdata

            # Fetch user details
            user = users_collection.find_one({"mobile": int(mobile)})
            if not user:
                return {"error": "User not found"}, 404

            user_lat = int(user["latitude"])
            user_lon = int(user["longitude"])

            # Fetch all products
            products = list(products_collection.find({}, {"_id": 0}))
            
            # Compute distances
            for product in products:
                product_lat = int(product.get("latitude", 0))
                product_lon = int(product.get("longitude", 0))
                product["distance"] = cls.calculate_distance(user_lat, user_lon, product_lat, product_lon)

            # Sort products by distance
            products = sorted(products, key=lambda x: x["distance"])

            return products, 200

        except Exception as e:
            return {"error": str(e)}, 500


    @classmethod
    def get_latest_arrivals(cls):
        try:
            products_collection = mongo.db.productdata
            # Fetch the latest 10 products and exclude the '_id' field
            latest_arrivals = list(products_collection.find({}, {"_id": 0}).sort("_id", -1).limit(50))
            print(latest_arrivals)
            return latest_arrivals, 200
        except Exception as e:
            return {"error": str(e)}, 500
