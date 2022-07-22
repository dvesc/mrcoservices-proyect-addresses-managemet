from datetime import datetime
import mongoengine as db

class embedded_data(db.EmbeddedDocument):
  _id= db.ObjectIdField(required=True)
  name= db.StringField(require=True)

class addresses (db.Document):
  user_id= db.StringField(require=True) #es string (id de auth0)
  country= db.EmbeddedDocumentField(embedded_data) 
  state= db.EmbeddedDocumentField(embedded_data)
  city= db.EmbeddedDocumentField(embedded_data)
  created_at= db.DateTimeField(required= True,default=datetime.now())
  updated_at= db.DateTimeField(required= True, default=datetime.now())
  deleted_at= db.DateTimeField(null=True, default=None,) 
  #null=true es para que aunque no tenga valor la ponga en la db como null, porque si no no la pone


  #Para convertir el cursor a una especie de json
  #pero luego hay que transformarlo a json con el JSONEncoder y luego  a dict otra vez
  def to_json(self):
    return {
      '_id': self.id, #pones 'id' ya que asi lo devuelve mongoengine
      'user_id': self.user_id,
      'country': {
        '_id':self.country._id,
        'name': self.country.name
      },
      'state': {
        '_id':self.state._id,
        'name':self.state.name
      },
      'city': {
        '_id': self.city._id,
        'name': self.city.name
      },
      'created_at': self.created_at,
      'updated_at': self.updated_at,
      'deleted_at': self.deleted_at
    }


