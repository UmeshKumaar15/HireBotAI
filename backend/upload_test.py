import firebase_admin
from firebase_admin import credentials, storage
import os
import json
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Load Firebase credentials from environment variables
def initialize_firebase():
    cred_dict_str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_DICT")
    if not cred_dict_str:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_DICT is not defined in the environment")

    try:
        cred_dict = json.loads(cred_dict_str)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in GOOGLE_APPLICATION_CREDENTIALS_DICT")

    # Initialize Firebase Admin SDK
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'storageBucket': cred_dict.get("project_id") + ".appspot.com"
        })

# Function to upload a file to Firebase Storage
def upload_to_firebase(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")

    try:
        # Initialize Firebase
        initialize_firebase()

        # Get the bucket
        bucket = storage.bucket()
        file_name = os.path.basename(file_path)

        # Create a blob and upload the file
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)

        # Get the public URL
        public_url = blob.public_url
        print(f"File uploaded successfully! Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error uploading file: {e}")

# Example usage
if __name__ == "__main__":
    file_path = input("Enter the full path to the file you want to upload: ")
    upload_to_firebase(file_path)
