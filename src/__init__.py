import logging.config

LOGGING_CONFIG = LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s][%(asctime)s][%(module)s][%(message)s]',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'M0': {
            'handlers': ['default'],
            'propagate': True,
            'level': 'DEBUG',
        },
        '__main__': {
            'handlers': ['default'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
