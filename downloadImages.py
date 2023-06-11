import os
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path='.env.dev')

API_KEY_PEXELS = os.getenv("API_KEY_PEXELS")
TEXT_CSV_FILE = os.getcwd() + os.getenv("TEXT_CSV_FILE")
IMAGES_FOLDER = os.getcwd() + os.getenv("IMAGES_FOLDER")

def downloadAndSaveImage(query):
    api = API(API_KEY_PEXELS)
    api.search(query, page=1, results_per_page=5)
    photos = api.get_entries()
    for photo in photos:
        imgUrl = photo.compressed if photo.compressed else photo.medium
        saveImageIntoFile(imgUrl)

def saveImageIntoFile(imgUrl):
    print(imgUrl)
    imageUrlParts = imgUrl.split('/')
    lastIndex = len(imageUrlParts) - 1
    imageName = imageUrlParts[lastIndex]
    imageNameIndex = imageName.find('jpeg')
    imageNameCleaned = imageName[:imageNameIndex] + 'jpeg'

    response = requests.get(imgUrl)
    if response.status_code:
        fp = open(IMAGES_FOLDER + imageNameCleaned, 'wb')
        fp.write(response.content)
        fp.close()
    


if __name__ == "__main__":
    downloadAndSaveImage('computers: tablets')



# API()

# df = pd.read_csv(TEXT_CSV_FILE, names=COLUMNS, skiprows=[0])
# print(df)
# for index, row in df.iterrows():
#     # print(row.tolist())
#     if(df['status'][index] == 'complete' ):
#         continue
#     t1 = gtts.gTTS(text=row[textIndex], lang='en', slow=False)
#     audio_file = row[audioNameIndex]+ '.wav'
#     audio_file_path = AUTDIOS_FOLDER + audio_file
#     t1.save(audio_file)
#     os.rename(audio_file, audio_file_path)
#     df['status'][index] = 'complete'
# df.to_csv(TEXT_CSV_FILE, index=False, header=False)
