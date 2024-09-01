# django template

> powered by [cookiecutter](https://github.com/cookiecutter/cookiecutter). <br>
> powered by [cookiecutter django](https://github.com/cookiecutter/cookiecutter).

## Features

- for Django 5.1
- works with python 3.12
- **JWT Authentication**: Secure API access with JSON Web Tokens.
- **DRF Spectacular**: Automatic OpenAPI/Swagger documentation generation.
- **Arvan Cloud Storage Integration**: Efficient and scalable storage solution.
- **Celery**: Asynchronous task management for handling background processes.
- **Custom User Model**: Flexible user authentication system with extended functionality.
- **Two-Step Registration**: Includes user registration flow with an activation URL sent via email.
- **SMTP Configuration**: Pre-configured for sending emails, supporting various SMTP services.

## Optional Integrations

These features can be enabled during initial project setup.

- **PostgreSQL Database**: Robust relational database management system.
- **Beer or MIT License**.
- **Redis for Caching**: High-performance cache layer for optimized API responses.
- **Celery Configuration**: Flexibly choose between Redis or RabbitMQ as the message broker for Celery task management.

## Constraints

- Only maintained 3rd libraries are used.
- Uses PostgreSQL or SQLite.
- Environment variables for configuration.

## Authors

- [@AbolfazlKameli](https://github.com/AbolfazlKameli/) (cookiecutter configuration)
- [@AbolfazlKameli](https://github.com/AbolfazlKameli/) (back-end dev)

## Usage

Let's pretend you want to create a Django project called "StackOverFlow clone". Rather than using startproject and
then editing the results to include your name, email, and various configuration issues that always get forgotten until
the worst possible moment, get cookiecutter to do all the work.<br>
First, get Cookiecutter:

```shell
$ pip install cookiecutter
```

Now run it against this repo:

```shell
$ cookiecutter https://github.com/AbolfazlKameli/django-cookiecutter
```

You'll be prompted for some values. Provide them, then a Django project will be created for you. <br>
Answer the prompts with your own desired options. For example:

```shell
$ cookiecutter https://github.com/AbolfazlKameli/django-cookiecutter                                                                  08:51:34 PM
    [1/17] project_name (My API): StackOverFlow clone
    [2/17] project_slug (stackoverflow_clone): 
    [3/17] description (Behold My Awesome Project!): this is a clone of StackOverFlow
    [4/17] author_name (Abolfazl Kameli): Abolfazl Kameli
    [5/17] email_domain_name (gmail.com): 
    [6/17] email_address (abolfazl-kameli@gmail.com): abolfazlkameli0@gmail.com
    [7/17] github_username (AbolfazlKameli): 
    [8/17] github_profile_address (https://github.com/AbolfazlKameli): 
    [9/17] year (2024): 
    [10/17] domain_name (127.0.0.1): 
    [11/17] Select open_source_license
      1 - MIT
      2 - Beer
      Choose from [1/2] (1): 2
    [12/17] timezone (UTC): Asia/Tehran
    [13/17] use_timezone_in_celery (y): y
    [14/17] Select database
      1 - default
      2 - postgresql
      Choose from [1/2] (1): 2
    [15/17] Select caches
      1 - redis
      2 - none
      Choose from [1/2] (1): 1
    [16/17] Select celery_message_broker
      1 - redis
      2 - rabbitmq-server
      Choose from [1/2] (1): 1
    [17/17] debug (y): y
Initialized empty Git repository in /home/abolfazl/projects/stackoverflow_clone/.git/
```

Enter the project and take a look around:

```shell
$ cd stackoverflow_clone
$ ls
```

“🎉 Surprise! I’ve just set up a Git repository for you.”

Don't forget to carefully look at the generated README. Awesome, right?
 
