from django.urls import path

from . import views

urlpatterns = [
    path(r'notifications', views.notifications, name='notifications'),
]
