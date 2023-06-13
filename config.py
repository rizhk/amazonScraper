import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.dev')

cwd = os.getcwd() # current working directory

API_KEY_PEXELS = os.getenv("API_KEY_PEXELS")
TEXT_CSV_FILE = cwd + '/data/text.csv'
IMAGES_FOLDER = cwd + '/data/images/'
AUTDIOS_FOLDER = cwd + '/data/audios/'
CSV_COLUMNS = ['text', 'prododuct_link', 'audio_name', 'status']