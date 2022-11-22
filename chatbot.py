from wit import Wit
import json
import random
client = Wit(access_token="4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT")

#Mensagem do cliente
#receber de um json
content = "Como mudar a foto de perfil?"
data_message = client.message(content)

intent = data_message.get("intents")[0].get("name")
""" entity = list(data_message['entities'])[0]
value = data_message['entities'][entity][0]['value']


print("\n\n")
print(data_message)
print("\n")
print(intent)
print("\n")
print(value)
 """

file = open("answer.json")

aswr = json.load(file)

tam = aswr[intent]["tam"]
response = aswr[intent]["response"][random.randint(0, tam)]

print(response)
