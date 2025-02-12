from ..extensions import mongo
import base64

class CategoryController:
    @classmethod
    def get_category(cls):
        try:
            category_collection = mongo.db.categorydata
            categories = category_collection.find()
            category_list = []
            for category in categories:
                category.pop("_id")
                
                if "image" in category:
                    category["image"] = base64.b64encode(category["image"]).decode('utf-8')
                category_list.append(category)
            return category_list, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @classmethod
    def add_category(cls,catid,name,image):
        try:
            category_collection = mongo.db.categorydata
            if category_collection.find_one({"catid":catid}):
                return {"error": "Category ID already exists"}, 409
            
            image_binary = image.read()

            category_data = {
                "catid": catid,
                "name": name,
                "image": image_binary
            }
            category_collection.insert_one(category_data)
            return {"message": "Category added successfully"}, 201
        
        except Exception as e:
            return {"error": str(e)}, 500
