from google.appengine.ext import db

from catnado.properties.key_property import KeyProperty


class UniquePropertyRecordExistsError(Exception):
  """Raise when attempting to create a property that already exists."""

  pass


class UniquePropertyRecord(db.Model):
  """Datastore model for keeping particular properties unique.

  Creates a key name using a combination of the Kind, Property Name, and Value.

  Since get_by_key_name is strongly consistent within a datastore transactional,
  one can be certain that no other entity exists with that specific combination
  as long as a UniquePropertyRecord is created during the same transaction.
  """

  target_key = KeyProperty()

  @staticmethod
  def make_key_name(kind, property_name, value):
    """Make a Key Name given a kind, property name, and value.

    Args:
      kind: required str or db.Model subclass
      property_name: required str; property name i.e. "email"
      value: required value (that can be converted to a string)

    Returns:
      str to be used as a Key Name

    Raises:
      ValueError if kind is not a string or db.Model subclass
    """
    if isinstance(kind, type) and issubclass(kind, db.Model):
      kind = kind.kind()
    if not isinstance(kind, basestring):
      raise ValueError('kind must be a string or db.Model subclass')

    return '{}:{}:{}'.format(kind, property_name, value)

  @staticmethod
  def create(kind, property_name, value, target_key=None):
    """Create a UniquePropertyRecord.

    If called from within a transactional, there is no attempt to verify that
    the given combo of key/property_name/value doesn't already exist. It is
    assumed that one calling this function from within a transactional is already
    verifying that the combo is unique.

    Args:
      (see make_key_name)
      target_key: optional db.Model subclass or key pointing at any entity
      transactional: optional bool, whether to create in a transaction (True)

    Returns:
      newly-created UniquePropertyRecord key or None

    Raises:
      AssertionError: if value is None and allow_none is False
      ValueError: if kind is not a string or db.Model subclass
    """
    assert value is not None

    called_from_transaction = db.is_in_transaction()

    def _create():
      if not called_from_transaction:
        existing_record = UniquePropertyRecord.retrieve(kind, property_name, value)
        if existing_record:
          raise UniquePropertyRecordExistsError(existing_record.key().name())
      key_name = UniquePropertyRecord.make_key_name(kind, property_name, value)
      return UniquePropertyRecord(key_name=key_name, target_key=target_key).put()

    if not called_from_transaction:
      return db.run_in_transaction(_create)
    else:
      return _create()

  @staticmethod
  def retrieve(kind, property_name, value):
    """Find a UniquePropertyRecord, if it exists.

    Args:
      see create

    Returns:
      bool; True iff a UniquePropertyRecord exists with the given kind, property
        name, and value
    """
    key_name = UniquePropertyRecord.make_key_name(kind, property_name, value)
    return UniquePropertyRecord.get_by_key_name(key_name)
