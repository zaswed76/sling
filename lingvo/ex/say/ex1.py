
# from gtts import gTTS
# for i in range(1):
#     tts = gTTS('This my cat', lang='en')
#     tts.save('tts_output{}.mp3'.format(str(i)))


import pyttsx3;
engine = pyttsx3.init();
engine.say("This my cat");
engine.runAndWait() ;