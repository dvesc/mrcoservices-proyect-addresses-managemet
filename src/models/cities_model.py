import mongoengine as db

class cities_model (db.DynamicDocument):

  #con esto vinculamos este modelo a la collecion ya existente en la db
  meta = {
    'collection': 'cities'
  }
