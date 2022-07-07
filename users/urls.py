'''определяет схемы URL для Learning_logs'''

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    #default authorization
    path('', include('django.contrib.auth.urls')),
    
    path('register/', views.register, name='register'),
    path('del_user/<int:user_id>/', views.del_user, name='del_user'),
    ]
