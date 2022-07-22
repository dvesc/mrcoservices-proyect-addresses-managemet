from fastapi import APIRouter
from typing import Optional
from starlette.requests import Request
import re  # manejar expresiones regulares
import services.city_services as city_services
from utils.pagination import paginated_data

city_routes = APIRouter()
uri_base = '/geografy/cities'

@city_routes.get(uri_base)
def get_cities(
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
      r'state_id|id|name', filter_value
    ) else 'created_at'
  else: order_by = 'created_at'


  sort:dict = {
    'order': '-' if order == None or order == 'desc' else '+',
    'order_by': order_by
  }

  coincidences:list = [list]

  #switch
  if filter_by == 'id':
     coincidences = city_services.coincidences_by_id(
      filter_value,sort
    )
  elif filter_by == 'name':
    coincidences = city_services.coincidences_by_name(
      filter_value,sort
    )
  elif filter_by == 'state_id':
    coincidences = city_services.coincidences_by_stateid(
      filter_value,sort
    )
  else:
    coincidences = city_services.coincidences_by_all(
      filter_value,sort
    )

  msg = paginated_data(siz,pag,coincidences, request)
  return msg