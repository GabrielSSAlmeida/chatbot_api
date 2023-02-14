from flask import Flask, request, make_response, jsonify
from wit import Wit
import json
import random


client = Wit(access_token="LV55LPSA5DDD3KRHYEU5GYXUD2AUHKIJ")
app = Flask(__name__)

#ver a confiança da intent enviada
#tentar mexer com entities
@app.route('/', methods=['GET'])
def get_answer():
    contentUserMessage = request.args.get('text')
    
    data_message = client.message(contentUserMessage)
    print(data_message)
    entities = data_message.get("entities")



    intent = data_message.get("intents")[0].get("name")
    intent_confidence = data_message.get("intents")[0].get("confidence")
    file = open("answer.json", encoding="utf-8")
    aswr = json.load(file)

    if(intent_confidence > 0.6):
        if(not bool(entities)):
            tam = aswr[intent]["tam"]
            response = aswr[intent]["response"][random.randint(0, tam)]
        else:
            maior_confidence = 0
            entity = ""

            for e in entities:
                confidence = entities.get(e)[0].get('confidence')
                if(confidence > maior_confidence):
                    maior_confidence = confidence
                    entity = entities.get(e)[0].get('name')

            tam = aswr[intent][entity]["tam"]
            response = aswr[intent][entity]["response"][random.randint(0, tam)]
    else:
        response = aswr["erro"]

    return make_response(
        jsonify(response)
    )


@app.route('/teste', methods=['POST'])
def post_intent():
    try:
        json = request.get_json()
        contentUserMessage = json['name']
        resp = client.create_intent(contentUserMessage)
        response = resp['id']+"-"+resp['name']
        return response
    except:
        return 'Erro'


@app.route('/teste/entidade', methods=['POST'])
def post_entity():
    
    try:
        json = request.get_json()
        name = json['name']
        roles = json['roles']
        lookups = json['lookups']
        keywords = json['keywords']
        resp1 = client.create_entity(name, roles, lookups)
        """ print("\n\n", keywords, "\n\n")
        for keyword in keywords:
            print("\n\n", keyword, "\n\n")
            resp2 = client.add_keyword_value(name, keyword)
        print(resp2) """
        return  resp1 
    except:
        return 'Erro'

@app.route('/teste/train', methods=['POST'])
def post_utterances():
    
    try:
        json = request.get_json()
        resp1 = client.train(json)
        return resp1
    except:
        return 'Erro'

app.run(debug=False, host='0.0.0.0')