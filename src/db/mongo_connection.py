from mongoengine import connect
#Para variables de entorno
import os
from dotenv import load_dotenv
load_dotenv() #Carga las variables de entorno

def connect_to_db():
  print('conecting to database...') 
  connect(host=
    'mongodb+srv://' + os.getenv('DB_USERNAME')+
    ':' + os.getenv('DB_PASSWORD')+
    '@' + os.getenv('DB_HOST')+
    '/' + os.getenv('DB_NAME')
  )
  print('Conected to mongo')