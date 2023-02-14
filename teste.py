from gtts import gTTS
  
import os
  
mytext = 'Assista o vídeo tutorial para entender melhor.😀👽👻'
  

language = 'pt'
tld = 'com.br'

myobj = gTTS(text=mytext, lang=language, slow=False, tld=tld)
  

myobj.save("welcome.mp3")

