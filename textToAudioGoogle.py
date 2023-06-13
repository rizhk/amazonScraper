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


df = pd.read_csv(TEXT_CSV_FILE, names=CSV_COLUMNS, skiprows=[0])

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



# audio = AudioSegment.from_mp3('welcome.mp3')
# new_file = speedup(audio,1.5,150)
# new_file.export("welcomeSpeedy.mp3", format="mp3")