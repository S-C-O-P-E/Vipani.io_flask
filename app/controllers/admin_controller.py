from flask import Blueprint, request, jsonify
from ..extensions import mongo

class AdminController:
    @classmethod
    def add_banners(cls, data):
        try:
            banners_collection = mongo.db.banners
            existing_banner = banners_collection.find_one({"bannerId": data["bannerId"]})
            if existing_banner:
                return {"error": "Banner ID already exists"}, 409
            banners_collection.insert_one(data)
            return {"message": "Banner added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500