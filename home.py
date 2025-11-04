from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify
from flask_cors import CORS
import json

load_dotenv()
app=Flask(__name__)
CORS(app)
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
products=db["products"]
categories=db["categories"]

@app.route("/", methods=['GET'])
def show_categories():
    category_list=list(categories.find({}))
    # Convert ObjectId to string
    for category in category_list:
        category['_id'] = str(category['_id'])
      
    return jsonify(category_list)



if __name__== '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=5001)