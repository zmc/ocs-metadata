import os
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo')
MONGO_PORT = 27017
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'build-metadata')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE', 'admin')
DEBUG = os.environ.get('DEBUG', False)

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
HATEOAS = False
EXTRA_RESPONSE_FIELDS = []
RENDERERS = ['eve.render.JSONRenderer']

products = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'name',
    },
    'schema': {
        'name': {
            'type': 'string',
            'unique': True,
        },
    },
}
builds = {
    'additional_lookup': {
        'url': 'regex(".+")',
        'field': 'version',
    },
    'schema': {
        'product': {
            'type': 'string',
            'required': True,
            'data_relation': {
                'resource': 'products',
                'field': 'name',
                'embeddable': True,
            },
        },
        'version': {
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
                    'version': {'type': 'string'},
                },
            },
        },
    },
}
DOMAIN = {
    'products': products,
    'builds': builds,
}
