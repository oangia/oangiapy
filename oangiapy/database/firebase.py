import firebase_admin
from firebase_admin import credentials, firestore
from .base import BaseDB

class Firebase(BaseDB):
    def __init__(self, service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create(self, collection, data):
        return self.db.collection(collection).add(data)

    def read(self, collection, query=None):
        col = self.db.collection(collection)
        if query:
            for field, op, value in query:
                col = col.where(field, op, value)
        return [doc.to_dict() for doc in col.stream()]

    def update(self, collection, doc_id, data):
        self.db.collection(collection).document(doc_id).update(data)

    def delete(self, collection, doc_id):
        self.db.collection(collection).document(doc_id).delete()