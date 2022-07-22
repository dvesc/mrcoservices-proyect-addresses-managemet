from fastapi import Request, app
from addresses.src.error.exceptions import DuplicationException
from fastapi.responses import JSONResponse

@app.exception_handler(DuplicationException)
async def duplication_exception_handler(
  req:Request,
  exc:DuplicationException
):
  return JSONResponse(
    status_code=500, content={
      'status':'',
      'error':'DuplicationException',
      'message':'The user already has this address'
    }
  )
