import math
from starlette.requests import Request
import re  # manejar expresiones regulares





def create_links (
  total_pages:int,
  complete_url:str,
  param:str
) -> dict:

  page_number:int = int(param.split('=')[1] or '1')
  nex:str=''  #next es un nombre reservado
  last:str=''
  prev:str=''
  first:str=''

  if(page_number > 0 and page_number < total_pages):
    nex= re.sub(  
      r'page=\d{1,}', 
      'page={}'.format(page_number+1),
      complete_url 
    )
    last= re.sub(  
      r'page=\d{1,}', 
      'page={}'.format(total_pages),
      complete_url 
    )
  if(page_number > 1):
    prev= re.sub(  
      r'page=\d{1,}', 
      'page={}'.format(page_number-1),
      complete_url 
    )
    first= re.sub(  
      r'page=\d{1,}', 
      'page=1',
      complete_url 
    )
  
  return {
    'next':nex,
    'last':last,
    'prev':prev,
    'self':complete_url,
    'first':first
  } 



#------------------------------------------------------------------------------
def paginated_data (
  siz:int,
  pag:int,
  data: list,
  req: Request
):
  page:int = pag or 1
  size:int = siz or 10
  start:int = (page-1)*size
  estimated_pages:int= len(data) / size
  total_pages:int

  #hacemos los redondeos necsarios para el calculo de paginas totales
  if estimated_pages > 0 and estimated_pages < 1:
    total_pages = math.ceil(estimated_pages)
  else: 
    total_pages = math.floor(estimated_pages)

  complete_url:str = ''
  querys:str = str(req.query_params)
  params:list = querys.split('&')
  links: dict = {}
  flag: int = 0

  #le pone a los query_params 'page' si no lo tenia
  for element in params:
    if re.match(r'page=\d{1,}',element):
      flag = 1 #encontro que si tiene page

  if flag == 0: #si no encontro nada 
    #si tiene otros querys ponemos page al final
    if len(params) >= 1 and params[0] != '':  
      querys = '?'+querys+'&page=1'
    #si no al inicio
    else: 
      querys = '?'+querys+'page=1'
    params = querys.split('&')
  
  #creamos los links  
  for param in params:
    if param.find(r'page') != -1:
      complete_url = req.url.path+querys
      links = create_links(total_pages, complete_url,param)

  #tenemos echa la paginacion    
  return {
    'data': data[start:start+size],
    'meta': {
      'current_page': page,
      'page_size': size,
      'total_elements': len(data),
      'total_pages': total_pages,
      'links': links,
    }
  }
