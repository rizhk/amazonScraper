import os
from pexels_api import API
from dotenv import load_dotenv
import requests
from google.cloud import vision
from google.cloud.vision import types

load_dotenv(dotenv_path='.env.dev')

API_KEY_PEXELS = os.getenv("API_KEY_PEXELS")
TEXT_CSV_FILE = os.getcwd() + os.getenv("TEXT_CSV_FILE")
IMAGES_FOLDER = os.getcwd() + os.getenv("IMAGES_FOLDER")

# Set up credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

# Initialize client
client = vision.ImageAnnotatorClient()

# Load image
with open(IMAGES_FOLDER + 'pexels-photo-207589.jpeg', 'rb') as image_file:
    content = image_file.read()

# Create image object
image = types.Image(content=content)

# Make request to API
response = client.label_detection(image=image)
labels = response.label_annotations

# Print results
print('Labels:')
for label in labels:
    print(label.description)