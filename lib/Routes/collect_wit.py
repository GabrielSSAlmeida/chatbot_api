from flask import request, jsonify, make_response, send_from_directory
from flask_restful import Resource
from lib import client
from gtts import gTTS
import random, os
from useful_variables import UsefulVariables
from datetime import datetime, timedelta
from lib.models.intent_db import IntentModel
from lib.models.response_db import ResponseModel, response_many_share_schema
from apscheduler.schedulers.background import BackgroundScheduler
from lib.cron_task import CronTask


class GetTextAnswer(Resource):
    def get(self):
        contentUserMessage = request.args.get('text')
        data_message = client.message(contentUserMessage)

        intent = data_message.get("intents")[0].get("name")
        intent_confidence = data_message.get("intents")[0].get("confidence")
        
        intentNameWit = intent.split('_')
        
        intentName = intentNameWit[0]
        programId = intentNameWit[1]

        if(intent_confidence > 0.6):
            search_intent = IntentModel.find_by_name_program(name=intentName, program=programId)

            if search_intent:
                intentId = search_intent.id

                search_response = response_many_share_schema.dump(
                    ResponseModel.find_by_intent_id(intent_id=intentId)
                )
                if search_response:
                    tam = len(search_response)
                    response = search_response[random.randint(0, tam-1)]
                    response.pop('id')
                

            else:
                response = jsonify({"erro": "Intent não encontrada"})
                response.status_code = 400
                return response   
        else:
            response = UsefulVariables.MESSAGE_ERRO

        return make_response(
            jsonify(response)
        )
    
class GetAudioAnswer(Resource):
        def get(self):
            contentUserMessage = request.args.get('text')
            data_message = client.message(contentUserMessage)

            intent = data_message.get("intents")[0].get("name")
            intent_confidence = data_message.get("intents")[0].get("confidence")
            
            intentNameWit = intent.split('_')
            
            intentName = intentNameWit[0]
            programId = intentNameWit[1]

            if(intent_confidence > 0.6):
                search_intent = IntentModel.find_by_name_program(name=intentName, program=programId)

                if search_intent:
                    intentId = search_intent.id

                    search_response = response_many_share_schema.dump(
                        ResponseModel.find_by_intent_id(intent_id=intentId)
                    )
                    if search_response:
                        tam = len(search_response)
                        response = search_response[random.randint(0, tam-1)]
                        response.pop('id')
                    

                else:
                    response = jsonify({"erro": "Intent não encontrada"})
                    response.status_code = 400
                    return response   
            else:
                response = UsefulVariables.MESSAGE_ERRO

            if response['type'] == "text":
                mytext = response["value"]
            else:
                mytext = response["description"]
            audioObj = gTTS(text=mytext, lang=UsefulVariables.LANGUAGE, slow=False, tld=UsefulVariables.TLD)

            #Cria pasta de audio caso nao exista
            if not os.path.isdir(UsefulVariables.PATH_AUDIOS):
                os.mkdir(UsefulVariables.PATH_AUDIOS)
            
            #O nome do arquivo tem a data de criação
            date_now = datetime.now().strftime('%d-%m-%Y-%H.%M.%S.%f')
            filename = f"audio{date_now}.mp3"

            #salva o arquivo de audio
            audioObj.save(os.path.join(UsefulVariables.PATH_AUDIOS, filename))
            future20min = (datetime.now() + timedelta(minutes=20)).replace(fold=1).strftime('%Y-%m-%d %H:%M:%S')

            sched = BackgroundScheduler(daemon=True)
            sched.add_job(func = CronTask.deleteAudio,trigger='date',next_run_time= future20min, args=[filename])
            sched.start()


            response['audio'] = UsefulVariables.API_URL+"audio/download?filename=" + filename

            return make_response(
                jsonify(response)
            )
        

class AudioDownload(Resource):
    def get(self):
        nameFile = request.args.get('filename')
        return send_from_directory(UsefulVariables.PATH_AUDIOS, nameFile, as_attachment=False)

""" class DeleteAudio(Resource):
    def get(self):
        dirName = request.args.get('dirname')
        final_dirname = os.path.join(UsefulVariables.BASENAME_DIRECTORY, dirName)
        if os.path.isdir(final_dirname):#se existe o diretorio
            shutil.rmtree(final_dirname)
            return ('', 204)
        else:
            return ('', 404) """