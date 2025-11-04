from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
import json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token,JWTManager
from authentication import token_required
from flask_jwt_extended import get_jwt_identity, jwt_required
from bson import ObjectId
from datetime import datetime

load_dotenv()
app=Flask(__name__)
CORS(app)
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
users=db["users"]
addresses=db["addresses"]

@app.route("/profile", methods=['GET'])
@token_required
def details():
    email=get_jwt_identity()
    if email == users.find_one({"email":email}):
        user = users.find_one(
        {"email": email},
        {"username": 1, "email": 1, "image": 1})
    return jsonify(user), 200
            
# Address
@app.route('/add_address', methods=['POST'])
def add_address():
    data = request.get_json()

    # Extract all the fields from request
    owner = data.get('owner')
    name = data.get('name')
    address = data.get('address')
    mobile = data.get('mobile')
    alternatemobile = data.get('alternatemobile')
    city = data.get('city')
    state = data.get('state')
    pincode = data.get('pincode')
    type_ = data.get('type')  # 'type' is a reserved word, so use type_

    # Basic validation
    if not all([owner, name, address, mobile, city, state, pincode, type_]):
        return jsonify({"error": "All required fields must be filled"}), 400

    # Prepare document
    new_address = {
        "owner": ObjectId(owner),  # convert string id to ObjectId
        "name": name,
        "address": address,
        "mobile": mobile,
        "alternatemobile": alternatemobile,
        "city": city,
        "state": state,
        "pincode": pincode,
        "type": type_,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    # Insert into new collection 'address'
    addresses.insert_one(new_address)

    return jsonify({"message": "Address added successfully"}), 201

if __name__== '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=5003)
