from flask import Flask, request, make_response, jsonify, send_from_directory
from wit import Wit
import json
import random
from gtts import gTTS


client = Wit(access_token="LV55LPSA5DDD3KRHYEU5GYXUD2AUHKIJ")
app = Flask(__name__)


language = 'pt'
tld = 'com.br'
filename = "audio.mp3"

##Para resposta em texto
@app.route('/', methods=['GET'])
def get_answer():
    contentUserMessage = request.args.get('text')
    data_message = client.message(contentUserMessage)


    intent = data_message.get("intents")[0].get("name")
    intent_confidence = data_message.get("intents")[0].get("confidence")
    file = open("answer.json", encoding="utf-8")
    aswr = json.load(file)

    if(intent_confidence > 0.6):
        tam = aswr[intent]["tam"]
        response = aswr[intent]["response"][random.randint(0, tam)]
    else:
        response = aswr["erro"]

    return make_response(
        jsonify(response)
    )


#Criar o audio
@app.route('/audio', methods=['GET'])
def get_audio_answer():
    contentUserMessage = request.args.get('text')
    data_message = client.message(contentUserMessage)
    intent = data_message.get("intents")[0].get("name")


    intent_confidence = data_message.get("intents")[0].get("confidence")
    file = open("answer.json", encoding="utf-8")
    aswr = json.load(file)

    if(intent_confidence > 0.6):
        tam = aswr[intent]["tam"]
        response = aswr[intent]["response"][random.randint(0, tam)]
    else:
        response = aswr["erro"]


    mytext = response["text"]
    audioObj = gTTS(text=mytext, lang=language, slow=False, tld=tld)
    audioObj.save('./audios/'+filename)

    obj = {
        "value": "http://192.168.1.7:5000/audio/download?filename=" + filename,
        "type": "audio",
        "text": "Teste"
    }

    return make_response(
        jsonify(obj)
    )

    
#Enviar o audio 
@app.route('/audio/download', methods=['GET'])
def get_audio_download():
    nameFile = request.args.get('filename')
    return send_from_directory('./audios/', nameFile, as_attachment=False)


app.run(debug=True, host='0.0.0.0')