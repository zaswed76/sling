
from gtts import gTTS
for i in range(10):
    tts = gTTS('This my cat', lang='en')
    tts.save('tts_output{}.mp3'.format(str(i)))