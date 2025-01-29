from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "music"

def get_database():
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]
def serialize_mongo_document(doc):
    """
    Convierte los campos ObjectId en un documento MongoDB a cadenas.
    """
    if not doc:
        return None
    doc['_id'] = str(doc['_id'])  # Convierte _id a string
    return doc
