from django.urls import path                    
from . import views

app_name = 'account'
urlpatterns = [
    path('register', views.create_account, name='register'),
    path('login', views.login, name="login"),
    path('logout',views.logout,name='logout')
]