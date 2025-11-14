from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from ...database.firebase import Firebase
from ...database.mongodb import MongoDB
from flask_cors import CORS, cross_origin

api_bp = Blueprint("api", __name__)
@api_bp.route('/data')
def data():
    return jsonify({"data": [1, 2, 3]})
#firebase_db = Firebase("agent52-firebase-adminsdk-fbsvc-913162cdf2.json")
#firebase_db.create("users", {"name": "Alice"})
#

@api_bp.route("/<collection>", methods=["POST"])
def create_item(collection):
    mongo_db = MongoDB("mongodb+srv://hqnhatdn:XiSgrN0lRLq4A8ch@cluster0.wnkrqan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", "mydb")
    data = request.json
    _id = mongo_db.create(collection, data)  # returns the inserted doc
    return jsonify({'id': _id}), 201

# READ ALL
@api_bp.route("/<collection>", methods=["GET"])
@cross_origin(origins="https://oangia.github.io")
def get_items(collection):
    # Get page and limit from query params
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    skip = (page - 1) * limit

    # Total documents
    total_records = mongo_db.total(collection)

    # Total pages
    total_pages = (total_records + limit - 1) // limit  # ceiling division

    # Query MongoDB
    cursor = mongo_db.paginate(collection, skip, limit)
    
    items = []
    for item in cursor:
        item["_id"] = str(item["_id"])
        items.append(item)

    return jsonify({
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "items": items
    })

# READ ONE
@api_bp.route("/<collection>/<item_id>", methods=["GET"])
def get_item(collection, item_id):
    #if not request.is_json:
    #    return jsonify({"error", "Not found"}), 404
    item = mongo_db.read(collection, item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

# UPDATE
@api_bp.route("/<collection>/<item_id>", methods=["PUT"])
def update_item(collection, item_id):
    data = request.json
    updated = mongo_db.update(collection, item_id, data)
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Not found"}), 404

# DELETE
@api_bp.route("/<collection>/<item_id>", methods=["DELETE"])
def delete_item(collection, item_id):
    deleted = mongo_db.delete(collection, item_id)
    if deleted:
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Not found"}), 404

