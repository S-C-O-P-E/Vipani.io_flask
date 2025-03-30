from flask import current_app, jsonify
from bson import ObjectId
import json
from ..extensions import mongo
import os
from werkzeug.utils import secure_filename


# Define the folder for storing product images/videos
UPLOAD_FOLDER = "images/producers"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(filename):
    """Get correct file path"""
    return os.path.join(UPLOAD_FOLDER, filename).replace("\\", "/")

class UserController:
    @classmethod
    def get_user(cls, user_id):
        try:
            
            #print(f"Fetching user with ID: {user_id}",type(user_id))
            # Ensure user_id is an ObjectId
            
            users_collection = mongo.db.userdatas
            user = users_collection.find_one({"userid": user_id})
            #print(f"Fetched user: {user}")
            
            if user:
                # Convert ObjectId to string for JSON serialization
                user['_id'] = str(user['_id'])
                return user
            else:
                return {"error": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
    
    @classmethod
    def login_user(cls, user_data):
        try:
            users_collection = mongo.db.userdatas
            existing_user = users_collection.find_one({"mobile": user_data["mobile"]})
            if existing_user:
                existing_user.pop("_id", None)  # Remove MongoDB _id
                #print(f"Existing user: {existing_user}")
                return {"message": "User already exists", "user": existing_user}, 200
            
            return {"message": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        

    @classmethod
    def register_user(cls, user_data):
        try:
            users_collection = mongo.db.userdatas
            existing_user = users_collection.find_one({"mobile": user_data["mobile"]})
            if existing_user:
                return {"error": "User already exists"}, 409
            # Generate a unique user ID
            user_id = str(ObjectId())  # Generate user ID
            user_data["userid"] = user_id
            #print(f"Generated user ID: {user_id}")
            # Insert the user data into the database (excluding _id)
            users_collection.insert_one(user_data)
            #print("User data inserted successfully")
            # Remove _id before returning
            user_data.pop("_id", None)
            return {"message": "User registered successfully", "user": user_data}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        

    @classmethod
    def update_profile(cls,mobile, user_data):
        try:
            users_collection = mongo.db.userdatas
            existing_user = users_collection.find_one({"mobile": mobile})
            if not existing_user:
                return {"error": "User not found"}, 404
            # Update the user's profile
            users_collection.update_one(
                {"mobile": mobile},
                {"$set": user_data}
            )
            return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

    @classmethod
    def update_producer(cls,mobile,producer_data,file):
        try:
            mobile = int(mobile)
            users_collection = mongo.db.userdatas
            existing_user = users_collection.find_one({"mobile": mobile})
            if not existing_user:
                return {"error": "User not found"}, 404
            # Update the user's profile
            print(producer_data)
            print(type(producer_data['categories']))
            print(producer_data['categories'])
            producer_data['categories'] = json.loads(producer_data['categories'])
            print(("type",producer_data['categories']))

            if file and allowed_file(file.filename):
                print("File is allowed")
                filename = secure_filename(file.filename)
                file_path = get_file_path(filename)
                file.save(file_path)
                server_url = "https://vipani-io-flask.onrender.com"
                file_url = f"{server_url.rstrip('/')}/api/v1/user/images/producers/{filename}"
                print(file_url)
                producer_data["media"] = file_url
                users_collection.update_one(
                    {"mobile": mobile},
                    {"$set": producer_data}
                )
                print("data",producer_data)

                return {"message": "Profile updated successfully"}, 200
            else:
                users_collection.update_one(
                    {"mobile": mobile},
                    {"$set": producer_data}
                )
                return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

            
        
        

    @classmethod
    def update_location(cls,mobile, user_data):
        try:
            users_collection = mongo.db.userdatas
            existing_user = users_collection.find_one({"mobile": mobile})
            if not existing_user:
                return {"error": "User not found"}, 404
            # Update the user's location
            users_collection.update_one(
                {"mobile": mobile},
                {"$set": {"latitude": user_data['latitude'], "longitude": user_data['longitude']}}
            )
            return {"message": "Location updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        

    @classmethod
    def follow_user(cls, data):
        try:
            user_mobile = data.get("consumer_mobile")
            producer_mobile = data.get("producer_mobile")
            follow_collection = mongo.db.userdatas
            user = follow_collection.find_one({"mobile": user_mobile})
            producer = follow_collection.find_one({"mobile": producer_mobile})
            if not user or not producer:
                return {"error": "User not found"}, 404
            following = user.get("following", [])
            if producer_mobile in following:
                pass
            else:
                following.append(producer_mobile)
                follow_collection.update_one(
                    {"mobile": user_mobile},
                    {"$set": {"following": following}}
                )
            followers = producer.get("followers", [])
            if user_mobile in followers:
                pass
            else:
                followers.append(user_mobile)
                follow_collection.update_one(
                    {"mobile": producer_mobile},
                    {"$set": {"followers": followers}}
                )
            return {"message": "User followed successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
            

        
        