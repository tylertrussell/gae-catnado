# 










## Classes
    
    
###`CompressedProperty`

An unindexed, compressed property.

  CompressedTextProperty and CompressedBlobProperty derive from this class.
  

        
#### Class Functions
            
            
`make_value_from_datastore`


 
            
`value_to_str`

Returns the value stored by this property encoded as a (byte) string,
    or None if value is None.  This string will be stored in the datastore.
    By default, returns the value unchanged.
 
            
`get_value_for_datastore`


 
            

        

    
    
###`CompressedTextProperty`

A string that will be stored in a compressed form (encoded as UTF-8).

  Example usage:
  >>> class CompressedTextModel(db.Model):
  ...  v = CompressedTextProperty()

  You can create a CompressedTextProperty and set its value with your string.
  You can also retrieve the (decompressed) value by accessing the field.
  >>> ustr = ...
  >>> model = CompressedTextModel(v=ustr)
  >>> model.put()
  datastore_types.Key.from_path(u'CompressedTextModel', ...)

  >>> model2 = CompressedTextModel.all().get()
  >>> model2.v == ustr
  True

  Compressed text is not indexed and therefore cannot be filtered on:

  >>> CompressedTextModel.gql("WHERE v = :1", ustr).count()
  0
  

        
#### Class Functions
            
            
`value_to_str`


 
            

        

    
    
###`CompressedBlobProperty`

A byte string that will be stored in a compressed form.

  Example usage:

  >>> class CompressedBlobModel(db.Model):
  ...   v = CompressedBlobProperty()

  You can create a CompressedBlobProperty and set its value with your raw byte
  string (anything of type str).  You can also retrieve the (decompressed) value
  by accessing the field.

  >>> model = CompressedBlobModel(v=...)
  >>> model.v = 'green'
  >>> model.v
  'green'
  >>> model.put() # doctest: +ELLIPSIS
  datastore_types.Key.from_path(u'CompressedBlobModel', ...)

  >>> model2 = CompressedBlobModel.all().get()
  >>> model2.v
  'green'

  Compressed blobs are not indexed and therefore cannot be filtered on:

  >>> CompressedBlobModel.gql("WHERE v = :1", 'green').count()
  0
  

        
#### Class Functions
            
            

        

    