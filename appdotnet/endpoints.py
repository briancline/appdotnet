from exceptions import MethodNotFoundException

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

BASE_URL = 'https://alpha-api.app.net'
ACCOUNT_BASE_URL = 'https://account.app.net'


def find_method(key, uri_vars=None):
    """ Given a method key, returns a tuple containing the HTTP verb and the
    full API endpoint for that particular method. If any vars are passed in,
    they are substituted out in the URL with the values provided.

    :param key: the API method key
    :param dict uri_vars: (optional) a dict containing any variables to
        substitute out in the endpoint URI
    :returns: (tuple) HTTP verb and full API endpoint URL

    """
    if key not in method_map:
        raise MethodNotFoundException

    (verb, uri) = method_map[key]

    if uri_vars is not None:
        print uri_vars
        uri = uri.format(**uri_vars)
    if uri[0] == '/':
        uri = BASE_URL + uri

    return (verb, uri)


method_map = {
    'oauth.token.create': (POST,   ACCOUNT_BASE_URL + '/oauth/access_token'),

    'streams.get':        (GET,    '/stream/0/streams/{stream_id}'),
    'streams.list':       (GET,    '/stream/0/streams'),
    'streams.create':     (POST,   '/stream/0/streams'),
    'streams.update':     (PUT,    '/stream/0/streams'),
    'streams.delete':     (DELETE, '/stream/0/streams/{stream_id}'),
    'streams.delete_all': (DELETE, '/stream/0/streams')
}
