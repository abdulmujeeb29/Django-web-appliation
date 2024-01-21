from django.urls import path 
from . import views 

urlpatterns =[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('post/<uuid:pk>',views.post,name='post'),
    path('blog',views.blog,name='blog'),
    path('about',views.about,name='about'),
    path('specialuser_reg',views.specialuser_register,name='specialuser_register'),
    path('dashboard',views.specialuser_dashboard,name='specialuser_dashboard'),
    path('myposts',views.specialuser_post,name='specialuser_post'),
    path('posts',views.specialuser_allpost,name='specialuser_allpost'),
    path('create_post',views.create_post, name='create_post'),
    path('update_post/<uuid:pk>',views.update_post, name='update_post'),
    # path('contact',views.contact,name='contact'),

    #path('delete/<uuid:pk>/delete',views.delete_post, name='delete_post'),
    path('delete_post_superuser/<uuid:pk>/', views.delete_post_superuser, name='delete_post_superuser'),
    path('delete_post_special_user/<uuid:pk>/',views.delete_post_special_user, name='delete_post_special_user'),

]

