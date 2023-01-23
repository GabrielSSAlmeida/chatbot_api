from flask import Flask, request, make_response, jsonify
from wit import Wit
import json
import random


client = Wit(access_token="4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT")
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_answer():
    contentUserMessage = request.args.get('text')
    data_message = client.message(contentUserMessage)
    intent = data_message.get("intents")[0].get("name")

    file = open("answer.json")
    aswr = json.load(file)
    tam = aswr[intent]["tam"]
    response = aswr[intent]["response"][random.randint(0, tam)]


    return make_response(
        jsonify(response)
    )
    
    
    
    
app.run(debug=False)