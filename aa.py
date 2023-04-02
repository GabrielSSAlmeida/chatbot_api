class GetAudioAnswer(Resource):
        def get(self):
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
                date_now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
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