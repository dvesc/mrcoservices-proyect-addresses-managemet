import services.state_services as state_services
import services.country_services as country_services
from models.address_model import addresses as model
import json 
from datetime import datetime
from bson import ObjectId
import re  # manejar expresiones regulares
from db.mongo_json import MongoJsonEncoder

#------------------------------------------------------------------------------
def create_address(user_id:str,city_vo:dict) -> dict:
  state_vo = state_services.get_by_id(
    city_vo['state']['$oid']
  )
  country_vo = country_services.get_by_id(
    state_vo['country']['$oid']
  )

  cursor = model(
    user_id = user_id,
    country = {
      '_id': ObjectId(country_vo['_id']['$oid']),
      'name': country_vo['slug'],
    },
    state = {
      '_id':ObjectId(state_vo['_id']['$oid']),
      'name': state_vo['name'],
    },
    city = {
      '_id':ObjectId(city_vo['_id']['$oid']),
      'name': city_vo['name'],
    },
  )
  
  #De cursor a dict a json a dict
  address_vo: dict = json.loads(
    MongoJsonEncoder().encode(
      cursor.save().to_json()
    )
  ) 
  #Retornamos un dict
  return address_vo



#GETS INDIVIDUALES----------------------------------------------------------------------------------
def get_by_id(address_id:str)->dict:
  if re.match(r"^[0-9a-fA-F]{24}$", address_id):
    id_obj = ObjectId(address_id)
  else: id_obj = ''


  cursor = model.objects(
    __raw__ = {
      '_id': id_obj,
      'deleted_at': None
    }
  ).first()
  #Si cursor esta vacio retornamos None y evitamos errores
  if not cursor: return None
  #De cursor a dict a json(con valores transformados) a dict
  address_vo: dict = json.loads(
    MongoJsonEncoder().encode(
      cursor.to_json()
    )
  )
  return address_vo

def get_by_userid_and_cityid(user_id:str,city_id:str)->dict:
  if re.match(r"^[0-9a-fA-F]{24}$", city_id):
    id_obj = ObjectId(city_id)
  else: id_obj = ''
  cursor = model.objects(
    __raw__ = {
      '$and':[
        {'user_id': user_id},
        {'city._id': id_obj},
        {'deleted_at': None}
      ]
    }
  ).first()
  print(cursor)
  #Si cursor esta vacio retornamos None y evitamos errores
  if not cursor: return None
  #De cursor a dict a json(con valores transformados) a dict
  address_vo: dict = json.loads(
    MongoJsonEncoder().encode(
      cursor.to_json()
    )
  )

  print(address_vo)
  return address_vo

#GET COINCIDENCIAS----------------------------------------------------------------------------------
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
    { 'user_id': id_obj },
    { 'country._id': id_obj },
    { 'country.name': regexp },
    { 'state._id': id_obj },
    { 'state.name': regexp },
    { 'city._id': id_obj},
    { 'city.name': regexp },
  ]
  cursor = model.objects(
    __raw__= {
      '$and': [{ 'deleted_at': None }, { '$or': terms }]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_user_id(filter_value:str,sort:dict)->list:
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'user_id': filter_value }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences


#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_country_id(filter_value:str,sort:dict)->list:
  #si el filter value es un id
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
    id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'country._id': id_obj }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_state_id(filter_value:str,sort:dict)->list:
  #si el filter value es un id
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
    id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'state._id': id_obj }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_city_id(filter_value:str,sort:dict)->list:
  #si el filter value es un id
  if re.match(r"^[0-9a-fA-F]{24}$", filter_value):
    id_obj = ObjectId(filter_value)
  else: id_obj = ''
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'city._id': id_obj }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_country_name(filter_value:str,sort:dict)->list:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'country.name': regexp }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_state_name(filter_value:str,sort:dict)->list:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'state.name': regexp} 
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences

#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
def coincidences_by_city_name(filter_value:str,sort:dict)->list:
  regexp = re.compile(
    r'{}'.format(filter_value),
    re.I #bandeas
  )
  #hacemos el filter
  cursor = model.objects(
    __raw__= {
      '$and': [
        { 'deleted_at': None }, 
        { 'city.name': regexp }
      ]
    }
  ).order_by(sort['order']+sort['order_by']) #'<+ o -><field por el que ordenara>'
  coincidences:list = []
  for coincidence in cursor:
    coincidences.append(
      json.loads(
        MongoJsonEncoder().encode(
          coincidence.to_json()
        )
      )
    )
    
  return coincidences




#ACTUALIZAR----------------------------------------------------------------------------------------
def update(address_id:str, city_vo: dict) -> dict:
  state_vo = state_services.get_by_id(
    city_vo['state']['$oid']
  )
  country_vo = country_services.get_by_id(
    state_vo['country']['$oid']
  )

  cursor = model.objects(
    __raw__ = {
      '_id': ObjectId(address_id),
      'deleted_at': None
    }
  ).first()

  #actualizamos 
  #OJO-> UPDATE no nos devuelve el vo actualizado solo el numero de documentos actualizados
  print(cursor.update(
    country = {
      '_id': ObjectId(country_vo['_id']['$oid']),
      'name': country_vo['slug'],
    },
    state = {
      '_id':ObjectId(state_vo['_id']['$oid']),
      'name': state_vo['name'],
    },
    city = {
      '_id':ObjectId(city_vo['_id']['$oid']),
      'name': city_vo['name'],
    },
    updated_at= datetime.now()
  ))

  #retornamos el actualizado
  return get_by_id(address_id)



#ELIMINAR---------------------------------------------------------------------------------------
def delete(address_id:str) -> dict:
  cursor = model.objects(
    __raw__ = {
      '_id': ObjectId(address_id),
      'deleted_at': None
    }
  ).first()
  #"eliminamos" ya que solo actualizamos el deleted_at
  cursor.update(
    deleted_at= datetime.now()
  )
  #De cursor a dict a json a dict
  address_vo: dict = json.loads(
    MongoJsonEncoder().encode(
     cursor.to_json()
    )
  ) 
  return address_vo

