from google.appengine.api import app_identity, urlfetch


APP_ENGINE_URL_FORMAT = 'https://{service}.{app_id}.appspot.com/{base_path}/{version}/{path}'

DEFAULT_BASE_PATH = 'api'

INBOUND_APP_ID = 'X-Appengine-Inbound-Appid'


def async_api_call(service, version, path, payload, base_path=None,
                  method=urlfetch.GET, deadline=None,):
  """ Make an asynchronous API call to another service in this GAE application.

  This function utilizes urlfetch with follow_redirects=False so AppEngine will
  add the X-Appengine-Inbound-Appid HTTP header which the target service will
  used to authenticate the request.

  Arguments:
    service: str; service name
    version: str; API version
    path: str; the API path to request
    payload: payload for urlfetch
    base_path: optional str; base API path (defaults to "api")
    method: optional int, method flag from urlfetch (defaults to urlfetch.GET)
    deadline: optional deadline in seconds

  Returns:
    urlfetch RPC object
  """
  url = APP_ENGINE_URL_FORMAT.format(
    service=service,
    app_id=app_identity.get_application_id(),
    base_path=base_path or DEFAULT_BASE_PATH,
    version=version,
    path=path,
  )
  rpc = urlfetch.create_rpc(deadline=deadline)
  return urlfetch.make_fetch_call(rpc, url, payload, method=method,
                           follow_redirects=False)


def blocking_api_call(service, version, path, payload, base_path=None,
                      method=urlfetch.GET, deadline=None,):
  """ Make a synchronous API call to another service in this GAE application.

  See async_api_call for full documentation.
  """
  rpc = async_api_call(service, version, path, payload, base_path, method,
                       deadline)
  return rpc.get_result()


class InsecureAPIRequestError(Exception):
  pass


def validate_api_request(request):
  """
  Arguments:
    request: webapp2 Request

  Raises:
    InsecureAPIRequestError: if the application ID header is missing from the
      request or the ID does not match the current application
  """
  purported_app_id = request.headers.get(INBOUND_APP_ID)
  actual_app_id = app_identity.get_application_id()

  if not purported_app_id or purported_app_id != actual_app_id:
    raise InsecureAPIRequestError(
      'Expected application ID {} but got {}'.format(
        purported_app_id,
        actual_app_id
      )
    )