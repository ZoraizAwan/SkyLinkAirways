try:
    from pymongo import MongoClient
except Exception:
    try:
        import mongodb as mongo_driver  # institution-provided wrapper fallback
        MongoClient = mongo_driver.MongoClient
    except Exception:
        MongoClient = None

import os

def get_mongo_client(uri=None):
    if MongoClient is None:
        raise RuntimeError("MongoDB driver not available. Install pymongo or provide mongodb driver.")
    uri = uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    return MongoClient(uri)


def insert_support_ticket(name, email, subject, message):
    client = get_mongo_client()
    db = client.skylink_db
    res = db.tickets.insert_one({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "status": "open"
    })
    client.close()
    return str(res.inserted_id)
