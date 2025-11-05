from flask import Flask ,request,jsonify
from functools import wraps
import jwt
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
client=MongoClient(os.getenv('MongoClient_URI'))
db=client["TechbayDB"]
users=db["todouser"]

#logout but token still valid are stored here
blacklist=set()

#Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args,**kargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and len(auth_header.split(" ")) == 2:
            token = auth_header.split(" ")[1]
        else:
            return jsonify({'message': 'Token missing in request'}), 400
    
        if token in blacklist:
            return jsonify({'message':'Token has been revoked!'}),401

        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user=users.find_one({'_id':ObjectId(data['user_id'])})

            if not current_user:
                return jsonify({'message':'User not found!'}),401
            
        except jwt.ExpiredSignatureError:
            blacklist.add(token)
            return jsonify({'message':"Token has expired!"}),401
        except jwt.InvalidTokenError:
            return jsonify({'message':'Token is invalid!'}),401
        
        return f(current_user,*args,**kargs)
    return decorated
