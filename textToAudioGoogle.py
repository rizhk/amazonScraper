import gtts
# from pydub import AudioSegment
# from pydub.effects import speedup
import csv
import os
import pandas as pd
import nltk
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


AUTDIOS_FOLDER = os.getcwd() + '/data/audios/'
TEXT_CSV_FILE = os.getcwd() + '/data/text.csv'
COLUMNS = [
    'text',
    'prododuct_link',
    'audio_name',
    'status'
]

textIndex = COLUMNS.index('text')
productLinkIndex = COLUMNS.index('prododuct_link')
audioNameIndex = COLUMNS.index('audio_name')
statusIndex = COLUMNS.index('status')

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)


df = pd.read_csv(TEXT_CSV_FILE, names=COLUMNS, skiprows=[0])
print(df)
for index, row in df.iterrows():
    # print(row.tolist())
    if(df['status'][index] == 'complete' ):
        continue
    t1 = gtts.gTTS(text=row[textIndex], lang='en', slow=False)
    audio_file = row[audioNameIndex]+ '.wav'
    audio_file_path = AUTDIOS_FOLDER + audio_file
    t1.save(audio_file)
    os.rename(audio_file, audio_file_path)
    df['status'][index] = 'complete'
df.to_csv(TEXT_CSV_FILE, index=False, header=False)


# exit program in python
exit()

with open(TEXT_CSV_FILE, 'w+') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        if line[statusIndex] == 'completed':
            continue
        t1 = gtts.gTTS(text=line[textIndex], lang='en', slow=False)
        t1.save(AUTDIOS_FOLDER + line[audioNameIndex])

        # file1 = drive.CreateFile({'title': line[audioNameIndex]})
        # file1.SetContentFile(AUTDIOS_FOLDER + line[audioNameIndex])
        # file1.Upload()
        # f = None



# audio = AudioSegment.from_mp3('welcome.mp3')
# new_file = speedup(audio,1.5,150)
# new_file.export("welcomeSpeedy.mp3", format="mp3")