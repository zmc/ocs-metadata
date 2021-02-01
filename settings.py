import os
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo')
MONGO_PORT = 27017
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'build-metadata')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE', 'admin')
DEBUG = os.environ.get('DEBUG', False)
X_DOMAINS = os.environ.get('X_DOMAINS', None)

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
HATEOAS = False
EXTRA_RESPONSE_FIELDS = []
RENDERERS = ['eve.render.JSONRenderer']

builds = {
    'additional_lookup': {
        'url': 'regex(".+")',
        'field': 'version',
    },
    'schema': {
        'product': {
            'type': 'string',
            'required': True,
        },
        'version': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'url': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'contents': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'name': {'type': 'string'},
                    'tag': {'type': 'string'},
                    'image': {'type': 'string'},
                    'bundle': {'type': 'string'},
                    'nvr': {'type': 'string'},
                },
            },
        },
    },
}
DOMAIN = {
    'builds': builds,
}
