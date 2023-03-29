from flask import request
from flask_restful import Resource
from lib import client
import json, tempfile, shutil
from useful_variables import UsefulVariables

from lib.auth.authenticate import jwt_required



#função que verifica se existe uma intenção
def verify_intent(intentName):
    intents = client.intent_list()
    for intent in intents:
        if intent['name'] == intentName:
            return True #Existe a intenção
    
    return False#não existe a intenção



#Adiciona intent no wit e no json
class AddIntent(Resource):
    @jwt_required
    def post(self, current_user):
        try:     
            #Pega o json pelo POST
            responseJson = request.get_json()
            intentName = responseJson['name']
            responseArray = responseJson['response']

            if(verify_intent(intentName)):
                return 'Intent já existe'
            
            #Cria a intent no wit
            witResponse = client.create_intent(intentName)
            if not "id" or not "name" in witResponse:
                return 'Erro ao criar intent'

            finalReturn = witResponse['id']+"-"+witResponse['name']
            
            #Cria a intent com as respostas no json
            #cria um arquivo json temporario
            with open(UsefulVariables.PATH_ANSWER, 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                dados = json.load(arq)
                #escreve nesse json
                tam = len(responseArray)- 1
                dados[intentName] = {
                    "tam": tam,
                    "response": responseArray
                }

                json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))

            # se tudo deu certo, renomeia o arquivo temporário
            shutil.move(tmpfile.name, UsefulVariables.PATH_ANSWER)

            return finalReturn

        except Exception as e:
            print(e)
            return 'Error'
        


#deleta intent no wit e no json
#OBS: TIVE QUE ALTERAR O ARQUIVO WIT, POIS TINHA UM ERRO COM A FUNÇÃO 'urllib.quote_plus()'
#A IMPORTAÇÃO MUDOU PARAR 'import urllib.parse' e a chamada foi para 'urllib.parse.quote_plus()'
class DeleteIntent(Resource):
    @jwt_required
    def delete(self, intentName, current_user):
        try:
            if(verify_intent(intentName)):
                witResponse = client.delete_intent(intentName)

                if witResponse["deleted"] != intentName:
                    return 'Erro ao apagar Intent'

                #cria um arquivo json temporario
                with open(UsefulVariables.PATH_ANSWER, 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                    dados = json.load(arq)
                    if intentName in dados:
                        dados.pop(intentName, None)

                        json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))
                    else:
                        return 'Erro'
                # se tudo deu certo, renomeia o arquivo temporário
                shutil.move(tmpfile.name, UsefulVariables.PATH_ANSWER)

                return witResponse
            
            return 'Intent não existe'
        except Exception as e:
                print(e)
                return 'Error'
        



#edita as respostas no json
class EditResponses(Resource):
    @jwt_required
    def put(self, current_user):
        try:     
            responseJson = request.get_json()
            intentName = responseJson['name']
            responseArray = responseJson['response']

             #cria um arquivo json temporario
            with open(UsefulVariables.PATH_ANSWER, 'r', encoding="utf-8") as arq, tempfile.NamedTemporaryFile('w', delete=False, encoding="utf-8") as tmpfile:
                dados = json.load(arq)
                if intentName in dados:
                    #escreve nesse json
                    tam = len(responseArray)- 1
                    dados[intentName] = {
                        "tam": tam,
                        "response": responseArray
                    }

                    json.dump(dados, tmpfile, ensure_ascii=False, indent=4, separators=(',',':'))
                else:
                    return 'Erro'
            # se tudo deu certo, renomeia o arquivo temporário
            shutil.move(tmpfile.name, UsefulVariables.PATH_ANSWER)


            return 'sucess'
        except Exception as e:
            print(e)
            return 'Error'
        



#Enviar as perguntas(Utterances) para treinar o bot
class TrainBot(Resource):
    @jwt_required
    def post(self, current_user):
        try:
            utterances = request.get_json()
            #Verificando se a intenção existe (Add entidade caso precise)
            for utterance in utterances:
                if(not verify_intent(utterance['intent'])): #Se não existe a intent, retorna o erro
                    return 'Alguma intent enviada não existe'
                
            witResponse = client.train(utterances)
            return witResponse
        
        except Exception as e:
            print(e)
            return 'Error'
        
        

class DeleteUtterance(Resource):
    @jwt_required
    def delete(self, current_user):
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
