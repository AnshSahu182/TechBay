from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
import json
from bson import ObjectId

load_dotenv()
app=Flask(__name__)
CORS(app)
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
products=db["products"]

#Product Page
@app.route("/products", methods=['GET'])
def prodcuts():
    products_list=list(products.find())
    for product in products_list:
            product['_id'] = str(product['_id'])
    return (products_list),200

@app.route("/products/categories", methods=['POST'])
def get_by_category():
    data = request.get_json()
    category = data.get('category')

    if not category:
        return jsonify({"error": "Category is required"}), 400

    product_list = list(products.find({"category": category}, {"_id": 0}))
    return jsonify(product_list)

@app.route("/products/brand", methods=['POST'])
def get_by_brand():
    data = request.get_json()
    brand = data.get('brand')

    if not brand:
        return jsonify({"error": "Brand is required"}), 400

    product_list = list(products.find({"brand": brand}, {"_id": 0}))
    return jsonify(product_list)

@app.route("/products/price_range", methods=["POST"])
def get_by_price():
    data= request.get_json()
    min_price=data.get('min')
    max_price=data.get('max')
    query = {"price":{"$gte":min_price,"$lte":max_price}}
    products_list=list(products.find(query))

# Convert ObjectIds to string
    for product in products_list:
        product['_id'] = str(product['_id'])
    return jsonify(products_list), 200

def featured_products():
    featured_ids = [
        "65b54e14a39a3ffd12fd2c12",
        "65b54e14a39a3ffd12fd2c10",
        "65b54e14a39a3ffd12fd2c0e",
        "65b54e14a39a3ffd12fd2c0c"
    ]

    # Convert strings to ObjectIds
    object_ids = [ObjectId(pid) for pid in featured_ids]

    # Fetch only these products
    featured = list(products.find(
        {"_id": {"$in": object_ids}},
        {"_id": 1, "name": 1, "price": 1, "image": 1, "category": 1}  # optional: limit fields
    ))

    # Convert ObjectIds to strings for JSON
    for prod in featured:
        prod["_id"] = str(prod["_id"])

    return jsonify(featured), 200

if __name__== '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=5002)