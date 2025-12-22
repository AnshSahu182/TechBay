from flask import request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MongoClient_URI'))
db = client["techbay"]
reviews = db["reviews"]
users = db["users"]
products = db["products"]

def review_product(current_user,product_id):
    data=request.get_json()
    rating=data.get('rating')
    comment=data.get('comment')

    if not rating or not comment:
        return jsonify({"error": "Rating and comment are required"}), 400
    
    reviews.insert_one({
        "user_id": current_user["_id"],
        "product_id": ObjectId(product_id),
        "rating": rating,
        "comment": comment,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()})
    
    return jsonify({"message":"Review added successfully"}),200

def update_review(current_user, review_id):
    data=request.get_json()
    rating=data.get('rating')
    comment=data.get('comment')

    review=reviews.find_one({"_id":ObjectId(review_id), "user_id":current_user["_id"]})
    if not review:
        return jsonify({"error": "Review not found or unauthorized"}), 404

    update_data={}
    if rating:
        update_data["rating"]=rating
    if comment:
        update_data["comment"]=comment
    update_data["updatedAt"]=datetime.utcnow()

    reviews.update_one({"_id":ObjectId(review_id)}, {"$set":update_data})

    return jsonify({"message":"Review updated successfully"}),200

def delete_review(current_user, review_id):
    review=reviews.find_one({"_id":ObjectId(review_id), "user_id":current_user["_id"]})
    if not review:
        return jsonify({"error": "Review not found or unauthorized"}), 404

    reviews.delete_one({"_id":ObjectId(review_id)})

    return jsonify({"message":"Review deleted successfully"}),200

def get_reviews_by_product(product_id):
    product_reviews=list(reviews.find({"product_id":ObjectId(product_id)}))
    for review in product_reviews:
        user=users.find_one({"_id":review["user_id"]})
        review["username"]=user["username"] if user else "Unknown"
        review["_id"]=str(review["_id"])
        review["user_id"]=str(review["user_id"])
        review["product_id"]=str(review["product_id"])
        review["createdAt"]=review["createdAt"].isoformat()
        review["updatedAt"]=review["updatedAt"].isoformat()
    return jsonify(product_reviews),200