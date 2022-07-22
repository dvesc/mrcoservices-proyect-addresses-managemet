from models.states_model import states_model as model
from bson import ObjectId
import json 
from db.mongo_json import MongoJsonEncoder
import re  # manejar expresiones regulares

#------------------------------------------------------------------------------
def get_by_name_and_country_id(name:str,country_id:str) -> dict:
  cursor: model = model.objects(
    __raw__= {
      'name': name,
      'country': ObjectId(country_id)
    }
  ).first()

  #Si cursor esta vacio retornamos None y evitamos errores
  if not cursor: return None

  #El MongoJsonEncoder no me funciona con colecciones sin modelos propios
  state_vo = json.loads(cursor.to_json())
  return state_vo

#------------------------------------------------------------------------------
def get_by_id(id:str) -> dict:
  cursor: model = model.objects(
    __raw__= {
      '_id': ObjectId(id)
    }
  ).first()

  #Si cursor esta vacio retornamos None y evitamos errores
  if not cursor: return None


  #El MongoJsonEncoder no me funciona con colecciones sin modelos propios
  #state_vo = json.loads(cursor.to_json())
  state_vo =  json.loads(cursor.to_json())

  return state_vo


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
    {'name': regexp},
    {'state': id_obj},
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
def coincidences_by_countryid(filter_value:str,sort:dict)->dict:
  #si el filter value es un id creamos un objectid
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
   id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #Hacemos el filtro
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'country': id_obj }
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
def coincidences_by_name(filter_value:str,sort:dict)->list:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'name': regexp }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(coincidence.to_json())
    )
    
  return coincidences