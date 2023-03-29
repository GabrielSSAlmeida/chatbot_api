from flask import request, jsonify, make_response, send_from_directory
from flask_restful import Resource
from app import client
from gtts import gTTS
import json, random, os, shutil
from useful_variables import UsefulVariables
from datetime import datetime


from app.auth.authenticate import jwt_required


class GetTextAnswer(Resource):
    @jwt_required
    def get(self, current_user):
        contentUserMessage = request.args.get('text')
        data_message = client.message(contentUserMessage)

        intent = data_message.get("intents")[0].get("name")
        intent_confidence = data_message.get("intents")[0].get("confidence")
        
        file = open(UsefulVariables.PATH_ANSWER, encoding="utf-8")
        aswr = json.load(file)

        if(intent_confidence > 0.6):
            tam = aswr[intent]["tam"]
            response = aswr[intent]["response"][random.randint(0, tam)]
        else:
            response = aswr["erro"]

        return make_response(
            jsonify(response)
        )
    
class GetAudioAnswer(Resource):
        @jwt_required
        def get(self, current_user):
            filename = "audio0.mp3"
            numero = int(filename[-5:-4])

            contentUserMessage = request.args.get('text')
            data_message = client.message(contentUserMessage)
            intent = data_message.get("intents")[0].get("name")


            intent_confidence = data_message.get("intents")[0].get("confidence")
            file = open(UsefulVariables.PATH_ANSWER, encoding="utf-8")
            aswr = json.load(file)

            if(intent_confidence > 0.6):
                tam = aswr[intent]["tam"]
                response = aswr[intent]["response"][random.randint(0, tam)]
            else:
                response = aswr["erro"]


            mytext = response["text"]
            audioObj = gTTS(text=mytext, lang=UsefulVariables.LANGUAGE, slow=False, tld=UsefulVariables.TLD)

            #arquivo de data
            if not os.path.isdir(UsefulVariables.UsefulVariables.PATH_AUDIOS):
                os.mkdir(UsefulVariables.PATH_AUDIOS)
                date_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                arquivo = open(UsefulVariables.PATH_AUDIOS+"/date.txt", "a")
                arquivo.write(str(date_now))
            
            
            while os.path.isfile(os.path.join(UsefulVariables.PATH_AUDIOS, filename)):        
                numero += 1
                filename = filename[:5] + str(numero)+'.mp3'
    
        
            audioObj.save(os.path.join(UsefulVariables.PATH_AUDIOS, filename))


            response['audio'] = UsefulVariables.API_URL+"audio/download?filename=" + filename

            return make_response(
                jsonify(response)
            )
        
class AudioDownload(Resource):
    @jwt_required
    def get(self, current_user):
        nameFile = request.args.get('filename')
        return send_from_directory(UsefulVariables.PATH_AUDIOS, nameFile, as_attachment=False)

class DeleteAudio(Resource):
    @jwt_required
    def get(self, current_user):
        dirName = request.args.get('dirname')
        final_dirname = os.path.join(UsefulVariables.BASENAME_DIRECTORY, dirName)
        if os.path.isdir(final_dirname):#se existe o diretorio
            shutil.rmtree(final_dirname)
            return ('', 204)
        else:
            return ('', 404)