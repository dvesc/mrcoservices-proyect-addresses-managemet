from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class DuplicationException(Exception):
  def __init__(self,message:str) -> None:
      self.msg = message


class NonexistentElementException(Exception):
  def __init__(self,message:str) -> None:
      self.msg =message

class BelongingAddressException(Exception):
  def __init__(self,message:str) -> None:
      self.msg = message

class AuthorizationHeaderException(Exception):
  def __init__(self,message:str) -> None:
      self.msg = message

class InvalidTokenException(Exception):
  def __init__(self,message:str) -> None:
      self.msg = message


