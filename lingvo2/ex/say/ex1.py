import gtts
from gtts import gTTS

from langdetect import detect

print(detect('cat'))



for i in ["кот который гуляет сам по себе"]:
    line = str(i)
    tts = gTTS(line, lang='ru')
    tts.save('tts_output{}.mp3'.format(line))


