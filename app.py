from lib import api, app

from lib.Routes.collect_wit import GetTextAnswer, GetAudioAnswer, AudioDownload, DeleteAudio
from lib.Routes.access_key import AccessLogin, AccessRegister, DeleteAccess
from lib.Routes.train_wit import AddIntent, DeleteIntent, EditResponses, TrainBot, DeleteUtterance
from lib.Routes.get_infos import GetAllIntents, GetAllUtterances, GetResponsesIntent


#TIRAR MODO DEBUG
#MUDAR SECRET KEY
#COLOCAR GIT IGNORE

api.add_resource(GetTextAnswer, "/")
api.add_resource(GetAudioAnswer, "/audio")
api.add_resource(AudioDownload, "/audio/download")
api.add_resource(DeleteAudio, "/audio/delete")

api.add_resource(AccessRegister, "/register")
api.add_resource(AccessLogin, "/login")
api.add_resource(DeleteAccess, "/delete_access")


api.add_resource(AddIntent, "/intent")
api.add_resource(DeleteIntent, "/delete/<string:intentName>")
api.add_resource(EditResponses, "/edit")
api.add_resource(TrainBot, "/train")
api.add_resource(DeleteUtterance, "/delete_utterance")


api.add_resource(GetAllIntents, "/get_intents")
api.add_resource(GetAllUtterances, "/get_utterances/<int:numberOfUtterances>")
api.add_resource(GetResponsesIntent, "/get_response")


if __name__ == "__main__":
    app.run(debug=True)