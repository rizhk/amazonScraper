# Description : Download images from pexels.com and save them into a folder
import requests
from pexels_api import API
from config import API_KEY_PEXELS, IMAGES_FOLDER, CSV_COLUMNS, TEXT_CSV_FILE
import spacy
import pandas as pd
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag



# Load the English language model
nlp = spacy.load("en_core_web_lg")

textIndex = CSV_COLUMNS.index('text')
productLinkIndex = CSV_COLUMNS.index('prododuct_link')
audioNameIndex = CSV_COLUMNS.index('audio_name')
statusIndex = CSV_COLUMNS.index('status')


    

def getSentences(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

def getPartsOfSpeech(sentence):
    doc = nlp(sentence)
    # Get the parts of speech
    # token.pos_ is POS tag and token.text is the word
    return [(token.pos_, token.text  )for token in doc]

def getNamedEntityRelationships(sentence):
    doc = nlp(sentence)
    ner = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    return ner


def getEntitiesFromNltk(sentence):
    # Tokenize the text
    tokens = word_tokenize(sentence)

    # Perform part-of-speech tagging
    pos_tags = pos_tag(tokens)

    # Perform named entity recognition
    ner_tags = ne_chunk(pos_tags)

    # Extract named entities
    entities = []
    for chunk in ner_tags:
        print(chunk)
        if hasattr(chunk, 'label'):
            entities.append((chunk.label(), ' '.join(c[0] for c in chunk)))

    return entities

def getWordsForImageSearch(text):
    sentences = getSentences(text)
    sentence_dict = {}

    for sentenceIndex, sentence in enumerate(sentences):
        partsOfSpeech = getPartsOfSpeech(sentence)
        words_list = []
        for index, (wordType, word) in enumerate(partsOfSpeech):
            main_word = ''
            if(wordType == 'NOUN'):
                # check if previous tuple in partsOfSpeech is ADJ
                # if yes, then append that word with this word
                if(index > 0 and partsOfSpeech[index-1][0] == 'ADJ'):
                    main_word = partsOfSpeech[index-1][1] + ' ' + word
                else:
                    main_word = word
                words_list.append(main_word)
                
        sentence_dict[sentenceIndex] = words_list

        print(sentence_dict)

    return sentence_dict
        # entities = getNamedEntityRelationships(sentence)
        # print(len(entities))
        # if(len(entities) == 0):
        #     # get entities from nltk
        #     entities = getEntitiesFromNltk(text)

        # for entity in entities:
        #     print(entity)
        #     # if(entity[0] == 'PERSON'):
        #     #     getImagesFromText(entity[1])    

def imagesBasedOnSearchedWords():
    df = pd.read_csv(TEXT_CSV_FILE, names=CSV_COLUMNS, skiprows=[0])

    for index, row in df.iterrows():
        # print(row.tolist())
        if(df['status'][index] == 'complete' ):
            continue
        words_dict = getWordsForImageSearch(row[textIndex])
        for sentenceIndex, words_list in words_dict.items():
            for word in words_list:
                getImagesFromText(word)
        df['status'][index] = 'complete'
    df.to_csv(TEXT_CSV_FILE, index=False, header=False)



def getImagesFromText(main_word, category= 'technology'):
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
    # getImagesFromText('tablets', 'technology')
    imagesBasedOnSearchedWords()

