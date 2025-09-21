import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv
import os

# We can remove the global db variable from here.
# db = None 

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    """
    load_dotenv() 
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not cred_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Please check your .env file.")

    cred = credentials.Certificate(cred_path)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    print("Firebase App initialized successfully.")

def get_db():
    """
    Returns an initialized Firestore client instance.
    This is a safer way to access the db client.
    """
    if not firebase_admin._apps:
        # This is a fallback in case the startup event failed silently.
        initialize_firebase()
    return firestore.client()