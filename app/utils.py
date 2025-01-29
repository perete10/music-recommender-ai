# utils.py
def serialize_mongo_document(doc):
    """
    Convierte un documento de MongoDB en un formato serializable para JSON.
    """
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])  # Convertir ObjectId a string
    return doc
