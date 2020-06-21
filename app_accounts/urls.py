from django.urls import path
from . import views

urlpatterns = [
    path('acceder/', views.login, name='loginName'),
    path('cerrarsesion/', views.logout, name='logoutName'),
    path('registrarse/', views.register2, name='register_name2'),
              ]

#   root is where you should look for info, and the path is MEDIA_URL
#   static is a whole app that allows to serve up images,files, etc...
