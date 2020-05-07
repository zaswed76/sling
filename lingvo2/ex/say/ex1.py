# import gtts
from gtts import gTTS

from textblob import TextBlob

line = "cat"


lang = TextBlob(line).detect_language()



print(lang)


tts = gTTS(line, lang=lang)
tts.save('tts_output{}.mp3'.format(line))


