from flask import current_app, jsonify
from bson import ObjectId
from ..extensions import mongo

class UserController:
    @classmethod
    def get_user(cls, user_id):
        try:   
            print(f"Fetching user with ID: {user_id}",type(user_id))
            users_collection = mongo.db.userdatas
            user = users_collection.find_one({"userid": user_id})
            print(f"Fetched user: {user}")
            
            if user:
                # Convert ObjectId to string for JSON serialization
                user['_id'] = str(user['_id'])
                return user, 200
            else:
                return {"error": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


