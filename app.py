from flask import Flask, request, make_response, jsonify, send_from_directory
from wit_alterado import Wit
import json, shutil, random, tempfile, os
from gtts import gTTS
from flask_cors import CORS

#4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT - Chatbot
#LV55LPSA5DDD3KRHYEU5GYXUD2AUHKIJ - Teste
client = Wit(access_token="4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT")
app = Flask(__name__)

CORS(app)

language = 'pt'
tld = 'com.br'


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


#Criar o audio - Pegar um ID, Criar audios com final 1,2,3...
@app.route('/audio', methods=['GET'])
def get_audio_answer():
    if request.method == 'GET':
        filename = "audio0.mp3"
        numero = int(filename[-5:-4])

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
        if not os.path.isdir('./audios'):
            os.mkdir('./audios')
        

        while os.path.isfile('./audios/'+filename):        
            numero += 1
            filename = filename[:5] + str(numero)+'.mp3'
 
        audioObj.save('./audios/'+filename)


        response['audio'] = "https://flask-api-chatobot.onrender.com/audio/download?filename=" + filename

        return make_response(
            jsonify(response)
        )

    
#Enviar o audio 
@app.route('/audio/download', methods=['GET'])
def get_audio_download():
    if request.method == 'GET':
        nameFile = request.args.get('filename')
        return send_from_directory('./audios/', nameFile, as_attachment=False)

#Deletar o audio 
@app.route('/audio/delete/', methods=['GET'])
def delete_audio():
    if request.method == 'GET':
        dirName = request.args.get('dirname')
        if os.path.isdir(dirName):#se existe o diretorio
            shutil.rmtree(dirName)
            return ('', 204)
        else:
            return ('', 404)


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
                tam = len(responseArray)- 1
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
                if intent in dados:
                    #escreve nesse json
                    tam = len(responseArray)- 1
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
        
#função que verifica se existe uma intenção
def verify_intent(intentName):
    intents = client.intent_list()
    for intent in intents:
        if intent['name'] == intentName:
            return True #Existe a intenção
    
    return False#não existe a intenção

#Criar intenção no Wit
@app.route('/intent', methods=['POST'])
def post_intent():
    if request.method == 'POST':
        try:
            responseJson = request.get_json()
            intentName = responseJson['name']

            if(verify_intent(intentName)):
                return 'Intent já existe'

            witResponse = client.create_intent(intentName)
            #print(witResponse)Não sei se vai precisar deste ID.
            finalReturn = witResponse['id']+"-"+witResponse['name']
            return finalReturn
        except:
            return 'Erro'    

#Enviar as perguntas para treinar o bot
@app.route('/train', methods=['POST'])
def post_utterances():
    if request.method == 'POST':
        try:
            utterances = request.get_json()
            #Verificando se a intenção existe (Add para entidade caso precise)
            for utterance in utterances:
                if(not verify_intent(utterance['intent'])): #Se não existe a intent, retorna o erro
                    return 'Alguma intent enviada não existe'
                
            witResponse = client.train(utterances)
            return witResponse
        
        except Exception as e:
            print(e)
            return 'Error'
    

#deletar uma intent
#OBS: TIVE QUE ALTERAR O ARQUIVO WIT, POIS TINHA UM ERRO COM A FUNÇÃO 'urllib.quote_plus()'
#A IMPORTAÇÃO MUDOU PARAR 'import urllib.parse' e a chamada foi para 'urllib.parse.quote_plus()'
@app.route('/delete/<string:intentName>', methods=['DELETE'])
def delete_intent(intentName):
    try:
        if request.method == 'DELETE':
            if(verify_intent(intentName)):
                witResponse = client.delete_intent(intentName)
                return witResponse
            
            return 'Intent não existe'
    except Exception as e:
            print(e)
            return 'Error'        

        

#deletar uma utterance
@app.route('/delete/utterance', methods=['DELETE'])
def delete_utterance():
    if request.method == 'DELETE':
        try:
            utterances = request.get_json()
            utterances_array = [] #Array de strings com as utterances que deseja excluir
            for utterance in utterances:
                utterances_array.append(utterance['text'])

            witResponse = client.delete_utterances(utterances_array)
            return witResponse
        except Exception as e:
            print(e)
            return 'Error'

#get all intents
@app.route('/get_intents', methods=['GET'])
def get_intents():
    if request.method == 'GET':
        try:
            return client.intent_list()
        except Exception as e:
            print(e)
            return 'Error'

#get all utterances
#numberOfUtterances <Obrigatorio>= Numero de Utterances(Mensagens de treinamento) maximos que deve receber entre 1 a 10000.
@app.route('/get_utterances/<int:numberOfUtterances>', methods=['GET'])
def get_utterances(numberOfUtterances):
    if request.method == 'GET':
        try:
            intentName = request.args.get('intent')
            return client.get_utterances(limit= numberOfUtterances,intents=[intentName])
        except Exception as e:
            print(e)
            return 'Error'
        

#get all response
@app.route('/get_response', methods=['GET'])
def get_response():
    if request.method == 'GET':
        try:
            intentName = request.args.get('intent')
            file = open("answer.json", encoding="utf-8")
            aswr = json.load(file)
            response = aswr[intentName]['response']
            return make_response(
                jsonify(response)
            )
        except Exception as e:
            print(e)
            return 'Error'

app.run(debug=True)