from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    'TOKEN_OBTAIN_SERIALIZER': '{{cookiecutter.project_slug}}.users.serializers.MyTokenObtainPairSerializer',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
