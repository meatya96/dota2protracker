from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('matches.urls')),  # Главная страница - матчи
    path('teams/', include('teams.urls')),
    path('heroes/', include('heroes.urls')),
    path('leagues/', include('leagues.urls')),  # Перенесли leagues сюда
    path('matches/', include('matches.urls')),  # Дублирующий путь для явного доступа
]
