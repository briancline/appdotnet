from exceptions import MethodNotFoundException

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

BASE_URL = 'https://alpha-api.app.net'
ACCOUNT_BASE_URL = 'https://account.app.net'


def find_method(key, vars=None):
    if key not in method_map:
        raise MethodNotFoundException

    (verb, uri) = method_map[key]

    if vars is not None:
        print vars
        uri = uri.format(**vars)
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
