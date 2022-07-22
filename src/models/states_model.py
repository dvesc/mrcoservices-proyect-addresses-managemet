import mongoengine as db
import json 
class states_model (db.DynamicDocument):

  #con esto vinculamos este modelo a la collecion ya existente en la db
  meta = {
    'collection': 'states'
  }
