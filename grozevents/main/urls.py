from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('event/<int:_id>/', views.event, name='event'),
    path('create_event/', views.create_event, name='create_event'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
