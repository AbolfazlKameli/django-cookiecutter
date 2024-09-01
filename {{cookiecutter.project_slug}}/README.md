# {{cookiecutter.project_name}}

{{cookiecutter.description}} <br>

> license: [{{cookiecutter.open_source_license}}]()

## Features

- **JWT Authentication**: Secure API access with JSON Web Tokens.
- **DRF Spectacular**: Automatic OpenAPI/Swagger documentation generation.
  {%- if cookiecutter.database == 'postgresql' %}
- **PostgreSQL Database**: Robust relational database management system.
  {% endif %}
  {%- if cookiecutter.caches == 'redis' %}
- **Redis for Caching**: High-performance cache layer for optimized API responses.
  {% endif %}
  {%- if cookiecutter.celery_message_broker == 'redis' %}
- **Redis as Celery Message Broker**: Redis is used as the message broker to efficiently handle task queues in Celery.
  {%- elif cookiecutter.celery_message_broker == 'rabbitmq-server'%}
- **Rabbit-mq as Celery Message Broker** : Rabbit-mq is used as the message broker to efficiently handle task queues in
  Celery.
  {% endif %}
- **Arvan Cloud Storage Integration**: Efficient and scalable storage solution.
- **Celery**: Asynchronous task management for handling background processes.
- **Custom User Model**: Flexible user authentication system with extended functionality.
- **Two-Step Registration**: Includes user registration flow with an activation URL sent via email.
- **SMTP Configuration**: Pre-configured for sending emails, supporting various SMTP services.

## Authors

- [{{cookiecutter.author_name}}]({{cookiecutter.github_profile_address}}) (What you did in this project)

## Run Locally

- Install required packages

{%- if cookiecutter.celery_message_broker == 'redis' or cookiecutter.caches == 'redis'%}
visit Redis [installation guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).
{%- elif cookiecutter.celery_message_broker == 'rabbitmq-server'%}
visit RabbitMQ [installation guide](https://www.rabbitmq.com/docs/download)

- Clone the project

```shell
$ git clone {{cookiecutter.github_profile_address}}/{{cookiecutter.project_slug}}
```

- Go to the project directory

```shell
$ cd {{cookiecutter.project_slug}}
```

- Make a virtual environment

```shell
$ python3 -m venv .venv
```

- Activate virtual environment

```shell
$ source .venv/bin/activate 
```

- Install requirements

```shell
$ pip install -r requirements.txt
```

- Apply Migrations to the Database

```shell
$ python managae.py migrate
```

- Start the django server

```shell
$ python manage.py runserver
```

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

### Celery

This app comes with Celery.<br>
To run a celery worker:

```shell
celery -A core worker -l INFO
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the
same folder with _manage.py_, you should be right.
