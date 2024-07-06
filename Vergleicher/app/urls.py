from django.contrib import admin
from django.urls import path,include
from .views import index,main,djacel
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='nomzodlar'),
    path('check/<str:pk>',main,name='check'),
    path('exam/',djacel,name = 'exam')
]