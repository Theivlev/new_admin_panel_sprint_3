LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'your_module_name': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}