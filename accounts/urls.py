from django.urls import path

from . import views

urlpatterns = [
    path(r'upload_image', views.upload_image, name='upload_image'),
    path(r'image_crop', views.image_crop, name='image_crop'),
]
