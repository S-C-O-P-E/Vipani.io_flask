from ..extensions import mongo
from bson.json_util import dumps
import json

class ProductController:
    @classmethod
    def get_product(cls, product_id):
        try:
            products_collection = mongo.db.productdata
            product = products_collection.find_one({"productId": product_id})
            
            if product:
                product.pop("_id")
                return product,200
            return {"error": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @classmethod
    def add_product(cls, product_data):
        try:
            products_collection = mongo.db.productdata
            if products_collection.find_one({"productId": product_data["productId"]}):
                return {"error": "Product ID already exists"}, 409
            products_collection.insert_one(product_data)
            return {"message": "Product added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @classmethod
    def update_product(cls, product_id, update_data):
        try:
            products_collection = mongo.db.productdata
            result = products_collection.update_one(
                {"productId": product_id},
                {"$set": update_data}
            )
            if result.modified_count:
                return {"message": "Product updated successfully"}, 200
            return {"error": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @classmethod
    def delete_product(cls, product_id):
        try:
            products_collection = mongo.db.productdata
            result = products_collection.delete_one({"productId": product_id})
            if result.deleted_count:
                return {"message": "Product deleted successfully"}, 200
            return {"error": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500