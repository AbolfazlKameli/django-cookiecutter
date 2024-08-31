from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    'TOKEN_OBTAIN_SERIALIZER': '{{cookiecutter.project_slug}}.apps.users.serializers.MyTokenObtainPairSerializer',
}
