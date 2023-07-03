from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('base_site.urls', namespace='base_site')),
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('admin/', admin.site.urls),
]
