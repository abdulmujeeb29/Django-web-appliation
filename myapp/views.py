import email

import uuid
from django.shortcuts import get_object_or_404, render,redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import auth 
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
                # registeration_email(email)
                
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
                return redirect('specialuser_reg')


            elif User.objects.filter(username=username).exists() :
                messages.info(request,'Username already used')
                return redirect('specialuser_reg')

            else :
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                specialuser = SpecialUser.objects.create(user=user,specialization=specialization)
                #return redirect('login')
                
                user =auth.authenticate(username=username,password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('/dashboard')

        else:
            messages.info(request,'password not the same')
            return redirect('/specialuser_reg')


    return render(request,'specialuser_reg.html')


from django.core.mail import send_mail

def registeration_email( email):
    subject = 'Thales'
    message = 'Welcome to ThalesMedia'
    from_email =settings.EMAIL_HOST_USER
    recipient = [email]

    sending = send_mail(subject,message,from_email,recipient , fail_silently=False)

    return sending
    



def login(request):
    if request.method =='POST':

        username= request.POST['username']
        password=request.POST['password']

        user =auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            
            # Check if the user is a SpecialUser
            if SpecialUser.objects.filter(user=user).exists():
                return redirect('/dashboard')  # Redirect to the special dashboard
            else:
                return redirect('/') 
        else:
            messages.info(request,'Invalid Credentials')
            return redirect ('login')


    return render(request,'login.html ')



def logout(request):
    auth.logout(request)
    return redirect ('/')

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
            messages.success(request, 'Your post has been successfully Created.')
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


# def delete_post(request, pk):
#     post = get_object_or_404(BlogPost, pk=pk)

#     if request.method == 'POST':
#         post.delete()
#         return redirect('/blog')

#     return render(request, 'delete_post.html', {'post': post})



@user_passes_test(lambda u: u.is_superuser)
def delete_post_superuser(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been successfully deleted.')
        return redirect('/blog')

    return render(request, 'delete_post.html', {'post': post})

def delete_post_special_user(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been successfully deleted.')
        return redirect('/myposts')  # Change this to the actual URL for special user page

    return render(request, 'delete_post.html', {'post': post})

# special user section 
@login_required
def specialuser_dashboard(request):
    user = request.user
    return render(request,'dashboard.html')

@login_required
def specialuser_post(request):
    user_id = request.user.id
    user_posts = BlogPost.objects.filter(author=user_id)
    return render(request, 'specialuser_post.html', {'user_posts': user_posts})

@login_required
def specialuser_allpost(request):
    user_id = request.user.id
    posts = BlogPost.objects.exclude(author=user_id)
    return render(request, 'specialuser_allpost.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES.get('image')
        body = request.POST['body']
        author = request.user
        post_id = uuid.uuid4()

        user_posts = BlogPost.objects.create(title=title,body=body,author=author,image=image, id=post_id)
        messages.success(request, 'Your post has been successfully Created .')
        return redirect('/dashboard')
        

    return render (request,'create_post.html')

def update_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        # Get data from the form
        title = request.POST['title']
        body = request.POST['body']
        image = request.FILES.get('image')

        # Update the post
        post.title = title
        post.body = body
        if image:
            post.image = image
        post.save()
        messages.success(request, 'Your post has been successfully Updated.')

        redirect_url = f'/update_post/{post.id}'
        return redirect(redirect_url)  # Replace with the appropriate URL
    
    return render(request, 'update_post.html', {'post': post})