# Description : Download images from pexels.com and save them into a folder
import requests
from pexels_api import API
from config import API_KEY_PEXELS, IMAGES_FOLDER, CSV_COLUMNS
import spacy


# Load the English language model
nlp = spacy.load("en_core_web_sm")

textIndex = CSV_COLUMNS.index('text')
productLinkIndex = CSV_COLUMNS.index('prododuct_link')
audioNameIndex = CSV_COLUMNS.index('audio_name')
statusIndex = CSV_COLUMNS.index('status')

def getSentences(text):
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences


def downloadAndSaveImage(main_word, category= 'technology'):
    api = API(API_KEY_PEXELS)
    query = f"{main_word} +: {category}"
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
    downloadAndSaveImage('tablets', 'technology')



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
