from django.urls import path 
from . import views 

urlpatterns =[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('post/<str:pk>',views.post,name='post'),
    path('blog',views.blog,name='blog'),
    path("test",views.test,name='test')
]