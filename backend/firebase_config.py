import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load credentials from JSON file
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()