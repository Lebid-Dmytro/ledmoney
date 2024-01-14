# Ваш основний urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('statistic.urls')),
    # Інші шляхи можуть бути тут
]
