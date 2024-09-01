from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

documents = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('{{cookiecutter.project_slug}}.users.urls', namespace='users')),
    path('schema/', include(documents))
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns = [
                      path('__debug__/', include('debug_toolbar.urls'))
                  ] + urlpatterns
