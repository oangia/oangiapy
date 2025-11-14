from pymongo import MongoClient
from bson import ObjectId
from .base import BaseDB
def serialize_doc(doc):
    if not doc:
        return None
    doc = dict(doc)  # convert from BSON object
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def serialize_docs(docs):
    return [serialize_doc(d) for d in docs]

class MongoDB(BaseDB):
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def total(self, collection):
        return self.db[collection].count_documents({})

    def paginate(self, collection, skip, limit):
        return serialize_docs(self.db[collection].find().skip(skip).limit(limit))
    def create(self, collection, data):
        return str(self.db[collection].insert_one(data).inserted_id)

    def read(self, collection, item_id):
        return serialize_doc(self.db[collection].find_one({"_id": ObjectId(item_id)}))

    # Read all documents
    def all(self, collection):
        return serialize_docs(list(self.db[collection].find()))

    def update(self, collection, doc_id, data):
        result = self.db[collection].update_one({"_id": ObjectId(doc_id)}, {"$set": data})
        output = {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None
        }
        return output

    def delete(self, collection, doc_id):
        return self.db[collection].delete_one({"_id": ObjectId(doc_id)})
