import pymongo
import json

from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, Response, make_response
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

try:
    mongo = pymongo.MongoClient(
        host="mongodb://localhost:27017",
        serverSelectionTimeoutMS = 3000
    )
    db = mongo.fishdbapi
    mongo.server_info()
except:
    print("Can't connect to database")
    
@app.route("/", methods=["GET"])
def getPond():
    try:
        data = list(db.pond.find())
        for pond in data:
            pond['_id'] = str(pond['_id'])
        response = make_response(jsonify(data,{"message": "Pond fetched"}),200)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
       response = make_response(jsonify({"error":str(e)}),500)
       response.headers["Content-Type"] = "application/json"
       return response
      
@app.route('/pond/<id>', methods=['GET'])
def getSelectedPond(id):
    try:
        data = db.pond.find_one({'_id': ObjectId(id)})
        data['_id'] = str(data['_id'])
        response = make_response(jsonify(data,{"message": "Pond selected"}),200)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
       response = make_response(jsonify({"error":str(e)}),500)
       response.headers["Content-Type"] = "application/json"
       return response
      
@app.route('/registerPond', methods=['POST'])
def registerPond():
    try:
        data = {
            "name": request.form['name'],
            "location": request.form['location'],
            "shape": request.form['shape'],
            "material": request.form['material']
        }
        dbResponse = db.pond.insert_one(data)
        response = make_response(jsonify({"message": "Pond created"}),200)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e: 
        response = make_response(jsonify({"error":str(e)}),500)
        response.headers["Content-Type"] = "application/json"
        return response
    
if __name__ == '__main__':
    app.run(debug=True)
