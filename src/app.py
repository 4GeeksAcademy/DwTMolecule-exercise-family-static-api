"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members


    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def add_member():
    body =request.json
    member = {}
    if "id" in body:
        member["id"] = body["id"]
    else:
        member["id"] = jackson_family._generateId()
    member = {
        **member,
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    new_member = jackson_family.add_member(member)
    response_body = {
        "new": new_member
    }

    return jsonify(response_body), 200



@app.route('/member/<int:id>', methods=['GET'])
def member_for_id(id):
    member = jackson_family.get_member(id)

    if member:
        formatted_member = {
            "id": member["id"],
            "first_name": member["first_name"], 
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(formatted_member), 200
    else:
        return jsonify({"msg": "Miembro no encontrado"}), 404
    


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    
    deleted = jackson_family.delete_member(id)

    if deleted:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"done": False}), 404

    # this is how you can use the Family datastructure by calling its methods


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
