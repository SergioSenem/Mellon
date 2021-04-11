from django.urls import path

from . import views

urlpatterns = [
    path('webhook', views.webhook, name='webhook'),
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('register', views.register, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('security_code', views.security_code, name='security_code')
]
