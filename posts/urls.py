from django.urls import path
from .views import post_home,post_list,post_delete,post_detail,post_create,post_update

app_name= 'posts'
urlpatterns = [
    path('',post_home),
    path('create/',post_create,name='create'),
    path('list/',post_list,name='list'),
    path('<str:slug>/',post_detail,name='detail'),
    
    path('<str:slug>/edit/',post_update,name='update'),
    path('<str:slug>/delete/',post_delete,name='delete'),
    

]
