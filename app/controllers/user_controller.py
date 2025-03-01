from flask import current_app, jsonify
from bson import ObjectId
from ..extensions import mongo

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
        
            

        
        