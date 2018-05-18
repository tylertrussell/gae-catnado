import array

from google.appengine.ext import db


class ArrayProperty(db.UnindexedProperty):
  """An array property that is stored as a string.

  Example usage:

  >>> class ArrayModel(db.Model):
  ...  v = ArrayProperty('i')
  >>> m = ArrayModel()

  If you do not supply a default the array will be empty.

  >>> m.v
  array('i')

  >>> m.v.extend(range(5))
  >>> m.v
  array('i', [0, 1, 2, 3, 4])
  >>> m.put() # doctest: +ELLIPSIS
  datastore_types.Key.from_path(u'ArrayModel', ...)
  >>> m2 = ArrayModel.all().get()
  >>> m2.v
  array('i', [0, 1, 2, 3, 4])
  """
  data_type = array.array

  def __init__(self, typecode, *args, **kwargs):
    self._typecode = typecode
    kwargs.setdefault('default', array.array(typecode))
    super(ArrayProperty, self).__init__(typecode, *args, **kwargs)

  def get_value_for_datastore(self, model_instance):
    value = super(ArrayProperty, self).get_value_for_datastore(model_instance)
    return db.Blob(value.tostring())

  def make_value_from_datastore(self, value):
    if value is not None:
      return array.array(self._typecode, value)

  def empty(self, value):
    return value is None

  def validate(self, value):
    if not isinstance(value, array.array) or value.typecode != self._typecode:
      raise db.BadValueError(
        "Property %s must be an array instance with typecode '%s'" % (
          self.name, self._typecode))
    return super(ArrayProperty, self).validate(value)

  def default_value(self):
    return array.array(self._typecode,
                       super(ArrayProperty, self).default_value())