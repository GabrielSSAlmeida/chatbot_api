import shutil, os
from datetime import timedelta, datetime

class CronTask:
    def sensor():
        if os.path.isdir('./audios'):
            with open("./audios/date.txt", "r", encoding="utf-8") as arquivo:
                date_str = arquivo.readline()
            date = datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S')

            diferenca = (datetime.now() - date) / timedelta(minutes=1)
            
            if diferenca > 20:
                shutil.rmtree('./audios') 
