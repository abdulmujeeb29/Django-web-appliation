from django.urls import path 
from . import views 

urlpatterns =[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('post/<uuid:pk>',views.post,name='post'),
    path('blog',views.blog,name='blog'),
    # path('delete_post/<uuid:pk>/delete',views.delete_post, name='delete_post'),

]