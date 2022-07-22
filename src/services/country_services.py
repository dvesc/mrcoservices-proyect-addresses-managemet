import json 
from bson import ObjectId
from models.countries_model import countries_model as model
from db.mongo_json import MongoJsonEncoder
import re  # manejar expresiones regulares
#------------------------------------------------------------------------------
def get_country_by_name(name:str) -> dict:
  cursor: model = model.objects(
    __raw__={'slug': name}
  ).first()

  #Si coincicende esta vacio retornamos None y evitamos errores
  if not cursor: return None

  #El MongoJsonEncoder no me funciona con collecion sin modelos propios 
  country_vo:dict = json.loads(cursor.to_json())

  return country_vo

#------------------------------------------------------------------------------
def get_by_id(id:str) -> dict:
  cursor: model = model.objects(
    __raw__={'_id': ObjectId(id)}
  ).first()

  #Si coincicende esta vacio retornamos None y evitamos errores
  if not cursor: return None

  #El MongoJsonEncoder no me funciona con collecion sin modelos propios 
  country_vo:dict = json.loads(cursor.to_json())

  return country_vo

#COINCIDENCES------------------------------------------------------------------
def coincidences_by_all(filter_value:str,sort:dict)->dict:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #si el filter value es un id creamos un objectid
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
   id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #Hacemos el filtro
  terms = [
    {'_id': regexp},
    {'slug': regexp},
  ]
  cursor = model.objects(
    __raw__= {
      '$and': [{ 'deleted_at': None }, { '$or': terms }]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences = []

  for coincidence in cursor:
    coincidences.append(
      json.loads(coincidence.to_json())
    )
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_id(filter_value:str,sort:dict)->dict:
  #si el filter value es un id creamos un objectid
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
   id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #Hacemos el filtro
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { '_id': id_obj }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(coincidence.to_json())
    )
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
def coincidences_by_slug(filter_value:str,sort:dict)->list:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'slug': regexp }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(coincidence.to_json())
    )
    
  return coincidences
