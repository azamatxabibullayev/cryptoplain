from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),

              ] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('main/', include('main.urls')),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
