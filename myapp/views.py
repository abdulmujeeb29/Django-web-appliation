import email

import uuid
from django.shortcuts import get_object_or_404, render,redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from.models import *

# Create your views here.
def index(request):
    
    return render(request,'index.html')

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


def specialuser_register(request):
    if request.method == 'POST' :

        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']
        password2 =request.POST['password2']
        specialization = request.POST['specialization']

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
                specialuser = SpecialUser.objects.create(user=user,specialization=specialization)
                #return redirect('login')
                
                user =auth.authenticate(username=username,password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('/')

        else:
            messages.info(request,'password not the same')
            return redirect('register')


    return render(request,'specialuser_reg.html')

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

def about(request):
    return render(request,'about.html')
# def contact(request):
#     return render(request,'contact.html')
 
def blog(request):
    blogposts= BlogPost.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        author=request.user 
        image =  request.FILES.get('image')
        post_id = uuid.uuid4()

        if title and body and image:
            # The fields are present, create and save the blog post
            blogpost = BlogPost.objects.create(title=title, body=body, author=author, image=image,id=post_id)
            return redirect('blog')

    return render (request,'blog.html', {'blogposts' : blogposts})       

def post(request, pk):                       #individual blog posts 
    posts=BlogPost.objects.get(id=pk)
    comments = Comment.objects.filter(post=posts).order_by('created')

    
    if request.method == 'POST':            #comment on a blog post 
        content = request.POST['content']
        author = request.user            #get the currently logged i user 

        comment = Comment.objects.create(content = content, author =author , post=posts )
        comment.save();
    
    return render(request,'post.html',{'posts':posts , 'comments' : comments})


def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('/blog')

    return render(request, 'delete_post.html', {'post': post})

