from auth0.v3.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier
from fastapi import Request, HTTPException

import os
from dotenv import load_dotenv
from requests import request

from error.exceptions import AuthorizationHeaderException, InvalidTokenException
load_dotenv() #Carga las variables de entorno

domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')

async def token_midleware(req: Request):
  #si nos pasan el token
  if 'authorization' in req.headers:
    jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
    issuer = 'https://{}/'.format(domain)

    #Le pegamos al endpoint que nos da la key secret
    sv = AsymmetricSignatureVerifier(jwks_url) 
    tv = TokenVerifier(
      signature_verifier=sv, 
      issuer=issuer, 
      audience=client_id
    )
    token = req.headers["authorization"].replace("Bearer ","") 

    try:
      tv.verify(token) #verificamos el token    
    except:
      raise InvalidTokenException('')

    return req
  else:
    raise AuthorizationHeaderException('')

