from datetime import timedelta

from decouple import config

broker_connection_retry_on_startup = True

{% if cookiecutter.celery_message_broker == 'rabbitmq-server' %}
broker_url = "pyamqp://guest@localhost//"
result_backend = 'rpc://'
{% elif cookiecutter.celery_message_broker == 'redis' %}
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"
{% endif %}
worker_prefetch_multiplier = 3
{% if cookiecutter.use_timezone_in_celery == 'y' %}
timezone = config('TIME_ZONE')
{% endif %}
task_serializer = 'json'
result_serializer = 'pickle'
accept_content = ['json', 'pickle']
result_expire = timedelta(minutes=1)
