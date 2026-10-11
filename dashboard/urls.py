from django.urls import path                    
from . import views

app_name = "dashboard"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('save_data',views.save_data,name="save_data")
    
]