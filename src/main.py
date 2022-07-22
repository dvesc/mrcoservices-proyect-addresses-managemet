from urllib.request import Request
from fastapi import  FastAPI
from error.exceptions import AuthorizationHeaderException, DuplicationException, InvalidTokenException, NonexistentElementException, BelongingAddressException
from routes.address_routes import address_routes
from routes.city_routes import city_routes
from routes.country_routes import country_routes
from routes.state_routes import state_routes
from fastapi.responses import JSONResponse
from db.mongo_connection import connect_to_db


app = FastAPI()
app.include_router(address_routes)
app.include_router(city_routes)
app.include_router(country_routes)
app.include_router(state_routes)

connect_to_db()
print('app is running')


#ERROR HANDLERS----------------------------------------------------------------
@app.exception_handler(DuplicationException)
async def duplication_exception_handler(
  req:Request,
  exc:DuplicationException
):
  return JSONResponse(
    status_code=409, content={
      'status':409,
      'error':'DuplicationException',
      'message':'The user already has this address'
    }
  )

@app.exception_handler(NonexistentElementException)
async def nonexistent_element_exception(
  req:Request, 
  exc: NonexistentElementException
):
  return JSONResponse(
    status_code=404, content={
      'status':404,
      'error':' NonexistentElementException',
      'message':exc.msg
    }
  )

@app.exception_handler(BelongingAddressException)
async def nonexistent_city_exception(
  req:Request, 
  exc: BelongingAddressException
):
  return JSONResponse(
    status_code=401, content={
      'status':401,
      'error':'BelongingAddressException',
      'message':exc.msg
    }
  )

@app.exception_handler(AuthorizationHeaderException)
async def authorization_header_exception(
  req:Request, 
  exc: AuthorizationHeaderException
):
  return JSONResponse(
    status_code=400, content={
      'status':400,
      'error':'AuthorizationHeaderException',
      'message': 'header authorization required'
    }
  )

@app.exception_handler(InvalidTokenException)
async def authorization_header_exception(
  req:Request, 
  exc: InvalidTokenException
):
  return JSONResponse(
    status_code=401, content={
      'status':401,
      'error':'InvalidTokenException',
      'message': 'Invalid Token'
    }
  )


