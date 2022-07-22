from typing import Optional
from fastapi import APIRouter, Depends
import re  # manejar expresiones regulares
from starlette.requests import Request
from DTOs.address_dtos import new_address_dto, updated_address_dto
from error.exceptions import DuplicationException, NonexistentElementException
from middlewares.belonging_middelaware import belonging_middleware
from middlewares.token_middleware import token_midleware
from utils.pagination import paginated_data 
#Importamos los servicios de las diversas colectiones
import services.address_services as address_services
import services.city_services as city_services

#Creamos el "ojeto" de las rutas
address_routes = APIRouter()
uri_base = '/user/addresses'


#CREAR DIRECCIONES-------------------------------------------------------------
@address_routes.post(uri_base)
def create_address(
body: new_address_dto, 
req = Depends(token_midleware)
):
  address_dto = dict(body)
  address_vo: dict = {}

  #Comprobamos que el la city exista
  city_vo: dict = city_services.get_by_id(address_dto['city_id'])
  if not city_vo: raise NonexistentElementException('the city does not exist')
  #Comporbarmos que el usuario no tenga esta direccion registrada ya
  address_vo = address_services.get_by_userid_and_cityid(
    address_dto['user_id'],
    city_vo['_id']['$oid']
  )
  if address_vo: raise DuplicationException('')

  #Creamos la direccion del usuario
  address_vo: dict =address_services.create_address(
    address_dto['user_id'],
    city_vo
  )

  return {
    'status': 'Address created successfully',
    'data': address_vo
  }





#ACTUALIZAR DIRECCIONES-------------------------------------------------------------
@address_routes.put(uri_base+'/{address_id}')
def update_address(
address_id,
body:updated_address_dto, 
req = Depends(token_midleware),
address_vo: dict = Depends (belonging_middleware)
):
  new_address_dto = dict(body)
  city_vo: dict
  
  #si pasaron el city id por el body lo usamos, si no usamos el que ya trae el address
  city_id:str = address_vo['city']['_id']

  if(new_address_dto['city_id']):
    city_id = new_address_dto['city_id']

  #Comprobamos que el la city exista 
  city_vo = city_services.get_by_id(city_id)
  if not city_vo: raise NonexistentElementException(
    'the city does not exist'
  )
  #actualizamos
  new_address_vo = address_services.update(address_id,city_vo)

  return {
    'status': 'Address updated successfully',
    'data': new_address_vo
  }




#ELIMINAR DIRECCIONES------------------------------------------------
@address_routes.delete(uri_base+'/{address_id}')
def delete_address(
address_id,
req = Depends(token_midleware),
address_vo: str = Depends (belonging_middleware)
):
  #eliminamos
  deleted_address_vo = address_services.delete(address_id)

  return {
    'status': 'Address deleted successfully',
  }


#OBTENER DIRECCIONES-------------------------------------------------
@address_routes.get(uri_base)
def get_addresses(
  request: Request,
  filterby: Optional[str] = None,
  filtervalue: Optional[str] = None,
  orderby: Optional[str] = None,
  order: Optional[str] = None,
  page: Optional[str] = None,
  size: Optional[str] = None,
):  
  query_params = request.query_params
  
  #Asignamos valores por defecto 
  filter_by:str = filterby if filterby != None else 'all'
  filter_value:str = filtervalue if filtervalue != None else ''
  pag:int
  siz:int
  order_by: str


  if page != None:
    pag = int(page) if page.isdigit() else 1
  else: pag = 1
  if size != None:
    siz = int(size) if size.isdigit() else 10
  else: siz = 10  
  if orderby != None:
    order_by = orderby if  re.match(
      r"created_at|country_id|country_name|state_id|state_name|city_id|city_name", filter_value
    ) else 'created_at'
  else: order_by = 'created_at'


  sort:dict = {
    'order': '-' if order == None or order == 'desc' else '+',
    'order_by': order_by
  }

  coincidences: list = []
  #switch
  if filter_by == 'user_id':
     coincidences = address_services.coincidences_by_user_id(
      filter_value,sort
    )
  elif filter_by == 'country_id':
    coincidences = address_services.coincidences_by_country_id(
      filter_value,sort
    )
  elif filter_by == 'country_name':
    coincidences = address_services.coincidences_by_country_name(
      filter_value,sort
    )
  elif filter_by == 'state_id':
    coincidences = address_services.coincidences_by_state_id(
      filter_value,sort
    )
  elif filter_by == 'state_name':
    coincidences = address_services.coincidences_by_state_name(
      filter_value,sort
    )
  elif filter_by == 'city_id':
    coincidences = address_services.coincidences_by_city_id(
      filter_value,sort
    )
  elif filter_by == 'city_name':
    print('aqui')
    coincidences = address_services.coincidences_by_city_name(
      filter_value,sort
    )
  else:
    coincidences = address_services.coincidences_by_all(
      filter_value,sort
    )

  
  msg = paginated_data(siz,pag,coincidences, request)
  return msg