from typing import Optional
from pydantic import BaseModel, validator
import re  # manejar expresiones regulares

class new_address_dto (BaseModel):
  user_id: str
  city_id: str

  #El user_id lo "valido" comparandolo con el id de auth0 del token

  @validator('city_id')
  def valid_city(cls,value):
    if not re.findall(r"^[0-9a-fA-F]{24}$", value):
      raise ValueError('the path "city" must be a valid mongo id')
    return value


#CUANDO SE ACTUALIZE-----------------------------------------------------------
class updated_address_dto (BaseModel):
  city_id: Optional[str] = None


  #El user_id lo "valido" comparandolo con el id de auth0 del token

  @validator('city_id')
  def updating_valid_city(cls,value):
    if value:
      if not re.findall(r"^[0-9a-fA-F]{24}$", value):
        raise ValueError('the path "city" must be a valid object id')
      return value


