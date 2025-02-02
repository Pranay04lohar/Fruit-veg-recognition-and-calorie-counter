from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('home/', views.home, name='home'),
    path('upload_image/', views.upload_image,name = 'upload_image')
]

