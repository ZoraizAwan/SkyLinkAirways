try:
    # If allowed list maps to pymongo, this will work
    from pymongo import MongoClient
except Exception:
    # If a different package named 'mongodb' is provided in your environment use it:
    try:
        import mongodb as mongo_driver  # fallback if institution provides a wrapper
        MongoClient = mongo_driver.MongoClient
    except Exception:
        MongoClient = None

def get_mongo_client(uri="mongodb://localhost:27017"):
    if MongoClient is None:
        raise RuntimeError("MongoDB driver not available. Install pymongo or provide mongodb driver.")
    return MongoClient(uri)

def insert_support_ticket(name, email, subject, message):
    client = get_mongo_client()
    db = client.slyink_db
    res = db.tickets.insert_one({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "status": "open"
    })
    client.close()
    return str(res.inserted_id)