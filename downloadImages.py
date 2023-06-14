# Description : Download images from pexels.com and save them into a folder
import requests
from pexels_api import API
from config import API_KEY_PEXELS, IMAGES_FOLDER, CSV_COLUMNS, TEXT_CSV_FILE
import spacy
import pandas as pd

# Load the English language model
nlp = spacy.load("en_core_web_sm")

textIndex = CSV_COLUMNS.index('text')
productLinkIndex = CSV_COLUMNS.index('prododuct_link')
audioNameIndex = CSV_COLUMNS.index('audio_name')
statusIndex = CSV_COLUMNS.index('status')
    

def getSentences(text):
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]
    return sentences

def getPartsOfSpeech(sentence):
    doc = nlp(sentence)
    # Get the parts of speech
    # token.pos_ is POS tag and token.text is the word
    return [token for token in doc]

def getNamedEntityRelationships(sentence):
    doc = nlp(sentence)
    ner = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    return ner

def getWordsForImageSearch(text):
    sentences = getSentences(text)
    print(sentences)
    for sentence in sentences:
        words = getPartsOfSpeech(sentence.doc)
        entities = getNamedEntityRelationships(sentence)
        print(words)
        print(entities)


def imagesBasedOnSearchedWords():
    df = pd.read_csv(TEXT_CSV_FILE, names=CSV_COLUMNS, skiprows=[0])

    for index, row in df.iterrows():
        # print(row.tolist())
        if(df['status'][index] == 'complete' ):
            continue
        getWordsForImageSearch(row[textIndex])
        df['status'][index] = 'complete'
    df.to_csv(TEXT_CSV_FILE, index=False, header=False)



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
    # downloadAndSaveImage('tablets', 'technology')
    imagesBasedOnSearchedWords()

