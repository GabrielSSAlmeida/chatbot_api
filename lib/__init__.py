from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from lib.configuration.config import Config
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from wit_alterado.wit_ import Wit
from flask_migrate import Migrate

#4AF23B6X4U6WQSQ2SW6M4V2ARIAKK4JT - Chatbot
#LV55LPSA5DDD3KRHYEU5GYXUD2AUHKIJ - Teste
client = Wit(access_token="LV55LPSA5DDD3KRHYEU5GYXUD2AUHKIJ")



#Inicializa todas a bibliotecas necessárias
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
ma = Marshmallow(app)
CORS(app)
migrate = Migrate(app, db)

#inicia o app Flask
db.init_app(app)

#importação das tabelas do banco de dados
from lib.models.access_db import AccessModel, access_share_schema, access_many_share_schema
from lib.models.intent_db import IntentModel, intent_share_schema, intent_many_share_schema
from lib.models.response_db import ResponseModel, response_share_schema, response_many_share_schema

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Access=AccessModel,
        Intent=IntentModel,
        Response=ResponseModel
    )

#Cria a database
with app.app_context():
    db.create_all()

#Cria a CronTask de apagar  audios a cada 20min
""" sched = BackgroundScheduler(daemon=True)
sched.add_job(CronTask.sensor,'interval',minutes=2)
sched.start() """