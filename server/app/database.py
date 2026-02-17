import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    key_path = os.getenv('FIREBASE_KEY_PATH')
    db_url = os.getenv('FIREBASE_DB_URL')

    if not key_path or not db_url:
        raise ValueError("Missing FIREBASE_KEY_PATH or FIREBASE_DB_URL in environment variables")
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": db_url
        })

    return db

firebase_db = initialize_firebase()