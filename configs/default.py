from kombu import Exchange, Queue

SWAGGER = {
    'doc_dir': '../docs',
    'openapi': '3.0.2',
}

PW_DB_URL = 'mysql+pool://127.0.0.1:3306/'
PW_CONN_PARAMS = {
    'max_connections': 2,
    'charset': 'utf8mb4',
    'stale_timeout': 3600,
    'database': 'email_test',
    'user': 'root',
    'password': '12345678'
}

EMAIL_DOMAIN_NAME = 'xxx'
EMAIL_SENDER = 'xxx'
EMAIL_API_KEY = 'xxx'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_TASK_DEFAULT_EXCHANGE = 'default-exchange'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'email.default'
CELERY_TASK_DEFAULT_QUEUE = 'email.default'

CELERY_TASK_SOFT_TIME_LIMIT = 300

default_exchange = Exchange(CELERY_TASK_DEFAULT_EXCHANGE,
                            type=CELERY_TASK_DEFAULT_EXCHANGE_TYPE)

CELERY_TASK_QUEUES = (
    Queue(CELERY_TASK_DEFAULT_QUEUE, default_exchange,
          routing_key=CELERY_TASK_DEFAULT_ROUTING_KEY),
)

CELERY_IMPORTS = ('app.tasks',)
