from flask import Flask, request, make_response, jsonify
import json
import random

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_answer():
    intent = request.args.get('text')
    file = open("answer.json")
    aswr = json.load(file)
    tam = aswr[intent]["tam"]
    response = aswr[intent]["response"][random.randint(0, tam)]
    return make_response(
        jsonify(response)
    )
    
app.run(host='0.0.0.0', debug=False)