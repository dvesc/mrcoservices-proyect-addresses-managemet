from auth0.v3.authentication.token_verifier import  AsymmetricSignatureVerifier
from error.exceptions import BelongingAddressException, NonexistentElementException
import services.address_services as address_services
from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv
load_dotenv() #Carga las variables de entorno

domain = os.getenv('AUTH0_DOMAIN')



async def belonging_middleware(req:Request) -> str: 
  user_id:str = ''

  #obtenemos el auth0 id (que esta en el middleware)
  jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
  sv = AsymmetricSignatureVerifier(jwks_url) 
  token = req.headers["authorization"].replace("Bearer ","") 
  payload = sv.verify_signature(token)
  auth0_id= payload['sub'].replace('auth0|','')


  if req.method == 'POST':
    #validamos que el user id en el body le pertenece al usuario que emite el token
    user_id = (await req.json())['user_id']  #obtenemos el id del body
    if user_id != auth0_id:
      raise BelongingAddressException(
        'you are trying to create an address for another user'
      )
    return req

  #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  if req.method == 'PUT' or req.method == 'DELETE' :
    address_id: str = req.path_params['address_id']
    address_vo: dict = address_services.get_by_id(address_id)

    #validamos que la direccion exista
    if not address_vo:
      raise NonexistentElementException('address does not exist')
    #Validamos que el user_id de la direccion le pertenece al usuario que emite el token
    if address_vo['user_id'] != auth0_id:
       raise BelongingAddressException(
        'you are trying to update an address for another user'
      )
      
    return address_vo

