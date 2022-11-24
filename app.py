import pymongo
import json

from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, Response
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
        value = list(db.pond.find())
        for pond in value:
            pond['_id'] = str(pond['_id'])
        response = jsonify(value, {"message": "Pond fetched"})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
    except Exception as e:
       response = jsonify({"error": str(e)})
       response.status_code = 400
       response.headers["Content-Type"] = "application/json"
    finally:
        return response
      
@app.route('/pond/<id>', methods=['GET'])
def getSelectedPond(id):
    try:
        value = db.pond.find_one({'_id': ObjectId(id)})
        value['_id'] = str(value['_id'])
        response = jsonify(data, {"message": "Pond selected"})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
    except Exception as e:
       response = jsonify({"error": str(e)})
       response.status_code = 400
       response.headers["Content-Type"] = "application/json"
    finally:
       return response
      
@app.route('/registerPond', methods=['POST'])
def registerPond():
    try:
        value = {
            "name": request.form['name'],
            "location": request.form['location'],
            "shape": request.form['shape'],
            "material": request.form['material']
        }
        executeDb = db.pond.insert_one(value)
        response = jsonify({"message": "Pond created"})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
    except Exception as e: 
        response = jsonify({"error": str(e)})
        response.status_code = 400
        response.headers["Content-Type"] = "application/json"
    finally:
        return response

@app.route('/pond/<id>', methods=['PUT'])
def updatePond(id):
    try:
        if request.method == 'PUT':
            value = {
                "name": request.form['name'],
                "location": request.form['location'],
                "shape": request.form['shape'],
                "material": request.form['material'],
            }
            executeDb = db.pond.update_one({'_id': ObjectId(id)}, {'$set': value})
            response = jsonify({"message": "Pond updated"})
            response.status_code = 200
            response.headers["Content-Type"] = "application/json"
    except Exception as e:
       response = jsonify({"error":str(e)})
       response.status_code = 400
       response.headers["Content-Type"] = "application/json"
    finally:
       return response
    
if __name__ == '__main__':
    app.run(debug=True)
