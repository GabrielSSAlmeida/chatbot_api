from flask import Flask, request, make_response, jsonify, send_from_directory
from wit import Wit
import json, shutil, random, tempfile, os
from gtts import gTTS


client = Wit(access_token="4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT")
app = Flask(__name__)


language = 'pt'
tld = 'com.br'
filename = "audio.mp3"

##Para resposta em texto
@app.route('/', methods=['GET'])
def get_answer():
    if request.method == 'GET':
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
    if request.method == 'GET':
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


        response['audio'] = "http://192.168.1.2:5000/audio/download?filename=" + filename

        print(response)
        return make_response(
            jsonify(response)
        )

    
#Enviar o audio 
@app.route('/audio/download', methods=['GET'])
def get_audio_download():
    if request.method == 'GET':
        nameFile = request.args.get('filename')
        return send_from_directory('./audios/', nameFile, as_attachment=False)


@app.route('/addJson', methods=['POST'])
def add_intent_answer_json():
    if request.method == 'POST':
        try:
            #Pega o json pelo POST
            responseJson = request.get_json()
            intentName = responseJson['intent']
            responseArray = responseJson['response']
            #cria um arquivo json temporario
            with open('answer.json', 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                dados = json.load(arq)
                #escreve nesse json
                tam = len(responseArray)
                dados[intentName] = {
                    "tam": tam,
                    "response": responseArray
                }

                json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))

            # se tudo deu certo, renomeia o arquivo temporário
            shutil.move(tmpfile.name, 'answer.json')

            return 'sucess'
            
        except:
            return 'Erro'

#edita as respostas
@app.route('/editJson/<string:intent>', methods=['PUT'])
def edit_answer_json(intent):
    if request.method == 'PUT':
        try:
            #Pega o json pelo PUT
            responseJson = request.get_json()           
            responseArray = responseJson['response']

            #cria um arquivo json temporario
            with open('answer.json', 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                dados = json.load(arq)
                print(dados)
                print(intent)
                if intent in dados:
                    #escreve nesse json
                    tam = len(responseArray)
                    dados[intent] = {
                        "tam": tam,
                        "response": responseArray
                    }

                    json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))
                else:
                    return 'Erro'
            # se tudo deu certo, renomeia o arquivo temporário
            shutil.move(tmpfile.name, 'answer.json')

            return 'sucess'
        except:
            return 'Erro'

#apaga uma intent
@app.route('/deleteIntentJson/<string:intent>', methods=['DELETE'])
def delete_intent_json(intent):
    if request.method == 'DELETE':
        try:
            #cria um arquivo json temporario
            with open('answer.json', 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                dados = json.load(arq)
                print(dados)
                print(intent)
                if intent in dados:
                    dados.pop(intent, None)

                    json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))
                else:
                    return 'Erro'
            # se tudo deu certo, renomeia o arquivo temporário
            shutil.move(tmpfile.name, 'answer.json')

            return 'sucess'
        except:
            return 'Erro'
    

app.run(debug=True, host='0.0.0.0')