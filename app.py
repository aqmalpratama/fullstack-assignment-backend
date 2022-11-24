import pymongo
import json

from flask import Flask, Response, request, make_response, jsonify
from flask_cors import CORS, cross_origin
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

        response = make_response(
                jsonify(data,
                    {"message": "Pond fetched"}
                ),
                200,
            )
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
        response = make_response(jsonify(data,{"message": "Pond get"}),200)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
       response = make_response(jsonify({"error":str(e)}),500)
       response.headers["Content-Type"] = "application/json"
       return response

@app.route('/pond/<id>', methods=['PUT'])
def pondUpdate(id):
    try:
        if request.method == 'PUT':
            data = {
                "name": request.form['name'],
                "location": request.form['location'],
                "shape": request.form['shape'],
                "material": request.form['material'],
                }
            dbResponse = db.pond.update_one({'_id': ObjectId(id)}, {'$set': data})
            response = make_response(jsonify({"message": "Pond updated"}),200)
            response.headers["Content-Type"] = "application/json"
            return response
        return make_response(jsonify({"message": "Pond already updated"}),200)
    except Exception as e:
       response = make_response(jsonify({"error":str(e)}),500)
       response.headers["Content-Type"] = "application/json"
       return response
      
@app.route('/register', methods=['POST'])
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
