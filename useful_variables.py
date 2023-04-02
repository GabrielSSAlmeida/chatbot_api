from pathlib import Path
import os

caminho_projeto = Path()

class UsefulVariables:

    LANGUAGE = 'pt'
    TLD = 'com.br'
    BASENAME_DIRECTORY = caminho_projeto.absolute()
    API_URL = "https://flask-api-chatobot.onrender.com/"
    PATH_AUDIOS = os.path.join(BASENAME_DIRECTORY, "audios")

    MESSAGE_ERRO = {
                "value":"Não foi possível entender ou não possuímos resposta para essa pergunta. Por favor, pergunte outra coisa",
                "type":"text"
            }
    

