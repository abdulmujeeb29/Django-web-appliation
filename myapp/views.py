import email
from poplib import POP3_SSL_PORT
from pyexpat import features
import uuid
from django.shortcuts import get_object_or_404, render,redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from.models import *

# Create your views here.
def index(request):
    Goodss= Goods.objects.all()
    return render(request,'index.html',{'Goodss': Goodss})

def register(request) :
    if request.method == 'POST' :

        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']
        password2 =request.POST['password2']

        if password== password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return redirect('register')


            elif User.objects.filter(username=username).exists() :
                messages.info(request,'Username already used')
                return redirect('register')

            else :
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                #return redirect('login')
                
                user =auth.authenticate(username=username,password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('/')

        else:
            messages.info(request,'password not the same')
            return redirect('register')

    else:
        return render (request,'register.html')



def login(request):
    if request.method =='POST':

        username= request.POST['username']
        password=request.POST['password']

        user =auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect ('login')


    return render(request,'login.html ')



def logout(request):
    auth.logout(request)
    return redirect ('')
 
def blog(request):
    posts=Post.objects.all()

    if request.method == 'POST':
        title =request.POST['title']
        details = request.POST['details']

        post_id = uuid.uuid4()

        post= Post.objects.create(id= post_id,title=title, details=details) 
        post.save();


    return render (request,'blog.html',{'posts' :posts})       

def post(request, pk):                       #individual blog posts 
    posts=Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=posts).order_by('created')

    
    if request.method == 'POST':            #comment on a blog post 
        content = request.POST['content']
        author = request.user            #get the currently logged i user 

        comment = Comment.objects.create(content = content, author =author , post=posts )
        comment.save();
    
    return render(request,'post.html',{'posts':posts , 'comments' : comments})


# def delete_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if request.method == 'POST':
#         post.delete()
#         return redirect('/blog')

#     return render(request, 'delete_post.html', {'post': post})