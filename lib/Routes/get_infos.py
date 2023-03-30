from flask import request, make_response, jsonify
from flask_restful import Resource
from lib import client
import json, tempfile, shutil
from useful_variables import UsefulVariables

from lib.auth.authenticate import jwt_required

#get todas as intents do wit
class GetAllIntents(Resource):
    def get(self, current_user):
        try:
            return client.intent_list()
        except Exception as e:
            print(e)
            return 'Error'


#get all utterances do wit
#numberOfUtterances <Obrigatorio>= Numero de Utterances(Mensagens de treinamento) maximos que deve receber entre 1 a 10000.
class GetAllUtterances(Resource):
    def get(self, numberOfUtterances, current_user):
        try:
            intentName = request.args.get('intent')
            return client.get_utterances(limit= numberOfUtterances,intents=[intentName])
        except Exception as e:
            print(e)
            return 'Error'

#get todas as respostas do json
class GetResponsesIntent(Resource):
    def get(self, current_user):
        try:
            intentName = request.args.get('intent')
            file = open(UsefulVariables.PATH_ANSWER, encoding="utf-8")
            aswr = json.load(file)
            response = aswr[intentName]['response']
            return make_response(
                jsonify(response)
            )
        except Exception as e:
            print(e)
            return 'Error'