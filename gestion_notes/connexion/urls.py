from django.contrib import admin
from django.urls import path
from .views import connexion, Login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',connexion,name='connexion'),
    path('login/', Login, name='login'),
    path('logout/',logout, name='logout'),
]