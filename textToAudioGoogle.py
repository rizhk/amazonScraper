import gtts
import os
import pandas as pd
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from config import TEXT_CSV_FILE, CSV_COLUMNS, AUTDIOS_FOLDER


textIndex = CSV_COLUMNS.index('text')
productLinkIndex = CSV_COLUMNS.index('prododuct_link')
audioNameIndex = CSV_COLUMNS.index('audio_name')
statusIndex = CSV_COLUMNS.index('status')

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)
class TextToAudio:

    def __init__(self):
        self.df = pd.read_csv(TEXT_CSV_FILE, names=CSV_COLUMNS, skiprows=[0])


    def __textToAudio(self, text, lang='en', slow=False, folderName="", fileName=0):
        fullPath = AUTDIOS_FOLDER + folderName + '/'
        if not os.path.exists(fullPath):
            os.makedirs(fullPath)

        t1 = gtts.gTTS(text=text, lang=lang, slow=slow)
        audio_file = str(fileName) + '.wav'
        audio_file_path = fullPath + audio_file
        t1.save(audio_file)
        os.rename(audio_file, audio_file_path)
        return audio_file_path
    
    def convert(self):
        for index, row in self.df.iterrows():
            if(self.df['status'][index] == 'complete' ):
                continue
            self.__textToAudio(row[textIndex], folderName = row[audioNameIndex], fileName=index)
            self.df['status'][index] = 'complete'
        self.df.to_csv(TEXT_CSV_FILE, index=False, header=False)


if __name__ == "__main__":
    textToAudio = TextToAudio()
    textToAudio.convert()



# audio = AudioSegment.from_mp3('welcome.mp3')
# new_file = speedup(audio,1.5,150)
# new_file.export("welcomeSpeedy.mp3", format="mp3")