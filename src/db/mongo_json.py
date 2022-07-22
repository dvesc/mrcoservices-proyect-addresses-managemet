import json
from bson import ObjectId
from datetime import datetime, date
import isodate as iso


#En mongoengine retornaremos la data solo con los valores en sus equivalentes de str
#esto quiere decir que valores como el ObjectId se muestran por su equivalente 
# asi-> {'$oid': '<el id>'}; igual con las Date -> {'$date': <timestamp>}
#Entonces transformaremos los "json primitivos" de mongoengine en json de "verdad"
#transformando esa data a los valores reales solo que como str Ej:
#{'$oid': '<el id>'} -> '<el id>'
#{'$date': <timestamp>} -> '2022-05-05T00:09:17'

class MongoJsonEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, (datetime, date)):
      return iso.datetime_isoformat(o)
      iso.datetime_isoformat(o)
    if isinstance(o, ObjectId):
      return str(o)
    return json.JSONEncoder.default(self, o)



